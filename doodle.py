import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
import os,re, sys
from scipy.stats import multivariate_normal
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon
from scipy.interpolate import splprep, splev
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

# set up directories to save images
save_dir = '/Users/ethan/code/doodles'
os.makedirs(save_dir, exist_ok=True)

CMAPS = ['viridis','inferno','binary','spring','summer','autumn','winter','ocean',
	'gist_earth','terrain','gnuplot','gnuplot2','cubehelix','gist_rainbow','twilight']

S = 0.5 # fraction of squiggles = S = 0.05
L = 0  # fraction of lines   = L-S = 0.05
#          fraction of markers = 1-L = 0.9

AUTO_WINDOW = False # randomly pull window size from normal distribution
NUM_DOODLES = 25 # how many doodles to draw

# read image files to get next file name
def get_next_filename(directory=save_dir, base_name="doodle_"):
	pattern = re.compile(rf"{re.escape(base_name)}(\d+)")
	files = os.listdir(directory)
	numbers = [int(pattern.match(f).group(1)) for f in files if pattern.match(f)]
	next_number = max(numbers) + 1 if numbers else 1
	return os.path.join(directory, f"{base_name}{next_number}.png")

def connect_all_points(ax,points,cmap='none',z=1):
	# can pass a color name to cmap to fix it to one color as well
	xs = points[:,0]
	ys = points[:,1]
	if cmap == 'none':
		colormap = plt.get_cmap(np.random.choice(CMAPS))
	elif cmap in CMAPS:
		colormap = plt.get_cmap(cmap)

	num = points.shape[0]
	w=2
	for i in np.arange(num):
		if cmap=='none': 
			this_color = colormap(i/num,1)
		else: 
			this_color = cmap
		for j in np.arange(i+1,num):
			if np.random.random() < 0: continue
			this_line = np.array([ [xs[i],ys[i]], [xs[j],ys[j]] ])
			ax.plot(this_line[:,0],this_line[:,1],'-',color=this_color,lw=0.5*w,alpha=0.7,zorder=z)

def connect_outer_points(ax,points,color='k',z=1):
	hull = ConvexHull(points)
	for simplex in hull.simplices:
		plt.plot(points[simplex, 0], points[simplex, 1], '-', color=color)

def draw_squiggle(ax,color):
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

	# determine window size
	if AUTO_WINDOW : window = np.random.normal(loc=0.3,scale=0.2)
	else :			 window = 1

	# intialize coordinates
	cur_point = np.random.random(size=2)
	path = cur_point
	count = 0

	# draw new points within the image boundary or below max steps
	while (cur_point[0] < 1) and (cur_point[1] < 1) and (count < max_steps):
		if doRandNeg: sign = np.random.choice([-1, 1])
		else: 		  sign = 1

		# new_window = window
		new_window = np.random.normal(loc=window,scale=0.001) #if scale is too high it just makes tight squiggles

		# nudge angle within window
		theta = theta + np.random.random() * new_window * np.pi * sign
		window = new_window*drift

		# step forward along path
		cur_point = cur_point + np.array([step_length*np.cos(theta), step_length*np.sin(theta)])
		path = np.vstack((path,cur_point))
		count += 1

	# randomly pick line width
	lw = np.random.choice([1,1,1.1,1.2,1.5])#,2,4]),8,16])
	ax.plot(path[:,0],path[:,1],'-',lw=lw,color=color)

def draw_line(ax,color):
	# randomly pick line width
	lw = np.random.choice([1,1,1.1,1.2,1.5,2,4])#,8,16])
	ax.plot(np.random.random(size=2),np.random.random(size=2),'-',lw=lw,color=color)

def draw_marker(ax,color):
	# randomly decide to fill or not fill marker
	if (np.random.random() < 0.3) : mfc = color 
	else : 							mfc = 'none'

	# choose marker style and rotate
	m     = np.random.choice(['1','2','3','4','s','p','P','*','h','H','+','x','D','d'])#,'$f(x)$']) # matplotlib shape codes
	lw    = np.random.choice([1,1,1.1,1.2,1.5,2,4])#,8,16]) # line width
	ms    = np.random.random()*200 # marker size
	pos   = np.random.random(size=2) # position
	alpha = np.random.random()*0.6 # transparency
	angle = np.random.random()#*360
	t = mpl.markers.MarkerStyle(marker=m)
	t._transform = t.get_transform().rotate_deg(angle)
	
	ax.plot(pos[0], pos[1], marker=t, ms=ms, mfc=mfc, mec=color, mew=lw, alpha=alpha)

