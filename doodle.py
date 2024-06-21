#dumb_walk.py

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
import os,re
from scipy.stats import multivariate_normal

# set up directories to save images
save_dir = '/Users/ethan/code/doodles'
os.makedirs(save_dir, exist_ok=True)

CMAPS = ['viridis','inferno','binary','spring','summer','autumn','winter','ocean',
	'gist_earth','terrain','gnuplot','gnuplot2','cubehelix','gist_rainbow','twilight']

# how to choose proportion of shapes:
# 
#	  decider
# 0      v                                 1
# |		      |                |           |
# |~squiggles~|~~~~~lines~~~~~~|~~markers~~|
# |           |                |           |
#             S                L

S = 0.05 # threshold for squiggles
L = 0.1 # threshold for lines

auto_window = True    # randomly pull window size from normal distribution
window = 0

num_doodles = 100 # how many lines to draw

# read image files to get next file name
def get_next_filename(directory, base_name="doodle_"):
	pattern = re.compile(rf"{re.escape(base_name)}(\d+)")
	files = os.listdir(directory)
	numbers = [int(pattern.match(f).group(1)) for f in files if pattern.match(f)]
	next_number = max(numbers) + 1 if numbers else 1
	return os.path.join(directory, f"{base_name}{next_number}.png")

def draw_squiggle(ax,window,color):
	# print('drawing squiggle')
	# set up parameters
	max_steps   = 2000   # max number of steps for a line
	step_length = 0.005   # how long should each step be
	doRandNeg   = True    # randomly decide if angle is pos or neg
	theta       = 0       # initial angle

	# drift controls window - expand or contract window
	# bug: if drift is > 1.000 then it breaks and draws straight lines
	# drift = np.random.choice([1.01, 1.00])
	# drift = 0.995 # theoretically should unravel line if less than 1
	drift = 1

	# intialize coordinates
	start_point = np.random.random(size=2)
	cur_point = start_point
	path = start_point
	count = 0

	# determine window size
	if auto_window : window = np.random.normal(loc=0.3,scale=0.2)
	else :			 window = window

	# draw new points within the image boundary or below max steps
	while (cur_point[0] < 1) and (cur_point[1] < 1) and (count < max_steps):
		if doRandNeg: sign = np.random.choice([-1, 1])
		else: 		  sign = 1

		# new_window = window
		new_window = np.random.normal(loc=window,scale=0.001) #if scale is too high it just makes tight squiggles

		theta = theta + np.random.random() * new_window * np.pi * sign
		window = new_window*drift

		cur_point = cur_point + np.array([step_length*np.cos(theta), step_length*np.sin(theta)])
		path = np.vstack((path,cur_point))
		count += 1

	# randomly pick line width
	lw = np.random.choice([1,1,1.1,1.2,1.5,2,4])#,8,16])
	ax.plot(path[:,0],path[:,1],'-',lw=lw,color=color)

def draw_line(ax,color):
	# print('drawing line')
	start_point = np.random.random(size=2)
	end_point =  np.random.random(size=2)
	path = np.vstack((start_point,end_point))

	# randomly pick line width
	lw = np.random.choice([1,1,1.1,1.2,1.5,2,4])#,8,16])
	ax.plot(path[:,0],path[:,1],'-',lw=lw,color=color)

def draw_marker(ax,color):

	# randomly decide to fill or not fill marker
	if (np.random.random() < 1.0) : mfc = color 
	else : 							mfc = 'none'

	# choose marker style and rotate
	m     = np.random.choice(['1','2','3','4','s','p','P','*','h','H','+','x','D','d','$f(x)$']) # matplotlib shape codes
	lw    = np.random.choice([1,1,1.1,1.2,1.5,2,4])#,8,16]) # line width
	ms    = np.random.random()*200 # marker size
	pos   = np.random.random(size=2) # position
	alpha = np.random.random() # transparency
	angle = np.random.random()*360
	t = mpl.markers.MarkerStyle(marker=m)
	t._transform = t.get_transform().rotate_deg(angle)
	
	ax.plot(pos[0], pos[1], marker=t, ms=ms, mfc=mfc, mec=color, mew=lw, alpha=alpha)

def draw_blur(ax,cmap):
	# parameters for multivariate norm
	mean = np.random.random(size=2)
	a = np.abs(np.random.normal(loc=0.03,scale=0.05))
	b = np.abs(np.random.normal(loc=0.03,scale=0.05))
	covariance = [[a, 0], [0, b]]

	# choose resolution and create grid
	res = np.random.randint(30,1000) 
	x = np.linspace(-1, 1, res)
	y = np.linspace(-1, 1, res)
	x, y = np.meshgrid(x, y)
	pos = np.dstack((x, y))

	# generate, normalize, add noise, display 
	z =  multivariate_normal(mean, covariance).pdf(pos)
	z = z / np.amax(z)
	z += np.random.random((res,res)) / np.random.randint(1,10)
	ax.pcolormesh(x, y, z, cmap=cmap, shading='auto',alpha=np.random.random())


if __name__ == '__main__':
	# set up plotting surface
	plt.style.use('dark_background')
	fig,ax = plt.subplots(figsize=(10,10))

	# draw background
	draw_blur(ax,np.random.choice(CMAPS))

	# determine colorscheme for doodles
	colormap = plt.get_cmap(np.random.choice(CMAPS))


	if not(auto_window):
		window = float(input('enter multiple of pi for angle decision: '))

	for n in np.arange(num_doodles):
		this_color = colormap(n/num_doodles,1) # other colormaps: viridis, cubehelix
		# shape = np.random.choice(['line', 'squiggle', 'marker'])
		
		decider = np.random.random()
		if   (decider <= squiggle_val) : draw_squiggle(ax,window,this_color)
		elif (decider > line_val) : 	 draw_marker(ax,this_color)
		else:							 draw_line(ax,this_color) 

	ax.set_xlim(0,1)
	ax.set_ylim(0,1)
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

