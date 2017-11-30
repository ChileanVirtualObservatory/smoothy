import numpy as np

def fix_mask(data, mask):
    """

    Parameters
    ----------
    data : numpy.ndarray or numpy.ma.MaskedArray
        Astronomical data cube.
    mask : numpy.ndarray
        Boolean that will be applied.

    Returns
    -------
    result : numpy.ma.MaskedArray
        Masked astronomical data cube.
    """

    ismasked = isinstance(data, np.ma.MaskedArray)
    if ismasked and mask is None:
        return data
    else:
        return np.ma.MaskedArray(data, mask)

def fix_limits(data, vect):
    """
    Fix vect index to be inside data

    Parameters
    ----------
    data : numpy.ndarray or numpy.ma.MaskedArray
        Astronomical data cube.
    vect : tuple, list or numpy.ndarray
        Array with the indexes to be fixed.

    Returns
    -------
    result : numpy.ndarray
        Fixed array of indexes.
    """

    if isinstance(vect, (tuple, list)):
        vect = np.array(vect)
    vect = vect.astype(int)
    low = vect < 0
    up = vect > data.shape
    if vect.any():
        vect[low] = 0
    if vect.any():
        vect[up] = np.array(data.shape)[up]
    return vect

def index_features(data, lower=None, upper=None):
    """ Creates an array with indices in features format """
    msh = index_mesh(data, lower, upper)
    dim = data.ndim
    ii = np.empty((dim, int(msh.size / dim)))
    for i in range(dim):
        ii[dim - i - 1] = msh[i].ravel()
    return ii

def slab(data, lower=None, upper=None):
    """
    Obtain the n-dimensional slab from lower to upper (i.e. slab is a vector of slices)

    Parameters
    ----------
    data : numpy.ndarray
        Atronomical data cube.
    lower : 3-tuple (default=None)
        Lower coordinates for the subcube.

    upper : 3-tuple (default=None)
        Upper coordinates for the subcube.


    Returns
    -------
    result : list
       list of slices using lower and upper coordinates to create a subcube.
    """

    if lower is None:
        lower = np.zeros(data.ndim)
    if upper is None:
        upper = data.shape
    lower = fix_limits(data, lower)
    upper = fix_limits(data, upper)
    m_slab = []
    for i in range(data.ndim):
        m_slab.append(slice(lower[i], upper[i]))
    return m_slab


def standarize(data):
    """
    Standarize astronomical data cubes in the 0-1 range.

    Parameters
    ----------
    data : numpy.ndarray or astropy.nddata.NDData or or astropy.nddata.NDData
        Astronomical data cube.

    Returns
    -------
    result : tuple
        Tuple containing the standarized numpy.ndarray or astropy.nddata.NDData cube, the factor scale y_fact and the shift y_min.
    """
    y_min = data.min()
    res = data - y_min
    y_fact = res.sum()
    res = res / y_fact
    return (res, y_fact, y_min)


def unstandarize(data, a, b):
    """
    Unstandarize the astronomical data cube: :math:`a \cdot data + b`.

    Parameters
    ----------
    data : numpy.ndarray or astropy.nddata.NDData or or astropy.nddata.NDData
        Astronomical data cube.
    a : float
        Scale value.
    b : float
        Shift value.

    Returns
    -------
    result : numpy.ndarray or astropy.nddata.NDData
        Unstandarized astronomical cube.
    """
    return a*data+b

def add(data, flux, lower, upper):
    """
    Adds flux to a sub-cube of an astronomical data cube.

    Parameters
    ----------
    data : numpy.ndarray or astropy.nddata.NDData or or astropy.nddata.NDData
        Astronomical data cube.
    flux : numpy.ndarray
        Flux added to the cube.
    lower : float
        Lower bound of the sub-cube to which flux will be added.
    upper : float
        Upper bound of the sub-cube to which flux will be added.
    """

    data_slab, flux_slab = matching_slabs(data, flux, lower, upper)
    data[data_slab] += flux[flux_slab]

def matching_slabs(data, flux, lower, upper):
    """
    Obtain the matching subcube inside the lower and upper points.

    Paramters
    ---------
    data : numpy.ndarray
        First data cube

    flux : numpy.ndarray
        Second data cubse

    lower : tuple
        Lower coordinates for the subcube.

    upper : tuple
        Upper coordinates for the subcube.


    Returns
    -------
    The subcube inside the lower and upper points that matches both data cube dimensions.
    """

    data_slab = slab(data, lower, upper)
    flow = np.zeros(flux.ndim)
    fup = np.array(flux.shape)
    for i in range(data.ndim):
        if data_slab[i].start == 0:
            flow[i] = flux.shape[i] - data_slab[i].stop
        if data_slab[i].stop == data.shape[i]:
            fup[i] = data_slab[i].stop - data_slab[i].start
    flux_slab = slab(flux, flow, fup)
    return data_slab, flux_slab
