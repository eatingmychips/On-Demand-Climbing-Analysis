import csv 
import pandas as pd
import itertools as it
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy import signal
import random
import os

def file_read(file):
    df = pd.read_csv(file, skiprows=2)
    
    new_column_names = ['coords', 'topx', 'topy', 'likelihood', 'middlex', 'middley', 'likelihood', 'bottomx', 'bottomy', 'likelihood']
    
    df.columns = new_column_names

    size = range(len(df.get('topx').to_numpy()))

    #Read in top
    topx = df.get('topx').to_numpy()
    topy = df.get('topy').to_numpy()
    top =[]
    for i in size: 
        top.append([topx[i], topy[i]])

    #Read in middle 
    middlex = df.get('middlex').to_numpy()
    middley = df.get('middley').to_numpy()
    middle = []
    for i in size: 
        middle.append([middlex[i], middley[i]])



    #Read in bottom 
    bottomx = df.get('bottomx').to_numpy()
    bottomy = df.get('bottomy').to_numpy()
    bottom = []
    for i in size: 
        bottom.append([bottomx[i], bottomy[i]])


    #Declare list of body parts for use in later code
    
    parts = [top, middle, bottom]
    
    return parts

def stim_file_read(file): 

    # Step 1: Remove the "DLC_resnet50_TwoCamDLCAug13shuffle1_100000" part
    file = os.path.basename(file)
    stripped_filename = file.split("DLC_resnet50_TwoCamDLCAug13shuffle1_100000")[0]
    
    # Step 2: Remove the "camera-1_" part
    stripped_filename = stripped_filename.replace("camera-1_", "")
    stim_file = r"C:\Users\lachl\OneDrive\Thesis\OnDemandClimbing\ElytraRawData\Stimulations\\" + stripped_filename + ".csv"

    df = pd.read_csv(stim_file, header = None)
    stim_pos = df.iloc[0,0]

    return stim_pos
    


def moving_avg(part):
    
        partx = []
        party = []
        for i in part: 
            partx.append(i[0])
            party.append(i[1])
        
        partx = pd.Series(partx)
        party = pd.Series(party)
        
        partx = round(partx.ewm(alpha=0.2, adjust= False).mean(), 100)
        partx = partx.tolist()

        party = round(party.ewm(alpha=0.2, adjust= False).mean(), 100)
        party = party.tolist()


        smooth_data = []
        for i in range(len(partx)):
            smooth_data.append([partx[i], party[i]])

        return smooth_data

# TODO: Fix Transverse velocity to return +ves and -ves

def body_vel(middle, bottom):
    body_v_in_line = []
    body_v_transverse = []
    size = range(len(middle))

    for i in size: 
        if i > 2: 
            # Calculate velocity vector of the middle point
            delta = np.subtract(middle[i], middle[i-2])
            
            # Calculate the direction of the body (middle to bottom)
            body_axis = np.subtract(middle[i], bottom[i])
            body_axis_norm = np.linalg.norm(body_axis)

            # Normalize the body axis to get the unit vector
            body_axis_unit = body_axis / body_axis_norm if body_axis_norm != 0 else np.zeros_like(body_axis)

            # Project the velocity vector onto the body axis to get in-line velocity
            in_line_velocity = np.dot(delta, body_axis_unit)

            # Subtract the in-line velocity from total velocity to get transverse velocity
            total_velocity = np.linalg.norm(delta)
            transverse_velocity = np.sqrt(total_velocity**2 - in_line_velocity**2)

            # Normalize and scale velocities (assuming 78 is the scaling factor)
            in_line_velocity = in_line_velocity / 78 * 100
            transverse_velocity = transverse_velocity / 78 * 100

            body_v_in_line.append(in_line_velocity)
            body_v_transverse.append(transverse_velocity)
        
    # Apply exponential smoothing to both in-line and transverse velocities
    body_v_in_line = pd.Series(body_v_in_line).ewm(alpha=0.5, adjust=False).mean().tolist()
    body_v_transverse = pd.Series(body_v_transverse).ewm(alpha=0.5, adjust=False).mean().tolist()

    return round(pd.Series(body_v_in_line), 5).tolist(), round(pd.Series(body_v_transverse), 5).tolist()