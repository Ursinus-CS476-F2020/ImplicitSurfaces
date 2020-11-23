import numpy as np
import matplotlib.pyplot as plt

from skimage import measure

def getEllipsoidGaussian(x, y, c, v1, sigma1, v2, sigma2):
    """
    Given a grid of points, create a multivariate Gaussian function
    with ellipsoidal cross sections
    Parameters
    ----------
    x: ndarray(M, N)
        A grid of x locations
    y: ndarray(M, N)
        A grid of y locations
    c: list(x, y)
        Location of the center of the Gaussian
    v1: list(x, y)
        Direction of the first principal axis
    sigma1: float
        Standard deviation along the first principal axis
    v2: list(x, y)
        Direction of the second principal axis
    sigma2: float
        Standard deviation along the second principal axis

    Returns
    -------
    f: ndarray(M, N)
        The corresponding scalar function of the Gaussian evaluated
        at all points on the grid
    """
    c = np.array(c, dtype=float).flatten()
    v1 = np.array(v1, dtype=float).flatten()
    v1 /= np.sqrt(np.sum(v1**2))
    v2 = np.array(v2, dtype=float).flatten()
    v2 /= np.sqrt(np.sum(v2**2))
    X = np.array([x, y]).T
    print(X.shape)
    X -= c[None, :]
    d1 = (X.dot(v1))**2/(sigma1**2)
    d2 = (X.dot(v2))**2/(sigma2**2)
    return np.exp(-d1)*np.exp(-d2)

def displayContours(f, cutoff):
    """
    Display the level sets of a function f given 
    a particular cutoff
    """
    contours = measure.find_contours(f, cutoff)
    plt.imshow(f.T, cmap=plt.cm.gray)
    plt.colorbar()
    for n, contour in enumerate(contours):
        plt.plot(contour[:, 0], contour[:, 1], linewidth=2)
    ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])

def makeBlobsMergingVideo():
    pix = np.linspace(0, 1, 100)
    x, y = np.meshgrid(pix, pix)

    sigmas = np.linspace(0.05, 0.2, 50)

    for i, sigma in enumerate(sigmas):
        f1 = np.exp(-((x-0.3)**2 + (y-0.6)**2)/(sigma**2))
        f2 = np.exp(-((x-0.6)**2 + (y-0.3)**2)/(sigma**2))
        f = f1 + f2

        # Display the image and plot all contours found
        displayContours(f, 0.2)
        plt.title("$\\sigma = %.3g$"%sigma)
        plt.savefig("%i.png"%i)

def isotropicGaussian():
    pix = np.linspace(0, 1, 100)
    x, y = np.meshgrid(pix, pix)
    sigma = 0.1
    cx = 0.5
    cy = 0.5
    f = np.exp(-((x-cx)**2+(y-cy)**2)/(sigma**2))
    displayContours(f, 0.5)
    plt.show()



def mySurface():
    pix = np.linspace(0, 1, 100)
    x, y = np.meshgrid(pix, pix)

    f1 = getEllipsoidGaussian(x, y, [0.3, 0.5], [1, 1], 0.1, [1, -1], 0.2)
    f2 = getEllipsoidGaussian(x, y, [0.6, 0.6], [1, 0], 0.2, [0, 1], 0.05)

    f = f1 + f2
    #f = np.minimum(f1, f2)
    displayContours(f, 0.2)
    plt.show()

#makeBlobsMergingVideo()
#isotropicGaussian()
mySurface()