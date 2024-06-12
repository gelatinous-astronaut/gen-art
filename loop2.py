import numpy as np 
import matplotlib.pyplot as plt 
import pdb

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
grid = np.mgrid[1:1000,1:1000].astype(np.float)/50 - 10 
x = grid[0]
y = grid[1]

if (0.0 in x) or (0.0 in y):
	zeros = np.where(x==0.0)[0][0]; x[zeros] = x[zeros] + 0.0001; y[zeros] = y[zeros] + 0.0001

# #-------------------------------------------------------------------------------------------------
# #-------------------------------------------------------------------------------------------------
# #-------------------------------------------------------------------------------------------------
# for i in np.round(np.linspace(0.01,1,100),2):
# 	x1 = x*i
# 	z = np.sin(x1*y) + np.cos(y/x1)

# 	plt.clf()
# 	sc = plt.scatter(x1,y,vmin=np.amin(z),vmax=1.1*np.amax(z),c=z,
# 		cmap=plt.cm.get_cmap('viridis'),edgecolors='none',s=10)

# 	imnum = str(int(i*100) - 1)

# 	if len(imnum)<3:
# 		ad = (3-len(imnum))*'0'
# 		imnum = ad+imnum

# 	plt.axis('off')
# 	plt.savefig('/home/ethan/code/images/loop/img'+imnum+'.png',format='png',dpi=300)

# 	print imnum

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
for i in np.sort(np.round(np.linspace(0.01,1,100),2))[::-1]:
	x1 = x*i
	z = np.sin(x1*y) + np.cos(y/x1)

	plt.clf()
	sc = plt.scatter(x1,y,vmin=np.amin(z),vmax=1.1*np.amax(z),c=z,
		cmap=plt.cm.get_cmap('viridis'),edgecolors='none',s=10)

	imnum = str(200 - int(i*100))
	plt.axis('off')
	plt.savefig('/home/ethan/code/images/loop/img'+imnum+'.png',format='png',dpi=300)

	print imnum


#-------------------------------------------------------------------------------------------------
pdb.set_trace()


