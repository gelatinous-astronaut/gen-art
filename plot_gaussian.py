#plot_gaussian.py

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pdb
from scipy.misc import derivative
from scipy.stats import norm
import seaborn as sns


# fig,ax = plt.subplots(figsize=(5,5))

# -- create gaussian data -- 
mu, sigma = 0.5, 0.1
data = np.random.normal(mu, sigma, 1000)
noise_factor = np.random.normal(loc=1,scale=0.15,size=1000)

data = data * noise_factor

sns.histplot(data=data,bins=30,kde=True)

# x = np.linspace(np.amin(data),np.amax(data),len(data))
# y = norm.pdf(x,mu,sigma)
# sns.lineplot(x=x,y=y)

# sns.kdeplot(data)

plt.show()
# hist, bin_edges = np.histogram(s,bins=30,density=True)
# bin_width = bin_edges[1] - bin_edges[0]
# bin_centers = bin_edges[:-1]+bin_width/2


# --- cumulative distribution function ---
# data_ordered = np.sort(data)[::-1]
# count = np.arange(len(data))
# ax.plot(data_ordered,count)
# ax.set_xlabel('value')
# ax.set_ylabel('N > value')
# plt.show()

# ---------------------------------------------------------------


pdb.set_trace()