import os, sys
import datetime
import imageio
from pprint import pprint
import time
import datetime

e = sys.exit
#
# R = 6
# ratio = 12
# sim_case = f'R{R}_ratio{ratio}_A50'

path_to_data = os.getcwd()
newdir = '/'.join([path_to_data, 'f2'])

cwd = os.getcwd()
os.chdir(newdir)

def create_gif(filenames, duration):
    images = []

    for filename in filenames:
        images.append(imageio.imread(filename))
    output_file = 'Gif-%s.gif' % datetime.datetime.now().strftime('%Y-%M-%d-%H-%M-%S')
    os.chdir(cwd)
    imageio.mimsave(output_file, images, duration=duration)

if __name__ == "__main__":
    script = sys.argv.pop(0)
    duration = 0.06
    filenames = sorted(filter(os.path.isfile, [x for x in os.listdir(newdir) if x.endswith(".png")]),
                            key=lambda p: os.path.exists(p) and os.stat(p).st_mtime or
                                      time.mktime(datetime.now().timetuple()))

    create_gif(filenames, duration)
