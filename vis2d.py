import numpy as np 
import matplotlib.pyplot as plt 
import pdb

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
type = 'linear'

if type=='log':
	x, y = np.array(np.meshgrid(np.logspace(0,3,1000), np.logspace(0,3,1000)))/50 - 10
	# x, y = np.array(np.meshgrid(np.linspace(1,1000,1000), np.logspace(1,1000,1000)))/50 - 10
elif type=='linear':
	grid = np.mgrid[1:1000,1:1000].astype(np.float)/50 - 10 
	x = grid[0]
	y = grid[1]
else:
	raise ValueError('oops')

# print x.shape; print y.shape

if (0.0 in x) or (0.0 in y):
	zeros = np.where(x==0.0)[0][0]; x[zeros] = x[zeros] + 0.0001; y[zeros] = y[zeros] + 0.0001

x = x*0.05

z = np.sin(x*y) + np.cos(y/x)

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
plt.clf()
# plt.figure(figsize=(9,16))
sc = plt.scatter(x,y,vmin=np.amin(z),vmax=1.1*np.amax(z),c=z,
	cmap=plt.cm.get_cmap('viridis'),edgecolors='none',s=10)

if type=='log':
	plt.xscale('log')
	plt.yscale('log')

plt.axis('off')
plt.savefig('/home/ethan/code/images/f1_zoom.png',format='png',dpi=300)
# plt.show()


#-------------------------------------------------------------------------------------------------
pdb.set_trace()


