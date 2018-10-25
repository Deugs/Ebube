
from scipy.optimize import curve_fit
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import numpy as np
import sys


from sklearn.linear_model import BayesianRidge as Lin_regress
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import ARDRegression

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

def gen_line_data(m = 5, c = 0, mean = 0, std = 0.4, num_samples = 100):
    """return line data"""
    noise = np.random.normal(mean, std, size=num_samples)
    X = np.linspace(0, 10, num_samples)
    Y = (m*X) + c + noise
    return Y.reshape(num_samples,1)

def gen_sine_data(f = 1.7, mean = 0, std = 0.1, num_samples = 1000 ):
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
    bn = []
    [bn.append(float(i)) for i in res]

    return bn

def preprocess_list_line(data):
    """return a list of Y data from generated data"""
    bn = []
    [bn.append(float(i[0])) for i in data]
    
    return bn

def preprocess_list_sine(data):
    """return a list of Y data from generated data"""
    bn = []
    lin = []
    [bn.append(float(i[0])) for i in data]
    [lin.append(float(i[1])) for i in data]
    
    return [bn, lin]

def line(x, M, C):
    """line equation for fitting"""
    return M*x + C

def sine(t, f):
    """line equation for fitting"""
    return np.sin(2*np.pi*f*t)

def predict_line(std = 0.8):
    #y = preprocess_str(read_file())
    y = preprocess_list_line(gen_line_data(std=std))
    n = len(y)
    x = np.linspace(0, 10, n)
    
    plt.figure(1)
    #plt.axis([0, 100, 0, 100])
    plt.scatter(x,y)
    plt.hold(True)
    
    M,C = train_regressor(x, y)
    print 'regression: '+str(M) +' '+str(C)
    
    Y = line(x, M, C)
    plt.plot(x,Y,'gs')
    
    M,C = curve_fit(line, x, y)[0]
    
    print 'curve_fit: '+str(M) +' '+str(C)
    
    Y = line(x, M, C)
    plt.plot(x,Y,'r-')
    
    plt.show()

def predict_sine(std = 0.0):
    #y = preprocess_str(read_file())
    x,y = preprocess_list_sine(gen_sine_data(std=std))

    plt.plot(x, y)
    plt.hold(True)
    
    f = curve_fit(sine, x, y)[0]
    
    print f
    
    Y = sine(x, f)
    plt.plot(x,Y,'r-')
    
    plt.show()

def train_regressor(xx, yy):

    X = []
    d = np.array(xx)
    y = np.array(yy)
    [X.append([i]) for i in d]
    y.reshape(len(y),)
    
    linearR = Lin_regress()

    reg0 = LinearRegression()
    reg1 = BayesianRidge()
    reg2 = RidgeCV()
    reg3 = ElasticNet()
    reg6 = ARDRegression()

    regresors = [reg0,reg1,reg2,reg3,reg6]

    predictor = []
    coef = []
    intercept = []
    for reg in regresors:
        predictor.append(reg.fit(X,y))
        #print reg.intercept_
        coef.append(reg.coef_[0])
        intercept.append(reg.intercept_)
        
    
        
    gradient = np.average(coef)
    intercept = np.average(intercept)
    
    print 'regression_avg: '+str(gradient)+' ' +str(intercept)
    mod = linearR.fit(X,y)
    return mod.coef_[0], mod.intercept_
    
def predict_fft():
    N = 1000# Number of sample points
    
    T = 1.0 / 800.0#sampling Time
    x = np.linspace(0.0, N*T, N)
    y = 2*np.sin(50.0 * 2.0*np.pi*x) + np.random.normal(0, 2, size=N)
    yff = fft(y)
    xff = np.linspace(0.0, 1.0/(2.0*T), N//2)
    
    p = list(yff)
    print xff[p.index(max(p))]
    
    plt.plot(xff, 2.0/N * np.abs(yff[0:N//2]))
    
    plt.show()  

#predict_line()
predict_fft()





