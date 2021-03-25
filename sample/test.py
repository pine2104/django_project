import numpy as np
import time

n= 10000
a = []
t1 = time.time()
for i in range(n):
    a += [1]
t_spent1 = time.time() - t1

print('list '+str(t_spent1) + 's')

b = np.empty(0)
t2 = time.time()
for i in range(n):
    np.append(b,i)
t_spent2 = time.time() - t2

print('np_array '+str(t_spent2) + 's')

