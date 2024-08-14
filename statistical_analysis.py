import csv 
import pandas as pd
from itertools import islice
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import MultipleLocator
from scipy import signal
from pre_analysis import *
import statistics as stat
import matplotlib.patches as mpatches
from os import listdir


######## Here we import the files necessary for analysis, we also import the representative files for gait plotting ########

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]



files = [r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\Presentation\\" + x 
         for x in find_csv_filenames(r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\Presentation")]

files = [r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\Presentation\beetle_8_trial_10_camera-1_clipDLC_resnet50_TwoCamDLCAug13shuffle1_100000.csv"]
########### End of file collection ###########

def stat_analysis(files): 
        
        for file in files:
            parts = file_read(file)
            top = moving_avg(parts[0])
            middle = moving_avg(parts[1])
            print(len(middle))
            bottom = moving_avg(parts[2])
            body_v = body_vel(middle)
            
        
        return body_v


body_v = stat_analysis(files)
time = list(range(len(body_v)))

fig, ax = plt.subplots()
line, = ax.plot(time, body_v)

# Set up plot limits
ax.set_xlim(0, len(time))
ax.set_ylim(np.min(body_v), np.max(body_v))
ax.set_title("Body Velocity vs Time (Frames)")
ax.set_xlabel("Frames (fps = 100)")
ax.set_ylabel("Velocity (Body Lengths / second)")

vertical_line = ax.axvline(x=time[125], color='red', linestyle=':', visible=False)

# Initialization function: plot the background of each frame
def init():
    line.set_ydata([np.nan] * len(time))
    vertical_line.set_visible(False)
    return line, vertical_line

# Animation function: update the line at each frame
def update(frame):
    line.set_data(time[:frame], body_v[:frame])
    if frame >= 125:
        vertical_line.set_visible(True)
    
    return line, vertical_line

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(time), init_func=init, blit=True, interval=15)

Writer = animation.FFMpegWriter(fps = 100, metadata=dict(artist = 'me'), bitrate = 1000)
ani.save("Animation.mp4", writer = Writer)
plt.show()