def draw_blur(ax,cmap,res=1000,random=True):
	# parameters for multivariate norm
	if random:
		mean = np.random.random(size=2)
		a = np.abs(np.random.normal(loc=0.05,scale=0.05))
		b = np.abs(np.random.normal(loc=0.05,scale=0.05))
		alpha = 0.3#np.random.random()
		res = np.random.randint(60,1000) 
	else:
		mean = np.array([0.5,0.5])
		a = 0.1
		b = 0.1
		alpha = 0.6
	covariance = [[a, 0], 
				  [0, b]]

	# choose resolution and create grid
	x = np.linspace(-1, 1, res)
	y = np.linspace(-1, 1, res)
	x, y = np.meshgrid(x, y)
	pos = np.dstack((x, y))

	# generate, normalize, add noise, display 
	z =  multivariate_normal(mean, covariance).pdf(pos)
	z = z / np.amax(z)
	z += np.random.random((res,res)) / np.random.randint(2,10)
	ax.pcolormesh(x, y, z, cmap=cmap, shading='auto',alpha=alpha)

def draw_network(ax, num, cmap):
	colormap = plt.get_cmap(cmap)
	points = np.random.random((num,2))

	x_shift = np.random.random() * 0.5 #- 0.5
	x_width = np.random.random() * 1
	xs = np.random.random(num)*x_width + x_shift#*np.random.choice([-1,1])
	xs = xs/np.amax(xs)

	y_shift = np.random.random() * 0.5 #- 0.5
	y_width = np.random.random() * 1
	ys = np.random.random(num)*y_width + y_shift#*np.random.choice([-1,1])
	ys = ys/np.amax(ys)

	w = 1
	for i in np.arange(num):
		this_color = colormap(i/num,1)
		ax.plot(xs[i],ys[i],'o',mew=0,mfc=this_color,ms=2*w)
		for j in np.arange(i+1,num):
			if np.random.random() < 0.6:
				continue
			# these_points = np.vstack((points[i],points[j]))
			these_points = np.array([ [xs[i],ys[i]],
									  [xs[j],ys[j]]  ])

			ax.plot(these_points[:,0],these_points[:,1],'-',color=this_color,lw=1*w,alpha=0.7)

def draw_point_circle(ax,num,r=0.1,color='orange',center=[0.5,0.5]):
	theta = np.linspace(0,2*np.pi,num+1)#*(0.95+np.random.random(num)/10)
	x = r*np.cos(theta) + center[0]
	y = r*np.sin(theta) + center[1]

	ax.plot(x,y,'o',mew=0,mfc=color,ms=4)
	points = np.vstack((x,y)).T
	connect_all_points(ax,points,cmap=color)

def draw_polygon(ax,color,sides=3,z=1):
	# generate points
	vertices = np.random.random((sides,2))
	vertices = np.append(vertices, [vertices[0]], axis=0)
	polygon = Polygon(vertices, closed=True, facecolor=color, edgecolor='none', alpha=0.5)
	ax.add_patch(polygon)

	# plot and connect points
	# ax.plot(vertices[:,0],vertices[:,1],'o',ms=4,mew=0,mfc=color,zorder=z)
	# ax.plot(vertices[:, 0], vertices[:, 1], color=color, zorder=z)

	# hull = ConvexHull(vertices)
	# ordered_vertices = vertices[hull.vertices]
	# ax.fill(ordered_vertices[:, 0], ordered_vertices[:, 1], color=color, alpha=0.5, zorder=z)
	# for simplex in hull.simplices:
	# 	plt.plot(vertices[simplex, 0], vertices[simplex, 1], '-', color=color)

