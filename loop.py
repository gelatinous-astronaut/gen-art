import numpy as np 
import matplotlib.pyplot as plt 

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
grid = np.mgrid[1:2000,1:2000].astype(float)/100 - 10 
# grid = np.mgrid[1:500,1:500].astype(np.float)/25 - 10 
x = grid[0]
y = grid[1]

if (0.0 in x) or (0.0 in y):
	zeros = np.where(x==0.0)[0][0]; x[zeros] = x[zeros] + 0.0001; y[zeros] = y[zeros] + 0.0001

#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

# nums = np.append(np.round(np.linspace(0.01,1,100),2), np.sort(np.round(np.linspace(0.01,1,100),2))[::-1])
# nums = np.append(np.linspace(1,99,99))

nums = np.append(np.round(np.logspace(-3,np.log10(0.5),100),2),np.sort(np.round(np.logspace(-3,np.log10(0.5),100),2))[::-1])
print(nums)

# for i in range(len(nums)):
# 	x1 = x*nums[i]
# 	z = np.sin(x1*y) + np.cos(y/x1)

# 	# plt.clf()

# 	# Get current size
# 	fig_size = plt.rcParams["figure.figsize"]
	 
# 	# Prints: [8.0, 6.0]
# 	print("Current size:", fig_size)
	 
# 	# Set figure width to 12 and height to 9
# 	fig_size[0] = 16
# 	fig_size[1] = 9
# 	plt.rcParams["figure.figsize"] = fig_size


# 	sc = plt.scatter(x1,y,vmin=np.amin(z),vmax=1.1*np.amax(z),c=z,
# 		cmap=plt.get_cmap('nipy_spectral'),edgecolors='none',s=10)

# 	ad = (4-len(str(i)))*'0'
# 	imnum = ad+str(i)

# 	# plt.axis('off')
# 	# plt.savefig('/home/ethan/code/visualizations/images/loop2/img'+imnum+'.png',format='png',dpi=300)
# 	# plt.savefig('test.png',bbox_inches='tight')
# 	plt.show()

# 	print(imnum)



