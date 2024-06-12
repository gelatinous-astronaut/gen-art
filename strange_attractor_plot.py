import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage import gaussian_filter
import numpy as np
import time, os, sys
from numba import njit

start_time = time.time()
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

'''
This code creates pretty pictures of Peter de Jong attractors (http://paulbourke.net/fractals/peterdejong/). 
It's an iterative sequence, which means that each value in the sequence depends on the one before it. 
So it's a relatively inefficient calculation, and requires some big for-loops. This program works by taking a 
specified number of timesteps, and breaking it up into "chunks" of a certain size, which it then calculates 
individually so your computer doesn't run out of RAM doing one single, massive calculation.
'''


#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
# image_resolution = [1920,1080]         #A standard 1080p monitor
# image_resolution = [3840,2160]          #4K resolution. Recommended resolution for saving images.
# image_resolution = [1125,2436]          #iPhone X resolution
# image_resolution = [2560,1440]         #Galaxy S8 and later (S8/9 and Note8/9 devices) resolution
# image_resolution = [750,1334]          #iPhone 8 resolution
# image_resolution = [1440,2560]         #Galaxy S6/S7 resolution
# image_resolution = [2000,2000]
image_resolution    = [3840,2160]
timesteps           = 1e8
randomize_values    = 1
randomize_color     = 1
save_image          = 0
images_to_make      = 1
chunk_size          = 1e6                      #don't make this too large unless you want to run out of ram
num_chunks          = round(timesteps/chunk_size)
smooth_image        = 1
my_dpi              = 240
import_params       = ''                       #Make this empty string ('') to avoid importing parameters
thing_array         = ['-','\\','|','/']
colormap_list       = ['inferno','nipy_spectral','hot','gnuplot2','jet','terrain','gist_ncar','viridis','plasma','magma',
                       'summer','autumn','winter','Wistia','ocean','rainbow','gist_rainbow','hsv','brg']
cm_name             = 'gnuplot2'
params              = [10.,28.,8./3.,1.]
whichattractor      = 0


#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#Turns out that this can be multithreaded just by setting something equal to 'True'!

if whichattractor==0:
    #original peter de jong attractor
    @njit(parallel=True)                                
    def attractor(x,y,num_steps,a,b,c,d):
        for i in range(1,int(num_steps)):
            x[i] = np.sin(a*y[i-1]) - np.cos(b*x[i-1])
            y[i] = np.sin(c*x[i-1]) - np.cos(d*y[i-1]) 
        return x,y
    imgdir = '/home/ethan/code/strange/images/0/'
    paramdir = '/home/ethan/code/strange/parameters/0/'

elif whichattractor==1:
    #modified pdj attractor
    @njit(parallel=True)                                
    def attractor(x,y,num_steps,a,b,c,d):
        for i in range(1,int(num_steps)):
            x[i+1] = np.sin(a*y[i]) - np.cos(b*x[i-1])
            y[i+1] = np.sin(c*x[i]) - np.cos(d*y[i-1])
        return x,y
    imgdir = '/home/ethan/code/strange/images/1/'
    paramdir = '/home/ethan/code/strange/parameters/1/'
    

elif whichattractor==2:
    #i forget what this one is called but its from fluid dynamics?
    @njit(parallel=True)                                
    def attractor(x,y,num_steps,a,b,c,d):
        for i in range(1,int(num_steps)):
            x[i] = x[i-1] - y[i-1]
            y[i] = y[i-1] + x[i-1] + a*y[i-1]
        return x,y
    imgdir = '/home/ethan/code/strange/images/2/'
    paramdir = '/home/ethan/code/strange/parameters/2/'

elif whichattractor==3:
    #lorenz attractor
    @njit(parallel=True)                                
    def attractor(x,y,z,num_steps,a,b,c):
        for i in range(1,int(num_steps)):
            x[i] = x[i-1] + a*(x[i-1] - y[i-1])
            y[i] = y[i-1] + x[i-1]*(b-z[i-1]) - y[i-1] 
            z[i] = z[i-1] + x[i-1]*y[i-1] - c*z[i-1]
        return x,y,z
    imgdir = '/home/ethan/code/strange/images/3/'
    paramdir = '/home/ethan/code/strange/parameters/3/'

