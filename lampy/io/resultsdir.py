import os
import sys

cwd = os.getcwd()

# if not os.path.isdir(cwd+'/results'):
#   os.mkdir(cwd+'/results')


def make_dir(_name):
    dir = '/' + _name + '-0'
    i = 1
    while os.path.isdir(cwd + dir):
      dir = dir.split('-')[0] + '-'+str(i)
      i+=1

    results_path = cwd + dir
    os.mkdir(results_path)
    return results_path

def sim_info_files(_name, _info):

    _path = make_dir(_name)

    from datetime import datetime
    date = datetime.now().strftime("%d-%m-%Y")
    _file1 = open('/'.join((_path,'info.txt')), 'w+')
    _file1.write('date:{}\n'.format(date))
    for data in _info.items():
        _file1.write('{}:{}\n'.format(data[0], data[1]))
    _file1.close()

    return _path.split('/')[-1]



if __name__ == '__main__':
    name = 'test'
    make_dir(name)
    results_path = rt_save.make_dir(sim_case)
