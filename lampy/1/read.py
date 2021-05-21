import numpy as np


class Atom:
    def __init__(self, dict):
        self.x = dict.get('position')
        self.v = dict.get('velocity')
        self.tag = dict.get('tag')
        self.properties = dict.get('properties')

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
        print(type, type=='atom')
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
        for line in file:

            if line.find('ITEM: ATOMS') >= 0:
                reading_atoms = True
                continue

            if reading_atoms:
                d = {}
                l = line.split()
                d['position'] = [l[2], l[3], l[4]]
                d['tag'] = l[1]
                d['velocity'] = None
                d['properties'] = None
                self.atoms.append(Atom(d))


    def parse_xyz_style(self):
        print('Implementation Incomplete / Not working')
        return None

if __name__=='__main__':

    a = DumpReader('dump.atom')