elif whichattractor==4:
    #i forget what this one is called but its from fluid dynamics?
    @njit(parallel=True)                                
    def attractor(x,y,num_steps,a,b,c,d):
        x = np.random.normal(a, b, size=int(num_steps))
        y = np.random.normal(c, d, size=int(num_steps))
        return x,y
    imgdir = '/home/ethan/code/strange/images/4/'
    paramdir = '/home/ethan/code/strange/parameters/4/'

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
for iteration in range(0,images_to_make):           
    
    if randomize_values == 1:
        a = np.random.uniform(-5,5)                 
        b = np.random.uniform(-5,5)
        c = np.random.uniform(-5,5)
        d = np.random.uniform(-5,5)
    elif import_params:
        print('Importing From File #'+import_params)
        newpfile = open(paramdir+import_params+'.txt', 'r')
        steps = np.int(newpfile.readline())
        a = np.float(newpfile.readline())
        b = np.float(newpfile.readline())
        c = np.float(newpfile.readline())
        d = np.float(newpfile.readline())
    else:
        a = params[0]
        b = params[1]
        c = params[2]
        d = params[3]

    #intialize arrays
    x = np.zeros(int(chunk_size)); x[0] = 0.5 
    y = np.zeros(int(chunk_size)); y[0] = 0.5

    print('Starting Calculations...')
    x,y = attractor(x,y,chunk_size,a,b,c,d)      
    isnanxy = not((np.count_nonzero(np.isnan(x)) > 0) or (np.count_nonzero(np.isnan(y)) > 0))

    #----------------------------------------------------------------------------------------------
    #---skip-bad-parameters------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------
    if (len(set(x)) == chunk_size) or (len(set(y)) == chunk_size) or isnanxy:
        hist = np.histogram2d(x,y,bins=[image_resolution[1],image_resolution[0]])[0]            
        
        printstring = 'Finished chunk 1 of '+str(int(num_chunks)) + ' [' + thing_array[0]+']'
        sys.stdout.write(printstring)
        sys.stdout.flush()
        sys.stdout.write("\b" * len( printstring ))
            
        if timesteps > chunk_size:
            for i in range(1,int(num_chunks)):   
                x[0] = x[int(chunk_size-1)]         
                y[0] = y[int(chunk_size-1)]
                x,y = attractor(x,y,chunk_size,a,b,c,d)
                hist += np.histogram2d(x,y,bins=[image_resolution[1],image_resolution[0]])[0]       
                printstring = 'Finished chunk '+str(i+1)+' of '+str(int(num_chunks)) + ' [' + thing_array[(i+1)%4] + ']'
                sys.stdout.write(printstring)
                sys.stdout.flush()
                if not(i+1 == num_chunks):
                    sys.stdout.write("\b" * len( printstring))
        

        hist = np.log10(hist+0.01)                      
        if smooth_image == 1:                           
            print('\n'+'Smoothing image...')
            hist_final = gaussian_filter(hist,0.5,0)
        else:
            hist_final = hist
        
        #------------------------------------------------------------------------------------------
        #---plotting-section-----------------------------------------------------------------------
        #------------------------------------------------------------------------------------------
        plt.close('all')        
                                
        fig_hist = plt.figure(figsize=(image_resolution[0]/my_dpi, image_resolution[1]/my_dpi), dpi=my_dpi,frameon=False)

        ax = plt.Axes(fig_hist, [0., 0., 1., 1.])           
        ax.set_axis_off()
        fig_hist.add_axes(ax)                  

        if randomize_color:
            cm_name = np.random.choice(colormap_list)

        cmap = cm.get_cmap(cm_name)
        cmap.set_under('black')                                                                 
        ax.imshow(hist_final,cmap=cmap,aspect='equal',vmin=hist.min()+0.00001)                  

        if save_image == 1:
            imgnum = str(  len(sorted(os.listdir(imgdir)))+1    )
            imgnum = (3 - len(imgnum))*'0' + imgnum
            if not(import_params):
                pfile = open(paramdir+imgnum+'.txt','w')
                pfile.write(str(int(timesteps))+'\n')
                pfile.write(str(a)+'\n')
                pfile.write(str(b)+'\n')
                pfile.write(str(c)+'\n')
                pfile.write(str(d)+'\n')
                pfile.close()
            else:
                imgnum = import_params+'_redo_'+cm_name
            plt.savefig(imgdir+imgnum+'.png',format='png',dpi=my_dpi)   

        else:
            plt.show()

        end_time=time.time()
        elapsed_time = round(end_time - start_time,2)   
        print('Elapsed Time: '+str(elapsed_time)+' seconds')
            
    else:
        print('Found a bad combination of parameters. Moving to next image.')
