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
import re
import time

files = [r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240719\beetle_8_trial_2_segment_2_.csv", r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240724\beetle_3_trial_1_segment_2_.csv"]
files = [r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240724\beetle_3_trial_1_segment_2_.csv"]
stim_folder = r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240724\Stimulations"



def read_in(files): 
 
    for file in files:
        #Get the filename that is to be analysed : E.g: Beetle_x_trial_y_segment_z_
        filename = os.path.splitext(os.path.basename(file))[0]

        #Create the stimulation file name and merge with stimulation path, then grab stimulation file. 
        stim_name = filename + 'stimulation.csv'
        stim_path = f"{stim_folder}\\{stim_name}"
        stim = get_stim_list(stim_path)

        #Read in the raw_data_file
        parts = file_read(file)
        top = moving_avg(parts[0])
        middle = moving_avg(parts[1])
        bottom = moving_avg(parts[2])
        
        #Create a list of top, middle, bottom points and assign to dictionary with 'key' as filename. 
        points = [top, middle, bottom]
       

    return points, stim

##TODO: Implement body angle compared to wall, Is the wall on the left or right side. What is the latency of climb, from first stimulation? How many stimulations until successful climb? 
points, stim = read_in(files)
print(stim)
def transform_z(z_values, new_min=0, new_max=40):

    # Transform the z values
    return [-1*(z - 500) for z in z_values]

#### Scatter animation ####
def animation_scatter_3d():
    # Assuming points is a list of three lists, each containing (x, y, z) tuples
    top = points[0]
    middle = points[1]
    bottom = points[2]

    # Extract x, y, and z values for each dataset
    x_top, y_top, z_top = zip(*top)
    x_middle, y_middle, z_middle = zip(*middle)
    x_bottom, y_bottom, z_bottom = zip(*bottom)

    # Transform z values if needed
    z_top = transform_z(z_top)
    z_middle = transform_z(z_middle)
    z_bottom = transform_z(z_bottom)

    # Create a figure and 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Initialize scatter plots
    scatter_top = ax.scatter([], [], [], c='purple', marker='o', label='Top')
    scatter_middle = ax.scatter([], [], [], c='green', marker='o', label='Middle')
    scatter_bottom = ax.scatter([], [], [], c='red', marker='o', label='Bottom')

    # Set axis limits
    ax.set_xlim(min(x_top + x_middle + x_bottom), max(x_top + x_middle + x_bottom))
    ax.set_ylim(min(y_top + y_middle + y_bottom), max(y_top + y_middle + y_bottom))
    ax.set_zlim(min(z_top + z_middle + z_bottom), max(z_top + z_middle + z_bottom))

    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Add legend
    ax.legend()

    # Add gray planes
    xx, yy = np.meshgrid(np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 10),
                         np.linspace(ax.get_ylim()[0], ax.get_ylim()[1], 10))

    zz_xy_plane = np.zeros_like(xx)  # Z=0 for the XY plane
    ax.plot_surface(xx, yy, zz_xy_plane, color='gray', alpha=0.5)

    yy_yz_plane = np.linspace(ax.get_ylim()[0], ax.get_ylim()[1], 10)
    zz_yz_plane, _ = np.meshgrid(np.linspace(ax.get_zlim()[0], ax.get_zlim()[1], 10), yy_yz_plane)
    
    xx_yz_plane = -120 * np.ones_like(zz_yz_plane)  # X=-120 for the YZ plane
    ax.plot_surface(xx_yz_plane, yy_yz_plane, zz_yz_plane, color='gray', alpha=0.5)

    def init():
        scatter_top._offsets3d = ([], [], [])
        scatter_middle._offsets3d = ([], [], [])
        scatter_bottom._offsets3d = ([], [], [])
        return scatter_top, scatter_middle, scatter_bottom

    def animate(i):
        # Update the data for each scatter plot
        scatter_top._offsets3d = (x_top[i:i+1], y_top[i:i+1], z_top[i:i+1])
        scatter_middle._offsets3d = (x_middle[i:i+1], y_middle[i:i+1], z_middle[i:i+1])
        scatter_bottom._offsets3d = (x_bottom[i:i+1], y_bottom[i:i+1], z_bottom[i:i+1])
        return scatter_top, scatter_middle, scatter_bottom

    # Create an animation
    ani = animation.FuncAnimation(fig, animate, init_func=init,
                                  frames=len(top), interval=10,
                                  blit=False)

    # Display the animation
    plt.show()

    # Optionally, save the animation
    # Writer = animation.FFMpegWriter(fps=20, metadata=dict(artist='Me'), bitrate=1800)
    # ani.save("3d_scatter_animation.mp4", writer=Writer)

