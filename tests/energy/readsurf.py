file = 'gamma.profile'
sum = 0
n = 0
with open(file, 'r') as fd:
  for i in range(100):
    fd.readline()
  for line in fd:
    l = line.split()
    sum+=float(l[1])
    n+=1
f = sum/n

print(f)
