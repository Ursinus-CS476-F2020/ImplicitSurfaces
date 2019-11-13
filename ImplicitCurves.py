import numpy as np
import matplotlib.pyplot as plt

from skimage import measure

def makeBlobsMergingVideo():
    pix = np.linspace(0, 1, 100)
    x, y = np.meshgrid(pix, pix)

    sigmas = np.linspace(0.05, 0.2, 50)

    for i, sigma in enumerate(sigmas):
        f1 = np.exp(-((x-0.3)**2 + (y-0.6)**2)/(sigma**2))
        f2 = np.exp(-((x-0.6)**2 + (y-0.3)**2)/(sigma**2))
        f = f1 + f2

        contours = measure.find_contours(f, 0.2)

        # Display the image and plot all contours found
        plt.clf()
        plt.imshow(f, cmap=plt.cm.gray)
        plt.colorbar()
        for n, contour in enumerate(contours):
            plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
        ax = plt.gca()
        ax.set_xticks([])
        ax.set_yticks([])
        plt.title("$\\sigma = %.3g$"%sigma)
        plt.savefig("%i.png"%i)

makeBlobsMergingVideo()
