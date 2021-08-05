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

class Box:

    def __init__(self, list):
        self.xlo = list[0]
        self.xhi = list[1]
        self.ylo = list[2]
        self.yhi = list[3]
        try:
            self.zlo = list[4]
            self.zhi = list[5]
        except:
            self.zlo = None
            self.zhi = None

    def get_length_x(self):
        return self.xhi - self.xlo

    def get_length_y(self):
        return self.yhi - self.ylo

    def get_length_z(self):
        return self.zhi - self.zlo


class Reader:

    def __init__(self):
        self.timesteps = []

    def read_timestep(self, file_name):
        numt = 0

        def skip_lines(f, n_skip):
            for _ in range(n_skip):
                f.readline()

        with open(file_name, ,'r') as file:

            read_time = False
            for line in file:

                if line.find('ITEM: TIMESTEP') >= 0:
                    read_time = True
                    continue

                if read_time:
                    l = float(line)
                    self.timestep.append(l)
                    read_time = False
                    skip_lines()






class DumpReader:

    def __init__(self, file, type='atom'):
        self.file_name = str(file)
        self.atoms = []
        self.box = None
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
        reading_box = False
        id = 0
        box_dim = []
        for line in file:

            if line.find('ITEM: ATOMS') >= 0:
                reading_atoms = True
                continue

            if line.find('ITEM: BOX BOUNDS ') >= 0:
                reading_box = True
                dim_id = 0
                continue

            if reading_box:
                l = line.split()
                box_dim.append(float(l[0]))
                box_dim.append(float(l[1]))
                dim_id += 1
                if dim_id >= 3:
                    reading_box = False
                continue


            if reading_atoms:
                l = line.split()
                #id = int(l[0])
                t = l[1]
                p = [float(l[2]), float(l[3]), float(l[4])]
                self.atoms.append(Atom(id, p, type=t))
                id+=1
        self.box = Box(box_dim)
        return


    def parse_xyz_style(self):
        print('Implementation Incomplete / Not working')
        return None




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
