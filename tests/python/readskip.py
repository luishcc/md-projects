import time
file  = 'test.txt'




def skip(f, n):
    for _ in range(n):
        a = f.readline()
        print('---'+a)



t1 = time.time()
with open(file, 'r') as f:

    for line in f:
        print(line)

        if line.find('skip2') >=0 :
            skip(f, 2)

t2 = time.time()

with open(file, 'r') as f:
    line = f.readline().split()[1:]
    print(line)
    for id, line in enumerate(f):
        print(line)

        if line.find('skip2') >=0 :
            skip(f, 1)

t3 = time.time()

print(t2-t1)
print(t3-t2)
