import numpy as np 
import matplotlib.pyplot as plt 

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
grid = np.mgrid[1:1000,1:1000].astype(np.float)/1000 
# grid = np.mgrid[1:500,1:500].astype(np.float)/25 - 10 
x = grid[0]
y = grid[1]

if (0.0 in x) or (0.0 in y):
	xzeros = np.where(x==0.0)[0][0]; x[xzeros] = x[xzeros] + 0.0001 
	yzeros = np.where(y==0.0)[0][0]; y[yzeros] = y[yzeros] + 0.0001

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------


H0G = 0.07175 # units of 1/Gyr

z = 2. / (3.*H0G*(np.sqrt(x)))*np.arcsinh( np.sqrt(x/y)*(1**(1.5)) )

plt.clf()

sc = plt.scatter(x,y,vmin=np.amin(z),vmax=1.1*np.amax(z),c=z,
	cmap=plt.cm.get_cmap('viridis'),edgecolors='none',s=10)



plt.axis('off')
# plt.savefig('/home/ethan/code/visualizations/time.png',format='png',dpi=300)
# plt.savefig('test.png',bbox_inches='tight')
plt.show()
