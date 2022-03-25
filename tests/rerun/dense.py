import numpy as np


def reading_snap(file):
    line = file.readline().split()
    density = 0
    num = int(line[1])
    for _ in range(num):
        line = file.readline().split()
        density += float(line[-1])
    return density / num

with open('den.txt', 'r') as file:
    file.readline()
    file.readline()
    file.readline()
    while True:
        try:
            print(reading_snap(file))
        except Exception as e:
            print(e)
            break
