from ovito.io import *
from ovito.modifiers import *




dir = '/home/luishcc/hdd/free_thread_results/R6_ratio6_A50-4/'
file = 'thread.lammpstrj'

pipeline = import_file(dir+file)

clt_mod = ClusterAnalysisModifier(cutoff = 0.8,
                                  compute_gyration = True,
                                  sort_by_size = True)

pipeline.modifiers.append(clt_mod)

for i in range(50, 100):
    data = pipeline.compute(i)
    cluster_table = data.tables['clusters']
    print(i)
    a = cluster_table['Radius of Gyration'][...]
    print(cluster_table['Radius of Gyration'][...])
    print(cluster_table['Cluster Size'][...])
    print()

# export_file(pipeline, f'{i}.dat', 'txt/table', key='clusters')
