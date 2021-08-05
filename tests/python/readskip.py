file  = 'test.txt'


def skip(f, n):
    for _ in range(n):
        a = f.readline()
        print(a+'---')

with open(file, 'r') as f:

    for line in f:
        print(line)

        if line.find('skip2') >=0 :
            skip(f, 2)
