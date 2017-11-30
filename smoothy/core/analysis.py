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
