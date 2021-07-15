import numpy as np
from math import floor


class Grid:

    def __init__(self, atoms, size=2):
        self.cells = {}
        self.size = size

        for atom in atoms:
            idr, idp = self.get_idpolar(atom.position)
            # idr, idp = self.get_idpolar2(atom.position, 4)
            idz = self.get_idz(atom.position)
            try:
                self.cells[(idr, idp,  idz)].add_atom(atom)
            except:
                self.cells[(idr, idp,  idz)] = Cell(idr, idp,  idz)
                self.cells[(idr, idp,  idz)].compute_volume(self.size)
                self.cells[(idr, idp,  idz)].add_atom(atom)

        self.ncells = len(self.cells)


    def get_idpolar(self, pos):

        ''' Calculate the IDs of radius coordinate and angular coordinate
        for a cell volume approximately close to cartesian, i.e. different
        angular division for different radius'''

        r = np.sqrt(pos[0]**2 + pos[1]**2)
        idr = floor(r / self.size)
        N = round(np.pi*(idr+1))
        bin_theta = 2*np.pi / N
        angle = np.arctan2(pos[1], pos[0])+np.pi
        idp = floor(angle / bin_theta)
        return idr, idp

    def get_idpolar2(self, pos, nangle):

        ''' Calculate the IDs of radius coordinate and angular coordinate
        for a cell volume having the same angle division in different radii.
        Obs.: Outer cells have larger volume'''

        r = np.sqrt(pos[0]**2 + pos[1]**2)
        idr = floor(r / self.size)
        bin_theta = 2*np.pi / nangle
        angle = np.arctan2(pos[1], pos[0])+np.pi
        idp = floor(angle / bin_theta)
        return idr, idp


    def get_idz(self, pos):
        return floor(pos[2] / self.size)

    def compute_density_correlation(self):
        pass


class Cell:

    def __init__(self, idr, idp, idz):
        self.atoms = []
        self.id = (idr, idp, idz)
        self.volume = None
        self.nangle = round(np.pi*(idr+1))
        self.angle = 2*np.pi / self.nangle
        self.density = None

    def add_atom(self, atom):
        self.atoms.append(atom)

    def compute_volume(self, size):
        self.volume = self.angle * size**3 * (2*self.id[0] + 1) * 0.5

    def get_density(self):
        return len(self.atoms) / self.volume


if __name__=='__main__':

    import sys
    import os
    sys.path.insert(0, os.path.expanduser('~')+'/md-projects/lampy')
    from readLammps import DumpReader

    data = DumpReader(sys.argv[1])

    grd = Grid(data.atoms, size = float(sys.argv[2])*0.75)

    idr = []
    idz = []
    d = []
    for key, cell in grd.cells.items():
        idr.append(cell.id[0])
        idz.append(cell.id[2])
        d.append(cell.get_density()/cell.nangle)

    from scipy.sparse import coo_matrix
    coo = coo_matrix((d, (idr, idz)))

    coo = coo.todense().transpose()

    import matplotlib.pyplot as plt


    fig, ax = plt.subplots(1,1)
    im = ax.imshow(coo)
    fig.colorbar(im)
    ax.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
    ax.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks
    plt.show()
