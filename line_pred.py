
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import sys

header = sys.path[0]+'/'

def write_file(data):
    """save a line data to line.txt in source folder"""
    f = open(header+'line.txt', 'w')
    f.write(str(data))
    f.close()

def read_file(name='line.txt'):
    """read a file form source folder"""
    f = open(header+name, 'r')
    raw =  str(f.read())
    f.close()
    return raw

def gen_line_data(m = -2, c = 0, mean = 0, std = 0.4, num_samples = 100):
    """return line data"""
    noise = np.random.normal(mean, std, size=num_samples)
    X = np.linspace(0, 10, num_samples)
    Y = (m*X) + c + noise
    return Y.reshape(num_samples,1)

def gen_sine_data(f = 2, mean = 0, std = 0.4, num_samples = 100 ):
    """return sine data"""
    noise = np.random.normal(mean, std, size=num_samples)
    t = np.linspace(0, 2, num_samples)
    y = np.sin(2*np.pi*f*t) + noise
    return np.hstack((t.reshape(num_samples,1),y.reshape(num_samples,1)))

def preprocess_str(data_str):
    """return a list of Y data from read file"""
    data = str(data_str)
    res = data.replace('[','')
    res = res.replace(']', '')
    res = res.replace(' ', '')
    res = res.split('\n')
    bin = []
    [bin.append(float(i)) for i in res]

    return bin

def preprocess_list(data):
    bin = []
    [bin.append(float(i[0])) for i in data]
    
    return bin

def line(x, M, C):
    """line equation for fitting"""
    return M*x + C

#y = preprocess_str(read_file())


#y = preprocess_str(read_file())

y = preprocess_list(gen_line_data())
print y
x = range(len(y))
x = X = np.linspace(-100, 1100, 100)

plt.figure(1)
plt.scatter(x,y)
plt.hold(True)

M,C = curve_fit(line, x, y)[0]

print str(M) +' '+str(C)

Y = (M*x) + C
plt.plot(x,Y,'r-')

plt.show()


