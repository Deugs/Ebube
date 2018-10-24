
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import sys

header = sys.path[0]+'/'

f = open(header+'line.txt', 'r')
raw = str(f.read())


def preprocess(data):
    data = str(data)
    res = data.replace('[','')
    res = res.replace(']', '')
    res = res.replace(' ', '')
    res = res.split('\n')
    bin = []
    [bin.append(float(i)) for i in res]
    
    
    return bin

def f(x, M, C):
    return M*x + C


y = preprocess(raw)
x = range(len(y))
x = X = np.linspace(0, 1000, 100)

plt.figure(1)
plt.scatter(x,y)
plt.hold(True)



M,C = curve_fit(f, x, y)[0]

print str(M) +' '+str(C)

Y = (M*x) + C
plt.plot(x,Y,'r-')

plt.show()


