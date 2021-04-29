#--------------------------------------------------------------#
#               Write a LAMMPS data file
#
#               Luis Carnevale
#               14 Feb 2021
#--------------------------------------------------------------#

class DataFile:
    def __init__(self, box, atoms, bonds=None, angles=None,
                 dihedrals=None, impropers=None):
        self.box = box
        self.atoms = atoms
        self.bonds = bonds
        self.angles = angles
        self.dihedrals = dihedrals
        self.impropers = impropers
        self.header = None
        self.info = self.get_info()

    def set_header(self, text):
        self.header = str(text)
        return

    def get_info(self):
        list = [self.atoms]
        if self.bonds is not None:
            list.append(self.bonds)
        if self.angles is not None:
            list.append(self.angles)
        if self.dihedrals is not None:
            list.append(self.dihedrals)
        if self.impropers is not None:
            list.append(self.impropers)
        return list

    def write_file(self, name, dir,):
        file = open(f'{dir}/{name}.data', 'w')
        self.write_header(file)
        self.write_info(file)
        self.write_mass()
        self.write_atoms()
        self.write_velocities()
        file.close()

    def write_header(self, file):
        if self.header is None:
            file.write('Lammps .data input file\n\n')
        else:
            file.write(self.header+'\n\n')
        return

    def write_info(self, file):
        for item in self.info:
            file.write(f'{item.number} {item.label}\n')
        file.write('\n')
        for item in self.info:
            file.write(f'{item.number_types} {item.label[:-1]} types\n')
        file.write('\n')
        file.write(f'{self.box.xlo} {self.box.xhi} xlo xhi\n')
        file.write(f'{self.box.ylo} {self.box.yhi} ylo yhi\n')
        file.write(f'{self.box.zlo} {self.box.zhi} zlo zhi\n')
        file.write('\n')
        return

    def write_mass(self, file):
        # file.write('Masses\n\n')
        # for i in range(self.atoms.number_types):
        #     file.write(f'{self.atoms.types.label} {}')
        pass

    def write_atoms(self):
        pass

    def write_velocities(self):
        pass
