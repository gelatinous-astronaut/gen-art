#dumb_walk.py

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm

num_walks = 10
fig,ax = plt.subplots(figsize=(5,5))

for i in np.arange(num_walks):
	norm = np.random.normal(size=1000)
	y = np.linspace(0,1,1000)

	position = 0
	x = np.array([])

	for n in norm:
		position += n
		x = np.append(x,position)

	this_color = cm.plasma(i/num_walks,1)

	ax.plot(x,y,color=this_color,lw=1)

plt.show()
