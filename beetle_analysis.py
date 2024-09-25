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




######## Here we import the files necessary for analysis, we also import the representative files for gait plotting ########

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith( suffix ) ]


dir_path = r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240719"

files = [r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240719\\" + x 
         for x in find_csv_filenames(dir_path)]

stim_files = [r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240719\Stimulations\\" + x 
         for x in find_csv_filenames(r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240719\Stimulations")]


stim_folder = r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\RawData\20240719\Stimulations"

########### End of file collection ########### 


def read_in(files): 
    pos_dict = {}   
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
        pos_dict[filename] = [points, stim]

    return pos_dict

##TODO: Implement body angle compared to wall, Is the wall on the left or right side. What is the latency of climb, from first stimulation? How many stimulations until successful climb? 
pos_dict = read_in(files)


corner_test = []
latencies = []
stim_effort = []

# Group the files by beetle name
beetle_groups = {}


# Dictionary to store results for each beetle
beetle_results = {}
beetle_latencies = {}
beetle_effort = {}
beetle_side_latencies = {}

# Populate the beetle_groups dictionary based on file names
for key, value in pos_dict.items():
    # Extract the beetle name using regex (assuming filenames follow 'Beetle_x_trial_...')
    beetle_name = re.match(r"(beetle_\d+)", key).group(1)  # Match the beetle name pattern
    

    if beetle_name not in beetle_groups:
        beetle_groups[beetle_name] = []
    
    # Append the current file (and its associated values) to the list for that beetle
    beetle_groups[beetle_name].append((key, value))


#Lists for comparing middle and corner latencies and stimulation efforts
latencies_middle = []
latencies_corner = []
stimulation_effort_middle = []
stimulation_effort_corner = []


# Now, loop through each beetle group and process files for each beetle collectively
for beetle_name, beetle_data in beetle_groups.items():
    corner_test = []
    latencies = []
    stim_effort = []

    print(f"\nProcessing data for {beetle_name}:")
    
    for key, value in beetle_data:
        # print("\n For: ", key, " We have the following results: ")
        # print("Average angle before wall climb: ", get_avg_angle(value))
        # print("Latency for wall climb from first stimulation: ", get_stim_latency(value))
        # print("Number of stimulations before wall climb: ", get_num_stims(value))

        # Append whether climb was corner or middle climb
        _, corner_middle = get_avg_angle(value)
        corner_test.append(corner_middle)

        if corner_middle == 0: 
            latencies_middle.append(get_stim_latency(value))
            stimulation_effort_middle.append(get_num_stims(value))
        elif corner_middle == 1: 
            latencies_corner.append(get_stim_latency(value))
            stimulation_effort_corner.append(get_num_stims(value))
        
        # Append Latency Value
        latencies.append(get_stim_latency(value))

        # Append Stim Effort
        stim_effort.append(get_num_stims(value))

    # Calculate statistics for the beetle
    ratio_corner = sum(corner_test) / len(corner_test) * 100 if len(corner_test) > 0 else 0
    avg_latency = np.median(latencies) if len(latencies) > 0 else None
    avg_stim_effort = np.median(stim_effort) if len(stim_effort) > 0 else None

    # Print the calculated values for each beetle
    print(f"\n{beetle_name} climbs corner walls {ratio_corner:.2f}% of the time")
    print("Average latency from first stimulation: ", avg_latency)
    print("Average stimulation effort was: ", avg_stim_effort)

    # Store the results in beetle_results dictionary
    beetle_results[beetle_name] = {
        "ratio_corner": ratio_corner,
        "avg_latency": avg_latency,
        "avg_stim_effort": avg_stim_effort
    }

    beetle_latencies[beetle_name] = latencies
    beetle_effort[beetle_name] = stim_effort
    
    


print(latencies_corner)
fig, axs = plt.subplots(1, 2, figsize=(10, 6))


axs[0].boxplot(beetle_latencies.values(), labels=beetle_latencies.keys())
axs[0].set_title('Boxplot of Stimulation Latencies for Each Beetle')
axs[0].set_xlabel('Beetle Name')
axs[0].set_ylabel('Stimulation Latencies (seconds)')

axs[1].boxplot(beetle_effort.values(), labels = beetle_effort.keys())
axs[1].set_title('Boxplot of Stimulation Effort for Each Beetle')
axs[1].set_xlabel('Beetle Name')
axs[1].set_ylabel('Stimulation Effort (No. Stimulations)')



plt.show()

laten_corner_middle = [latencies_corner, latencies_middle]
label = ["Corner", "Middle"]
fig, axs = plt.subplots(1, 2, figsize=(10, 6))
axs[0].boxplot(laten_corner_middle)
axs[0].set_xticklabels(label, fontsize = 13)
axs[0].set_ylabel("Wall Climbing Latency (s)")
axs[0].set_title("Wall Climbing Latency vs Corner or Middle Climb")

stim_corner_middle = [stimulation_effort_corner, stimulation_effort_middle]
label = ["Corner", "Middle"]
axs[1].boxplot(stim_corner_middle)
axs[1].set_xticklabels(label, fontsize = 13)
axs[1].set_ylabel("Stimulation Effort")
axs[1].set_title("Stimulation Effort vs Corner or Middle Climb")

plt.show()




