import numpy as np


class Atom:
    def __init__(self, id, p, v=None, type=None):
        self.id = id
        self.position = p
        self.velocity = v
        self.type = type
        self.properties = {}

    def set_property(self, name, vale):
        self.properties[name] = value


class DumpReader:

    def __init__(self, file, type='atom'):
        self.file_name = str(file)
        self.atoms = []
        #self.box = None
        #self.timestep = None
        self.parse(type)


    def parse(self, type):
        if type == 'atom':
            self.parse_atom_style()
            return
        elif type == 'xyz':
            self.parse_xyz_style()
            return
        else:
            print('Style not supported')
            return


    def parse_atom_style(self):
        list = []

        file = open(self.file_name, 'r')

        linenumber = 0
        reading_atoms = False
        id = 0
        for line in file:

            if line.find('ITEM: ATOMS') >= 0:
                reading_atoms = True
                continue

            if reading_atoms:
                l = line.split()
                #id = int(l[0])
                t = l[1]
                p = [float(l[2]), float(l[3]), float(l[4])]
                self.atoms.append(Atom(id, p, type=t))
                id+=1


    def parse_xyz_style(self):
        print('Implementation Incomplete / Not working')
        return None

    def delete_atom(self, id):
        pass


class DataReader:

    def __init__(self, file):
        self.file_name = str(file)
        self.atoms = []
        #self.box = None
        #self.timestep = None
        self.parse()

    def parse(self):
        list = []

        file = open(self.file_name, 'r')

        linenumber = 0
        id = 0
        reading_atoms = False
        for line in file:

            if line.find('ITEM: ATOMS') >= 0:
                reading_atoms = True
                continue

            if reading_atoms:
                d = {}
                l = line.split()
                d['position'] = [float(l[2]), float(l[3]), float(l[4])]
                d['tag'] = l[1]
                d['velocity'] = None
                d['properties'] = None
                self.atoms.append(Atom(d, id))
                id += 1


    def parse_xyz_style(self):
        print('Implementation Incomplete / Not working')
        return None

    def delete_atom(self, id):
        pass




if __name__=='__main__':

    a = DumpReader('dump.atom')