def draw_spline(ax,cmap,num,z=1):
	# generate points
	x = np.random.random(num)
	y = np.random.random(num)

	# Parameterize the data and create segmented spline 
	tck, u = splprep([x, y], s=0)
	unew = np.linspace(0, 1, 3000)
	out = splev(unew, tck)
	points = np.array([out[0], out[1]]).T.reshape(-1, 1, 2)
	segments = np.concatenate([points[:-1], points[1:]], axis=1)

	# initialize line collection
	colormap = plt.get_cmap(cmap)
	norm = plt.Normalize(unew.min(), unew.max())
	lc = LineCollection(segments, cmap=colormap, norm=norm)
	lc.set_array(unew)

	# parametrize line width
	t = np.linspace(0,8*np.pi,len(segments))
	# lw_func = 16*np.sin(t)*np.sin(15*t)
	# lw_func = np.e**(t/4.)*(np.sin(4*t)+0.25)
	T = 0.1 + t/15.
	lw_func = np.e**(t/4.)*np.sin(2*np.pi*t/T)
	lc.set_linewidths(lw_func)

	# set opacity and plot
	lc.set_alpha(0.5)
	ax.add_collection(lc)

	


if __name__ == '__main__':
	# set up plotting surface
	plt.style.use('dark_background')
	fig,ax = plt.subplots(figsize=(6,10))
	colormap = plt.get_cmap(np.random.choice(CMAPS))

	# draw background
	cmap = np.random.choice(CMAPS)
	# cmap = 'binary'
	# draw_blur(ax,cmap, res=200,random=False)

	# test drawing functions 
	# draw_network(ax,20,np.random.choice(CMAPS))

	# colormap = plt.get_cmap('gnuplot')
	# np.random.randint(100,500)

	for i in np.arange(3):
		draw_blur(ax,cmap=np.random.choice(CMAPS), res=100,random=True)

	# r = 0.1
	# draw_point_circle(ax,num=1,r=r,color=colormap(1/9,1),center=[0.2,0.8])
	# draw_point_circle(ax,num=2,r=r,color=colormap(2/9,1),center=[0.5,0.8])
	# draw_point_circle(ax,num=3,r=r,color=colormap(3/9,1),center=[0.8,0.8])

	# draw_point_circle(ax,num=4,r=r,color=colormap(4/9,1),center=[0.2,0.5])
	# draw_point_circle(ax,num=5,r=r,color=colormap(5/9,1),center=[0.5,0.5])
	# draw_point_circle(ax,num=6,r=r,color=colormap(6/9,1),center=[0.8,0.5])

	# draw_point_circle(ax,num=7,r=r,color=colormap(7/9,1),center=[0.2,0.2])
	# draw_point_circle(ax,num=8,r=r,color=colormap(8/9,1),center=[0.5,0.2])
	# draw_point_circle(ax,num=9,r=r,color=colormap(9/9,1),center=[0.8,0.2])

	# draw_point_circle(ax,num=10,r=0.08,color='white',center=[0.9,0.7])


	num_poly = 6
	for n in np.arange(num_poly):
		# sides = np.random.randint(3,20) 
		sides = 3
		this_color = colormap((n+1)/(num_poly+1),1)
		draw_polygon(ax,this_color,sides=sides,z=10**n)
	

	draw_spline(ax,num=15,cmap=np.random.choice(CMAPS))


	# determine colorscheme for doodles
	colormap = plt.get_cmap(np.random.choice(CMAPS))
	# draw doodles
	for n in np.arange(NUM_DOODLES):
		this_color = colormap(n/NUM_DOODLES,1) # other colormaps: viridis, cubehelix
		decider = np.random.random()
		if   (decider <= S) : draw_squiggle(ax,this_color)
		elif (decider > L)  : draw_marker(ax,this_color)
		else : 				  draw_line(ax,this_color) 

	# set bounds and display
	ax.set_xlim(0,1)
	ax.set_ylim(0,1)
	ax.set_axis_off()
	plt.tight_layout()
	plt.show()

	# prompt to save or not save the doodle
	yn = input('save figure, y/[n]? ')
	while not(yn in ['y','n','Y','N','0','1','']):
		yn = input('save figure, y/[n]? ')

	if yn in ['y','Y','1']:
		print('saving figure: ' + get_next_filename())
		fig.savefig(get_next_filename(),format='png',dpi=300,bbox_inches='tight')
	elif yn in ['n','N','0','']:
		print('figure not saved')

