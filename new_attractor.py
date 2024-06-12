import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage import gaussian_filter
import numpy as np
import time, os, sys
from numba import njit
import pdb

@njit(parallel=True)                                
def attractor(x,y,num_steps,a,b,c,d):
    
    for i in range(1,int(num_steps)):
        x[i] = np.sin(a*y[i-1]) - np.cos(b*x[i-1])
        y[i] = np.sin(c*x[i-1]) - np.cos(d*y[i-1]) 
    
    return x,y


def plot(size):

	plt.clf()
	fig, ax = plt.subplots()
	# plt.rc('text', usetex=True)
	plt.rc('font', family='serif', size=9)

	x = np.zeros(int(size))
	y = np.zeros(int(size))

	x[0]=0.5
	y[0]=0.5

	a = np.random.uniform(-5,5)                 
	b = np.random.uniform(-5,5)
	c = np.random.uniform(-5,5)
	d = np.random.uniform(-5,5)

	x,y = attractor(x,y,size,a,b,c,d)

	ax.plot(x,y,',')
	ax.set_xscale('log')
	ax.set_yscale('log')

	plt.show()

# ------------
plot(1.e6)



         