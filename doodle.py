#dumb_walk.py

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os,re

# set up directories to save images
save_dir = os.getcwd()+'/doodles'
os.makedirs(save_dir, exist_ok=True)

# read image files to get next file name
def get_next_filename(directory, base_name="doodle_"):
	pattern = re.compile(rf"{re.escape(base_name)}(\d+)")
	files = os.listdir(directory)
	numbers = [int(pattern.match(f).group(1)) for f in files if pattern.match(f)]
	next_number = max(numbers) + 1 if numbers else 1
	return os.path.join(directory, f"{base_name}{next_number}.png")

# set up parameters
num_walks   = 20      # how many lines to draw
max_steps   = 20000   # max number of steps for a line
step_length = 0.005   # how long should each step be
autofrac    = False    # randomly pull direction from normal distribution
doRandNeg   = True    # randomly decide if angle is pos or neg
theta       = 0       # initial angle

# set up plotting surface
plt.style.use('dark_background')
fig,ax = plt.subplots(figsize=(10,10))

# frac sets the width of the angle window available
# 		2 means 2pi means full circle --> very twisty lines
# 		low number means narrow window --> straight-ish lines
if autofrac:
	frac = np.random.normal(loc=0.5,scale=0.1)
else:
	frac = float(input('enter multiple of pi for angle decision: '))

# loop through lines to draw
for n in np.arange(num_walks):
	if autofrac:
		frac = np.random.normal(loc=0.5,scale=0.1)

	# intialize coordinates
	start_point = np.random.random(size=2)
	cur_point = start_point
	path = start_point
	count = 0

	# controls frac - expand or contract window
	# bug: if drift is > 1.000 then it draws straight lines
	# drift = np.random.choice([1.01, 1.00])
	# drift = 0.995
	drift = 1

	straight_line = (np.random.random() < 0.7)

	if straight_line:
		end_point =  np.random.random(size=2)
		path = np.vstack((path,end_point))

	else:
		# draw new points within the image boundary or below max steps
		while (cur_point[0] < 1) and (cur_point[1] < 1) and (count < max_steps):
			if doRandNeg: sign = np.random.choice([-1, 1])
			else: 		  sign = 1

			# newfrac = frac
			newfrac = np.random.normal(loc=frac,scale=0.01) #if scale is too high it just makes tight squiggles

			theta = theta + np.random.random() * newfrac * np.pi * sign
			frac = newfrac*drift

			d_vec = np.array([step_length*np.cos(theta), step_length*np.sin(theta)])
			cur_point = cur_point + d_vec
			path = np.vstack((path,cur_point))
			count += 1

	# choose line color from colormap
	# other colormaps: viridis, cubehelix
	this_color = cm.jet(n/num_walks,1)


	# randomly pick line width
	lw = np.random.choice([1,1,1.1,1.2,1.5,2,4])#,8,16])

	ax.plot(path[:,0],path[:,1],'-',lw=lw,color=this_color)
	print(count)

ax.set_xlim(0,1)
ax.set_ylim(0,1)
# ax.xaxis.set_visible(False)
# ax.yaxis.set_visible(False)
ax.set_axis_off()

plt.tight_layout()
plt.show()

yn = input('save figure, y/[n]? ')

if yn=='y':
	filename = get_next_filename(save_dir)
	print('saving figure: '+filename)
	fig.savefig(filename,format='png',dpi=300,bbox_inches='tight')
else:
	print('figure not saved')

