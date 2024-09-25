import csv 
import pandas as pd
import itertools as it
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy import signal
import random

def file_read(file):
    df = pd.read_csv(file)
    

    size = range(len(df.get('middle_x').to_numpy()))

    #Read in top
    topx = df.get('top_x').to_numpy()
    topy = df.get('top_y').to_numpy()
    topz = df.get('top_z').to_numpy()
    top =[]
    for i in size: 
        top.append([topx[i], topy[i], topz[i]])

    #Read in middle 
    middlex = df.get('middle_x').to_numpy()
    middley = df.get('middle_y').to_numpy()
    middlez = df.get('middle_z').to_numpy()
    middle = []
    for i in size: 
        middle.append([middlex[i], middley[i], middlez[i]])



    #Read in bottom 
    bottomx = df.get('bottom_x').to_numpy()
    bottomy = df.get('bottom_y').to_numpy()
    bottomz = df.get('bottom_z').to_numpy()
    bottom = []
    for i in size: 
        bottom.append([bottomx[i], bottomy[i], bottomz[i]])


    #Declare list of body parts for use in later code
    
    parts = [top, middle, bottom]
    
    return parts



def body_vel(middle):
    body_v = []
    size = range(len(middle))
    for i in size: 
        if i > 1: 
            delta = np.subtract(middle[i], middle[i-1])
            norm = np.linalg.norm(delta)
            norm = norm/78*100
            body_v.append(norm)
        
    body_v = pd.Series(body_v)
    body_v = round(body_v.ewm(alpha = 0.01, adjust= False).mean(), 5)
    body_v = body_v.tolist()

    return body_v

def moving_avg(part):
    
        partx = []
        party = []
        partz = []

        for i in part: 
            partx.append(i[0])
            party.append(i[1])
            partz.append(i[2])
        
        partx = pd.Series(partx)
        party = pd.Series(party)
        partz = pd.Series(partz)

        partx = round(partx.ewm(alpha=0.5, adjust= False).mean(), 5)
        partx = partx.tolist()

        party = round(party.ewm(alpha=0.5, adjust= False).mean(), 5)
        party = party.tolist()

        partz = round(partz.ewm(alpha=0.5, adjust= False).mean(), 5)
        partz = partz.tolist()


        smooth_data = []
        for i in range(len(partx)):
            smooth_data.append([partx[i], party[i], partz[i]])

        return smooth_data


### Plot x and y values w.r.t time ###
def xyzplot(parts, name):
    points = parts[0]
    stims = parts[1]
    top = points[0]
    middle = points[1]
    bottom = points[2]
    topx, topy, topz = zip(*top)
    middlex, middley, middlez = zip(*middle)
    bottomx, bottomy, bottomz = zip(*bottom)

    fig, axs = plt.subplots(3, 1, figsize=(10, 8))

    # Plot x coordinates for top, middle, bottom
    axs[0].plot(topx, label='Top', marker='o')
    axs[0].plot(middlex, label='Middle', marker='o')
    axs[0].plot(bottomx, label='Bottom', marker='o')
    axs[0].set_title('X Coordinates')
    axs[0].legend()

    # Plot y coordinates for top, middle, bottom
    axs[1].plot(topy, label='Top', marker='o')
    axs[1].plot(middley, label='Middle', marker='o')
    axs[1].plot(bottomy, label='Bottom', marker='o')
    axs[1].set_title('Y Coordinates')
    axs[1].legend()

    # Plot z coordinates for top, middle, bottom
    axs[2].plot(topz, label='Top', marker='o')
    axs[2].plot(middlez, label='Middle', marker='o')
    axs[2].plot(bottomz, label='Bottom', marker='o')
    axs[2].set_title('Z Coordinates')
    axs[2].legend()

    # Set a common x-label for all subplots
    for ax in axs:
        for stim in stims:
            ax.axvline(x=stim, color='r', linestyle='--', label='Stimulus' if stim == stims[0] else "")
        ax.set_xlabel('Frames')
        ax.legend()

    axs[0].set_title(name)

    # Adjust layout
    plt.tight_layout()
    plt.show()


