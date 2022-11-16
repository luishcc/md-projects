import os

from mdpkg.rwfile import DumpReader, Dat


snap = 10

trj = DumpReader('test.lammpstrj')
trj.read_sequential()
trj.read_velocity('dump.vel', trj.snap)


with open('comb.lammpstrj', 'w') as fd:
    while True:
        try:
            trj.read_next()
            trj.read_velocity('dump.vel', trj.snap)
        except Exception as e:
            print(e)
            exit()

        print(trj.snap.time)
        fd.write('ITEM: TIMESTEP\n')
        fd.write(f'{trj.snap.time}\n')
        fd.write('ITEM: NUMBER OF ATOMS\n')
        fd.write(f'{trj.snap.natoms}\n')
        fd.write('ITEM: BOX BOUNDS pp pp pp\n')
        fd.write(f'{trj.snap.box.xlo} {trj.snap.box.xhi}\n')
        fd.write(f'{trj.snap.box.ylo} {trj.snap.box.yhi}\n')
        fd.write(f'{trj.snap.box.zlo} {trj.snap.box.zhi}\n')
        fd.write('ITEM: ATOMS id type x y z vx vy vz\n')
        for id, atom in trj.snap.atoms.items():
            x,y,z = atom.position
            vx,vy,vz = atom.velocity
            fd.write(f'{id} 1 {x} {y} {z} {vx} {vy} {vz}\n')
