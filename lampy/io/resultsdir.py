import os
import sys

cwd = os.getcwd()

# if not os.path.isdir(cwd+'/results'):
#   os.mkdir(cwd+'/results')


def make_dir(_name, _number_from):
    dir = '/' + f'{_number_from}'
    i = _number_from
    while os.path.isdir(cwd + '/'+ _name + dir):
      dir = '/' + str(i)
      i+=1

    results_path = cwd +'/' + _name + dir
    os.mkdir(results_path)
    return results_path

def save_files(_name, _info, _number_from=1):

    _path = make_dir(_name, _number_from)

    from datetime import datetime
    date = datetime.now().strftime("%d-%m-%Y")
    _file1 = open('/'.join((_path,'info.txt')), 'w+')
    _file1.write('date:{}\n'.format(date))
    for data in _info.items():
        _file1.write(f'{data[0]}:{data[1]}\n')
    _file1.close()
    
    print(_path)
    return _path



if __name__ == '__main__':
    name = 'test'
    make_dir(name)
    results_path = rt_save.make_dir(sim_case)
