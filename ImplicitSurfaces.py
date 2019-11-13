import sys

import numpy as np
import matplotlib.pyplot as plt
import mcubes #https://github.com/pmneila/PyMCubes

def saveOffFileExternal(filename, VPos, ITris):
    """
    Save OFF file given vertex and triangle buffers
    Parameters
    ----------
    filename: string
        Path to which to save file
    VPos: ndarray(M, 3)
        Coordinates of the M vertices
    ITris: ndarray(N, 3)
        Vertex indices of the N triangles
    """
    nV = VPos.shape[0]
    nF = ITris.shape[0]
    if nV == 0:
        print("ERROR: The mesh you're trying to save has zero vertices, so the volume is either all negative or all positive")
        return
    fout = open(filename, "w")
    fout.write("OFF\n%i %i %i\n"%(nV, nF, 0))
    for i in range(nV):
        fout.write("%g %g %g\n"%tuple(VPos[i, :]))
    for i in range(nF):
        fout.write("3 %i %i %i\n"%tuple(ITris[i, :]))
    fout.close()

def getBowlingPin():
    X, Y, Z = np.mgrid[:100, :100, :100]
    u = np.exp(-((X-70.0)**2 + (Y-70.0)**2 + (Z-70.0)**2)/(2.0*6.0**2))
    u += np.exp(-((X-50.0)**2 + (Y-50.0)**2 + (Z-50.0)**2)/(2.0*15.0**2))
    u = u - 0.2
    VPos, ITris = mcubes.marching_cubes(u, 0)
    saveOffFileExternal("bowlingpin.off", VPos, ITris)

def getCutSphere():
    X, Y, Z = np.mgrid[:100, :100, :100]
    u1 = np.exp(-((X-50.0)**2 + (Y-50.0)**2 + (Z-50.0)**2)/(2.0*15.0**2))
    

    VPos, ITris = mcubes.marching_cubes(u1-0.5, 0)
    saveOffFileExternal("sphere.off", VPos, ITris)

if __name__ == '__main__':
    getCutSphere()