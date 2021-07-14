import numpy as np
from math import floor


class Grid:

    def __init__(self, atoms, size=2):
        self.cells = {}
        self.size = size
        self.ncells = len(self.cells)

        for atom in atoms:
            idr, idp = get_idpolar(atom.position)
            idz = get_idz(atom.position)
            try:
                self.cells[(idr, idp,  idz)].add_atom(atom)
            except:
                self.cells[(idr, idp,  idz)] = Cell(idr, idp,  idz)
                self.cells[(idr, idp,  idz)].add_atom(atom)


    def get_idpolar(self, pos):
        r = np.sqrt(pos[0]**2 + pos[1]**2)
        idr = floor(r / self.size)
        N = round(np.pi*(idr+1))
        bin_theta = 2*np.pi / N
        angle = np.arctan2(pos[1], pos[0])+np.pi
        idp = floor(angle / bin_theta)
        return idr, idp

    def get_idz(self, pos):
        return floor(pos[2] / self.size)


class Cell:

    def __init__(self, idr, idp, idz):
        self.atoms = []


    def add_atom(self, atom):
        self.atoms.append(atom)
