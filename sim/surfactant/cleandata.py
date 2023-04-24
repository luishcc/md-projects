import os
from ovito.io import *
from ovito.modifiers import *

R = 8
sc = 1.8

file = f'initial_cylinder_{R}_{sc}.data'
save_file = '.'.join([file,'CLEAN'])
if os.path.isfile(save_file):
    print(f'File {save_file} already exists.')
    while True:
        answer = input('Do you want to proceed? (yes/no)')
        if answer == "yes" or answer == "y":
            print("Proceeding...")
            break
        elif answer == "no" or answer == "n":
            print("Aborting...")
            exit()
        else:
            print("Invalid input, please enter 'yes' or 'no'.")

pipeline = import_file(file, atom_style='hybrid', atom_substyles=('angle', 'mdpd'))

cluster_mod = ClusterAnalysisModifier(cutoff=0.9, sort_by_size=True)
pipeline.modifiers.append(cluster_mod)

select_mod = ExpressionSelectionModifier(expression = 'Cluster != 1')
pipeline.modifiers.append(select_mod)

pipeline.modifiers.append(DeleteSelectedModifier())

pipeline.compute()

export_file(pipeline, save_file, 
    'lammps/data', atom_style='hybrid',
    atom_substyles=('angle', 'mdpd')
)
