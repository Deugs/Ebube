import numpy as np
import sys
import matplotlib.pyplot as plt

header = sys.path[0]+'/'

mean = 0
std = 0.4 
num_samples = 100

noise = np.random.normal(mean, std, size=num_samples)

X = np.linspace(0, 1000, num_samples)
Y = (2*X) + 2 + 40*noise
data_line = Y.reshape(num_samples,1)

plt.figure(1)
plt.scatter(X,Y)



t = np.linspace(0, 2, num_samples)
y = np.sin(2*np.pi*2*t) + noise
data_sig = np.hstack((t.reshape(num_samples,1),y.reshape(num_samples,1)))

plt.figure(2)
plt.scatter(t,y)

#plt.show()

f = open(header+'line.txt', 'w')
f.write(str(data_line))
f.close()

f = open(header+'sine.txt', 'w')
f.write(str(data_sig))
f.close()
