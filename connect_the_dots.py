import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
import os,re
from scipy.stats import multivariate_normal

save_dir = '/Users/ethan/code/doodles'
os.makedirs(save_dir, exist_ok=True)

CMAPS = ['viridis','inferno','binary','spring','summer','autumn','winter','ocean',
	'gist_earth','terrain','gnuplot','gnuplot2','cubehelix','gist_rainbow','twilight']

def get_next_filename(directory=save_dir, base_name="ctd_"):
	pattern = re.compile(rf"{re.escape(base_name)}(\d+)")
	files = os.listdir(directory)
	numbers = [int(pattern.match(f).group(1)) for f in files if pattern.match(f)]
	next_number = max(numbers) + 1 if numbers else 1
	return os.path.join(directory, f"{base_name}{next_number}.png")






if __name__ == '__main__':
	# set up plotting surface
	plt.style.use('dark_background')
	fig,ax = plt.subplots(figsize=(10,10))

	draw_blur(ax,np.random.choice(CMAPS))
	draw_circle(ax,20,'orange')

	ax.set_xlim(0,1)
	ax.set_ylim(0,1)
	ax.set_axis_off()
	plt.tight_layout()
	plt.show()

	# prompt to save or not save the doodle
	yn = input('save figure, y/[n]? ')
	if yn=='y':
		# filename = get_next_filename()
		print('saving figure: ' + get_next_filename())
		fig.savefig(get_next_filename(),format='png',dpi=300,bbox_inches='tight')
	else:
		print('figure not saved')