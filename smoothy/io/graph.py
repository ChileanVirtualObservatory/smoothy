from astropy import log
import numpy as np
from astropy.wcs import wcs
from astropy.nddata import support_nddata
from smoothy.core.analysis import rms
from smoothy.upi.axes import axes_names, axes_units, extent, spectral_velocities, _get_axis
import ipyvolume.pylab as ipvlab
import matplotlib.pyplot as plt

# TODO: complete the nddata support (i.e. data, meta...)
# TODO: make animation possible again


@support_nddata
def visualize(data, wcs=None, unit=None, contour=False):
    """
    Generic function to visualize data, line-plot for 1D and image for 2D.

    Parameters
    ----------
    data : numpy.ndarray or astropy.nddata.NDData or astropy.nddata.NDDataRef
        Astronomical image

    wcs : astropy.wcs.WCS
        World Coordinate System from the image (not needed if contained in NDData)

    unit : astropy.unit
        Image units (not needed if contained in NDData)

    contour : numpy.ndarray
        For plotting Contourns
    """
    if data.ndim == 1:
        return visualize_plot(data, wcs, unit)
    elif data.ndim == 2:
        return visualize_image(data, wcs, unit, contour)
    elif data.ndim == 3:
        return visualize_volume(data, wcs, unit, contour)
    else:
        log.error("Data dimensions must be between 1 and 3")


@support_nddata
def visualize_plot(data, wcs=None, unit=None):
    """
    Plot 1D data for astronomical data.

    Parameters
    ----------
    data : numpy.ndarray or astropy.nddata.NDData
        Astronomical image

    wcs : astropy.wcs.WCS
        World Coordinate System from the image (not needed if contained in NDData)

    unit : astropy.unit
        Image units (not needed if contained in NDData)
    """
    if wcs is None:
        plt.plot(data)
        plt.ylabel(unit)
    else:
        # TODO: Implement x vector, but check why the wcs cannot be onedimensional!
        plt.plot(data)
        plt.ylabel(unit)
        plt.xlabel(wcs.axis_type_names[0])
    #plt.show()


@support_nddata
def visualize_image(data, wcs=None, unit=None, contour=False):
    """
    Plot 2D astronimical data.

    Parameters
    ----------
    data : numpy.ndarray or astropy.nddata.NDData or astropy.nddata.NDDataRef
        Astronomical image

    wcs : astropy.wcs.WCS
        World Coordinate System from the image (not needed if contained in NDData)

    unit : astropy.unit
        Image units (not needed if contained in NDData)

    contour : numpy.ndarray
        For plotting Contourns
    """
    if wcs is None:
        plt.imshow(data, origin='lower', cmap=plt.cm.gist_heat)
        cb = plt.colorbar()
        cb.ax.set_ylabel(unit)
    else:
        gax = plt.subplot(111,projection=wcs)
        plt.imshow(data, origin='lower', cmap=plt.cm.gist_heat)
        g0 = gax.coords[0]
        g1 = gax.coords[1]
        g0.set_axislabel(wcs.axis_type_names[0])
        g1.set_axislabel(wcs.axis_type_names[1])
        g0.grid(color='yellow', alpha=0.5, linestyle='solid')
        g1.grid(color='yellow', alpha=0.5, linestyle='solid')
        cb = plt.colorbar()
        cb.ax.set_ylabel(unit)
    if contour:
        arms = rms(data)
        dmax = data.max()
        crs = np.arange(1, dmax/arms)
        plt.contour(data, levels=arms*crs, alpha=0.5)
    plt.show()


def _draw_spectra(data, wcs=None, unit=None,velocities=False):
    try:
        freq_axis = _get_axis(wcs, "FREQ")
    except ValueError:
        log.warning("Data does not have a spectral dimension")
        return
    ll = list(range(wcs.naxis))
    ll.remove(freq_axis)
    yvals = np.nansum(data, axis=tuple(ll))
    plt.ylabel(unit)
    if velocities:
        xvals = spectral_velocities(data, wcs=wcs)
        plt.xlabel("VEL [Km/s]")
    else:
        dim = wcs.wcs.spec
        fqis = np.arange(data.shape[data.ndim - dim - 1])
        idx = np.zeros((fqis.size, data.ndim))
        idx[:, dim] = fqis
        vals = wcs.all_pix2world(idx, 0)
        xvals = vals[:, dim]
        plt.xlabel("FREQ [Hz]")
    plt.plot(xvals, yvals)


@support_nddata
def visualize_spectra(data, wcs=None, unit=None, velocities=False):
    if wcs is None:
        if data.ndim != 1:
            log.info("Only 1D data can be shown without WCS")
            return
        else:
            visualize_plot(data, wcs, unit)
            return
    _draw_spectra(data, wcs, unit, velocities)
    plt.show()

@support_nddata
def visualize_volume(data, wcs=None, unit=None):
    if wcs is None:
        log.error("WCS is needed by this function")
        return

    if unit is None:
        log.error("Unit is needed by this function")
        return

    ipvlab.clear()

    labels = ["{} [{}]".format(axe, str(unit)) for axe, unit in
              zip(upi.axes_names(data, wcs), upi.axes_units(data, wcs))]

    ipvlab.xyzlabel(*labels[::-1])

    extent = upi.extent(data, wcs)
    minlim = extent[0]
    maxlim = extent[1]

    ipvlab.xlim(minlim[2].value, maxlim[2].value)
    ipvlab.ylim(minlim[1].value, maxlim[1].value)
    ipvlab.zlim(minlim[0].value, maxlim[0].value)

    ipvlab.style.use('dark')

    tf = ipvlab.transfer_function(level=[0.39, 0.54, 0.60], opacity=[0.2, 0.2, 0.2])
    vol = ipvlab.volshow(data, tf=tf, controls=False, level_width=0.1)

    ipvlab.gcf().width = 1024
    ipvlab.gcf().height = 456

    ipvlab.show()
