from .utils import fix_mask, slab
import numpy as np

def rms(data, mask=None):
    """
    Compute the RMS of data. If mask != None, then we use that mask.

    Parameters
    ----------
    data : (M,N,Z) numpy.ndarray or astropy.nddata.NDData or or astropy.nddata.NDDataRef
        Astronomical data cube.

    mask : numpy.ndarray (default = None)

    Returns
    -------
    RMS of the data (float)
    """
    # TODO: check photutils background estimation for using that if possible
    if mask is not None:
        data = fix_mask(data, mask)
    mm = data * data
    rms = np.sqrt(mm.sum() * 1.0 / mm.size)
    return rms

def denoise(data, threshold):
    """
    Performs denoising of data cube, thresholding over the threshold value.

    Parameters
    ----------
    data : numpy.ndarray or astropy.nddata.NDData or or astropy.nddata.NDData
        Astronomical data cube.
    threshold : float
        Threshold value used for denoising.

    Returns
    -------
    result : numpy.ndarray
        Denoised (thresholded) astronomical data cube.
    """

    elms = data > threshold
    newdata = np.zeros(data.shape)
    newdata[elms] = data[elms]
    return newdata

def gaussian_function(mu, P, feat, peak):
    """
    Generates an N-dimensional Gaussian using the feature matrix feat,
    centered at mu, with precision matrix P and with intensity peak.

    Parameters
    ----------
    mu : numpy.ndarray
        Centers of gaussians array.
    P : numpy.ndarray
        Precision matrix.
    feat : numpy.ndarray.
        Features matrix.
    peak : float
        Peak value of the resulting evaluation.

    Returns
    -------
    result: 2D numpy.ndarray
        Returns the gaussian function evaluated at the value on feat.
    """

    cent_feat = np.empty_like(feat)
    for i in range(len(mu)):
        cent_feat[i] = feat[i] - mu[i]
    qform = (P.dot(cent_feat)) * cent_feat
    quad = qform.sum(axis=0)
    res = np.exp(-quad / 2.0)
    res = peak * (res / res.max())
    return res

def integrate(data, mask=None, axis=(0)):
    """
    Sums the slices of a cube of data given an axis.

    Parameters
    ----------
    data : (M,N,Z) numpy.ndarray or astropy.nddata.NDData or astropy.nddata.NDDataRef
        Astronomical data cube.

    mask : numpy.ndarray (default = None)

    axis : int (default=(0))

    Returns
    -------
     A numpy array with the integration results.

    """
    if mask is not None:
        data = fix_mask(data, mask)
    newdata = np.sum(data, axis=axis)
    mask = np.isnan(newdata)
    return newdata