def plot_3d(parts):
    top = parts[0]
    middle = parts[1]
    bottom = parts[2]
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    topx, topy, topz = zip(*top)
    middlex, middley, middlez = zip(*middle)
    bottomx, bottomy, bottomz = zip(*bottom)
    ax.scatter(topx, topy, topz)
    ax.scatter(middlex, middley, middlez)
    ax.scatter(bottomx, bottomy, bottomz)

    plt.show()


def get_stim_list(path): 
    with open(path, newline='') as csvfile: 
        reader = csv.reader(csvfile)
        row = next(reader)

    return list(map(int, row))



def get_avg_angle(parts): 
    points = parts[0]
    top = points[0]
    middle = points[1]
    bottom = points[2]
    angles = []
    if len(bottom) == 0 or len(middle) == 0:
        return "No valid coordinates in bottom or middle", 0
    
    for coord1, coord2 in zip(bottom, middle): 
        x1, y1, z1 = coord1
        x2, y2, z2 = coord2
    
        #We only care about the angle BEFORE we climb the wall. 
        if z1 or z2 > 450: 
            if x1 or x2 < -95:
                #Calculate the differences in x-y plane
                delta_x = x2 - x1
                delta_y = y2 - y1
                
                # Calculate the angle in radians
                angle_radians = math.atan2(delta_y, delta_x)
                
                # Convert angle to degrees
                angle_degrees = math.degrees(angle_radians)
                
                angles.append(angle_degrees)

                last_x = x2
                last_y = y2

    #TODO: Implement counting of corners and non-corners. Probably to do in 'statistical_analysis.py'. 
    #TODO: Implement Average Stim Latency / trial and / beetle. 
    #TODO: Implement 'stimulation effort function' Pretty much done with get_num_stims. 
    #TODO: Clarify orientation and DLC accuracy with videos on computer. 
    #TODO: Extract good example and see if analysis also looks good. 
    #TODO: Re-record raw elytra stimulation Parameters. 
    if not angles: 
        return "No Valid angles detected, ", 0

    avg = np.median(angles)
    
    
    if 20 < avg < 140:
        if last_y < -60:  #Beetle is on the top corner
            return "Right hand side facing wall, Top corner", 1
        elif last_y > 30: #Beetle is on the bottom corner
            return "Right hand side facing wall, Bottom corner", 1
        else:   #Beetle is in the middle 
            return "Right hand side facing wall, Middle", 0
        
    elif -200 < avg < -110:
        if last_y < -60 and last_x < -95:  #Beetle is on the top corner
            return "Right hand side facing wall, Top corner", 1
        elif last_y > 30 and last_x < -105: #Beetle is on the bottom corner
            return "Left hand side facing wall, Bottom corner", 1
        elif last_y < -60 and last_x > -95: 
            return "Right hand side facing wall, Middle", 0
        elif last_y > 30 and last_x > -105: 
            return "Left hand side facing wall, Middle", 0
        else: 
            return 0,0
    elif -100 < avg < 10: 
        if last_y < -60:  
            return "Left hand side facing wall, Top corner", 1
        elif last_y > 30:
            return "Left hand side facing wall, Bottom corner", 0
        else:
            return "Left hand side facing wall, Middle", 1
    else: 
        return "Unsure on wall orientation", 0



def get_stim_latency(parts): 
    #Get top, middle and bottom points
    points = parts[0]
    stim = parts[1]
    top = points[0]
    middle = points[1]
    bottom = points[2]

    begin = stim[0]

    for i in range(len(top)): 
        if top[i][2] < 450: 
            end = i
            break
        else: 
            end = i

    time = (end - begin)/100

    return time


def get_num_stims(parts): 
    points = parts[0]
    stims = parts[1]
    top = points[0]
    middle = points[1]
    bottom = points[2]

    pre_stims = []
    for i in range(len(top)): 
        if top[i][2] < 450: 
            for stim in stims: 
                if stim < i: 
                    pre_stims.append(stim)
            break
    
    return len(pre_stims)

