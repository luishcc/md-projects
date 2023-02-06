#--------------------------------------------------------------#
#               Write a LAMMPS data file (SIMPLIFIED)
#
#               Luis Carnevale
#               14 Feb 2021
#--------------------------------------------------------------#

class DataFile:
    def __init__(self, box, atoms):
        self.box = box
        self.atoms = atoms
        self.header = None

    def set_header(self, text):
        self.header = str(text)
        return

    def write_file(self, name, dir,):
        file = open(f'{dir}/{name}.data', 'w')
        self.write_header(file)
        self.write_info(file)
        self.write_mass(file)
        self.write_atoms(file)
        file.close()

    def write_header(self, file):
        if self.header is None:
            file.write('Lammps .data input file\n\n')
        else:
            file.write(self.header+'\n\n')
        return

    def write_info(self, file):
        file.write(f'{self.atoms.number} atoms\n')
        file.write('\n')
        file.write('1 atom types\n')
        file.write('\n')
        file.write(f'{self.box.xlo} {self.box.xhi} xlo xhi\n')
        file.write(f'{self.box.ylo} {self.box.yhi} ylo yhi\n')
        file.write(f'{self.box.zlo} {self.box.zhi} zlo zhi\n')
        file.write('\n')
        return

    def write_mass(self, file):
        file.write('Masses\n\n')
        file.write('1 1\n')
        file.write('\n')
        return

    def write_atoms(self, file):
        file.write('Atoms\n\n')
        pos = self.atoms.positions
        typ = self.atoms.types
        for i in range(self.atoms.number):
            t = typ[i]
            file.write(f'{i+1} {t} 1 {pos[i].x} {pos[i].y} {pos[i].z}\n')
        return
