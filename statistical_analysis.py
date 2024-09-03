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
import os

######## Here we import the files necessary for analysis, we also import the representative files for gait plotting ########

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith( suffix ) ]



files = [r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240719\\" + x 
         for x in find_csv_filenames(r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240719")]

stim_files = [r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240719\Stimulations\\" + x 
         for x in find_csv_filenames(r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240719\Stimulations")]


stim_folder = r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240719\Stimulations"

########### End of file collection ########### 


def stat_analysis(files): 
    pos_dict = {}   
    for file in files:
        filename = os.path.splitext(os.path.basename(file))[0]
        stim_name = filename + 'stimulation.csv'
        stim_path = f"{stim_folder}\\{stim_name}"
        stim = get_stim_list(stim_path)
        parts = file_read(file)
        top = moving_avg(parts[0])
        middle = moving_avg(parts[1])
        bottom = moving_avg(parts[2])
        body_v = body_vel(middle)
        
        points = [top, middle, bottom]
        pos_dict[filename] = [points, stim]

    return body_v, pos_dict

##TODO: Implement body angle compared to wall, Is the wall on the left or right side. What is the latency of climb, from first stimulation? How many stimulations until successful climb? 

body_v, pos_dict = stat_analysis(files)





for key, value in pos_dict.items():
    xyzplot(value, key)








#### Animation of Velocity ####

"""
def animation_vel(): 
    fig, ax = plt.subplots()
    line, = ax.plot(time, body_v)

    # Set up plot limits
    ax.set_xlim(0, len(time))
    ax.set_ylim(0, 1.5)
    ax.set_title("Body Velocity vs Time (Frames) (Right Elytra Stimulation)")
    ax.set_xlabel("Frames (fps = 100)")
    ax.set_ylabel("Velocity (Body Lengths / second)")

    vertical_line1 = ax.axvline(x=time[50], color='red', linestyle=':', visible=False)
    vertical_line2 = ax.axvline(x=time[130], color='red', linestyle=':', visible=False)
    vertical_line3 = ax.axvline(x=time[200], color='red', linestyle=':', visible=False)
    vertical_line4 = ax.axvline(x=time[250], color='red', linestyle=':', visible=False)
    vertical_line5 = ax.axvline(x=time[330], color='red', linestyle=':', visible=False)

    # Initialization function: plot the background of each frame
    def init():
        line.set_ydata([np.nan] * len(time))
        vertical_line1.set_visible(False)
        vertical_line2.set_visible(False)
        vertical_line3.set_visible(False)
        vertical_line4.set_visible(False)
        vertical_line5.set_visible(False)

        return line, vertical_line1, vertical_line2, vertical_line3, vertical_line4, vertical_line5

    # Animation function: update the line at each frame
    def update(frame):
        line.set_data(time[:frame], body_v[:frame])
        if frame >= 50:
            vertical_line1.set_visible(True)
        if frame >= 130:
            vertical_line2.set_visible(True)
        if frame >= 200:
            vertical_line3.set_visible(True)
        if frame >= 250:
            vertical_line4.set_visible(True)
        if frame >= 330:
            vertical_line5.set_visible(True)
        
        return line, vertical_line1, vertical_line2, vertical_line3, vertical_line4, vertical_line5

    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=len(time), init_func=init, blit=True, interval=3)

    Writer = animation.FFMpegWriter(fps = 100, metadata=dict(artist = 'me'), bitrate = 1000)
    ani.save("vert_wall_beetle_6_trial_2_cam-1.mp4", writer = Writer)
    plt.show()


#### Scatter animation ####
def animation_scatter():
    top = points[0]
    middle = points[1]
    bottom = points[2]

    # Extract x and y values for each dataset
    x_top, y_top = zip(*top)
    x_middle, y_middle = zip(*middle)
    x_bottom, y_bottom = zip(*bottom)

    # Create a figure and axis
    fig, ax = plt.subplots()
    line_top, = ax.plot([], [], color='purple', marker='o', linestyle='-', label='Top')
    line_middle, = ax.plot([], [], 'go-', label='Middle')
    line_bottom, = ax.plot([], [], 'ro-', label='Bottom')

    # Set axis limits
    ax.set_xlim(min(x_top + x_middle + x_bottom) - 1, max(x_top + x_middle + x_bottom) + 1)
    ax.set_ylim(min(y_top + y_middle + y_bottom) - 1, max(y_top + y_middle + y_bottom) + 1)

    # Add legend
    ax.legend()

    def init():
        line_top.set_data([], [])
        line_middle.set_data([], [])
        line_bottom.set_data([], [])
        return line_top, line_middle, line_bottom

    def animate(i):
        # Update the data for each line
        line_top.set_data(x_top[i:i+1], y_top[i:i+1])
        line_middle.set_data(x_middle[i:i+1], y_middle[i:i+1])
        line_bottom.set_data(x_bottom[i:i+1], y_bottom[i:i+1])
        return line_top, line_middle, line_bottom

    # Create an animation
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(top), interval=1, blit=True)

    # Display the animation
    plt.show()
"""





