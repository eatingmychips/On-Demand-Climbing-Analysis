import csv 
import pandas as pd
from itertools import islice
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy import signal
from elytra_pre_analysis import *
import statistics as stat
import matplotlib.patches as mpatches
from os import listdir


######## Here we import the files necessary for analysis, we also import the representative files for gait plotting ########

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

files = [r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\ElytraRawData\\"+x 
             for x in find_csv_filenames(r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\ElytraRawData")]

########### End of file collection ###########



"""This is the statistical analysis function and will be called ONCE per angle. 
So, all files of a specific angle will be run through in the inner for loop. """

def stat_analysis(files):
    # Declare empty lists to store data (optional if you want to store the results later)
    vel_avg = []

    # Create subplots for in-line and transverse velocities
    

    for file in files: 
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        ## Read all files in and pass through moving average filter ##
        parts = file_read(file)
        top = moving_avg(parts[0])
        middle = moving_avg(parts[1])
        bottom = moving_avg(parts[2])

        # Get the stimulation Position from csv file
        stim_pos = stim_file_read(file)

        ## Calculate avg body velocity ##
        in_line_vel, transv_vel = body_vel(middle, bottom)

        # Plot in-line velocity on ax1
        ax1.plot(in_line_vel, label=f'In-line Velocity ({file})')
        ax1.axvline(x=stim_pos, color='r', linestyle='--', label=f'Stim {file}')  # Mark stimulation point

        # Plot transverse velocity on ax2
        ax2.plot(transv_vel, label=f'Transverse Velocity ({file})')
        ax2.axvline(x=stim_pos, color='r', linestyle='--', label=f'Stim {file}')  # Mark stimulation point

        # Customize the plots
        ax1.set_title('In-line Velocity for All Files')
        ax1.set_ylabel('In-line Velocity (units/s)')
        #ax1.legend(loc='best')

        ax2.set_title('Transverse Velocity for All Files')
        ax2.set_ylabel('Transverse Velocity (units/s)')
        ax2.set_xlabel('Frame')
        #ax2.legend(loc='best')

        # Display the plots
        plt.tight_layout()
        plt.show()

    return vel_avg



stat_analysis(files)