def animation_scatter_2d():
    # Assuming points is a list of three lists, each containing (x, y, z) tuples
    top = points[0]
    middle = points[1]
    bottom = points[2]

    # Extract x, y, and z values for each dataset
    x_top, y_top, z_top = zip(*top)
    x_middle, y_middle, z_middle = zip(*middle)
    x_bottom, y_bottom, z_bottom = zip(*bottom)

    # # Transform z values
    z_top = transform_z(z_top)
    z_middle = transform_z(z_middle)
    z_bottom = transform_z(z_bottom)

    # Create a figure and subplots
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))

    # Set titles and labels for each subplot
    for ax in axs:
        ax.set_xlim(0, len(x_top))
        ax.set_xlabel('Time')
    
    axs[0].set_title('X vs Time')
    axs[0].set_ylabel('X')
    
    axs[1].set_title('Y vs Time')
    axs[1].set_ylabel('Y')
    
    axs[2].set_title('Z vs Time')
    axs[2].set_ylabel('Z')

    # Initialize lines for each subplot
    line_x_top, = axs[0].plot(x_top, 'purple', label='Top')
    line_x_middle, = axs[0].plot(x_middle, 'green', label='Middle')
    line_x_bottom, = axs[0].plot(x_bottom, 'red', label='Bottom')

    line_y_top, = axs[1].plot(y_top, 'purple', label='Top')
    line_y_middle, = axs[1].plot(y_middle, 'green', label='Middle')
    line_y_bottom, = axs[1].plot(y_bottom, 'red', label='Bottom')

    line_z_top, = axs[2].plot(z_top, 'purple', label='Top')
    line_z_middle, = axs[2].plot(z_middle, 'green', label='Middle')
    line_z_bottom, = axs[2].plot(z_bottom, 'red', label='Bottom')

    # Add legends
    for ax in axs:
        ax.legend()

    # Initialize vertical lines for stim points
    stim_lines = [[ax.axvline(x=stim_point, color='red', linestyle=':', visible=False) for stim_point in stim] for ax in axs]


    def init():
        for line in [line_x_top, line_x_middle, line_x_bottom,
                     line_y_top, line_y_middle, line_y_bottom,
                     line_z_top, line_z_middle, line_z_bottom]:
            line.set_data([], [])
        
        for ax_lines in stim_lines:
            for stim_line in ax_lines:
                stim_line.set_visible(False)
            
        return (line_x_top, line_x_middle, line_x_bottom,
                line_y_top, line_y_middle, line_y_bottom,
                line_z_top, line_z_middle, line_z_bottom) + tuple(stim_line for ax_lines in stim_lines for stim_line in ax_lines)

    def animate(i):
        if i < len(x_top):
            line_x_top.set_data(range(i), x_top[:i])
            line_x_middle.set_data(range(i), x_middle[:i])
            line_x_bottom.set_data(range(i), x_bottom[:i])

            line_y_top.set_data(range(i), y_top[:i])
            line_y_middle.set_data(range(i), y_middle[:i])
            line_y_bottom.set_data(range(i), y_bottom[:i])

            line_z_top.set_data(range(i), z_top[:i])
            line_z_middle.set_data(range(i), z_middle[:i])
            line_z_bottom.set_data(range(i), z_bottom[:i])

        for j in range(len(stim)):
            if i >= stim[j]:
                for ax_lines in stim_lines:
                    ax_lines[j].set_visible(True)

        return (line_x_top, line_x_middle, line_x_bottom,
                line_y_top, line_y_middle, line_y_bottom,
                line_z_top, line_z_middle, line_z_bottom) + tuple(stim_line for ax_lines in stim_lines for stim_line in ax_lines)

    # Create an animation with 100 frames per second
    ani = animation.FuncAnimation(fig, animate, init_func=init,
                                  frames=len(top), interval=1,
                                  blit=True)

    # Display the animation
    plt.tight_layout()
    plt.show()

def calculate_angle(x1, y1, x2, y2):
    # Calculate the angle in radians and convert to degrees
    return np.degrees(np.arctan2(y2 - y1, x2 - x1))

def animation_scatter_angle():
    # Assuming points is a list of three lists, each containing (x, y, z) tuples
    top = points[0]
    middle = points[1]
    bottom = points[2]

    # Extract x, y, and z values for each dataset
    x_top, y_top, z_top = zip(*top)
    x_middle, y_middle, z_middle = zip(*middle)
    x_bottom, y_bottom, z_bottom = zip(*bottom)

    # # Transform z values
    z_top = transform_z(z_top)
    z_middle = transform_z(z_middle)
    z_bottom = transform_z(z_bottom)

    # Calculate angles between middle and bottom points
    angles = [calculate_angle(xm, ym, xb, yb) for xm, ym, xb, yb in zip(x_middle, y_middle, x_bottom, y_bottom)]

    # Create a figure and subplots
    fig, axs = plt.subplots(2, 1, figsize=(8, 8))

    # Set titles and labels for each subplot
    axs[0].set_title('Angle in XY Plane vs Time')
    axs[0].set_ylabel('Angle (degrees)')
    axs[0].set_xlim(0, len(angles))
    
    axs[1].set_title('Z vs Time')
    axs[1].set_ylabel('Z')
    axs[1].set_xlim(0, len(z_middle))

    for ax in axs:
        ax.set_xlabel('Time')

    # Initialize lines for each subplot
    line_angle, = axs[0].plot(angles, 'blue', label='Angle')
    line_z_top, = axs[1].plot(z_top, 'purple', label='Top')
    line_z_middle, = axs[1].plot(z_middle, 'green', label='Middle')
    line_z_bottom, = axs[1].plot(z_bottom, 'red', label='Bottom')
    # Add legends
    for ax in axs:
        ax.legend()

    def init():
        line_angle.set_data([], [])
        line_z_middle.set_data([], [])
        line_z_bottom.set_data([], [])
        line_z_top.set_data([], [])
        return line_angle, line_z_middle, line_z_bottom

    def animate(i):
        # Update the data for each subplot
        if i < len(angles):
            line_angle.set_data(range(i), angles[:i])
            line_z_middle.set_data(range(i), z_middle[:i])
            line_z_bottom.set_data(range(i), z_bottom[:i])
            line_z_top.set_data(range(i), z_top[:i])
        return line_angle, line_z_middle, line_z_bottom, line_z_top

    # Create an animation with 100 frames per second
    ani = animation.FuncAnimation(fig, animate,
                                  init_func=init,
                                  frames=len(angles),
                                  interval=10,
                                  blit=True)

    # Display the animation
    plt.tight_layout()
    plt.show()

# Call the function to run the animation
animation_scatter_2d()
# Call the function to run the animation