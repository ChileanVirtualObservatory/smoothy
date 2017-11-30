import numpy as np


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


