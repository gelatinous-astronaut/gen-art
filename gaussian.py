import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage import gaussian_filter
import numpy as np
import time, os, sys
from numba import njit
import pdb
colormap_list       = ['inferno','nipy_spectral','hot','gnuplot2','jet','terrain','gist_ncar','viridis','plasma','magma',
                       'summer','autumn','winter','Wistia','ocean','rainbow','gist_rainbow','hsv','brg']

plt.clf()


image_resolution = [2e3, 2e3]
my_dpi=200

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
mu = np.random.uniform(-1000,1000) 
sigma = np.random.uniform(1,50)

x = np.random.normal(mu, sigma, int(1e5))
y = np.random.normal(mu, sigma, int(1e5))

hist = np.histogram2d(x,y,bins=[image_resolution[1],image_resolution[0]])[0]

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
mu = np.random.uniform(1,5) 
sigma = np.random.uniform(1,5)

x = np.random.normal(mu, sigma, int(1e5))
y = np.random.normal(mu, sigma, int(1e5))

hist += np.histogram2d(x,y,bins=[image_resolution[1],image_resolution[0]])[0]

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
fig_hist = plt.figure(figsize=(image_resolution[0]/my_dpi, image_resolution[1]/my_dpi), dpi=my_dpi,frameon=False)

ax = plt.Axes(fig_hist, [0., 0., 1., 1.])           
ax.set_axis_off()
fig_hist.add_axes(ax)


cm_name = np.random.choice(colormap_list)
cmap = cm.get_cmap(cm_name)
cmap.set_under('black')


hist_final = gaussian_filter(hist,0.5,0)            
ax.imshow(hist_final,cmap=cmap,aspect='equal',vmin=hist.min()+0.00001) 
plt.savefig('test.png')




pdb.set_trace()