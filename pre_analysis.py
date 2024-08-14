import csv 
import pandas as pd
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy import signal
import random

def file_read(file):
    df = pd.read_csv(file, skiprows=2)
    
    new_column_names = ['coords', 'topx', 'topy', 'likelihood', 'middlex', 'middley', 'likelihood', 'bottomx', 'bottomy', 'likelihood' ]
    
    df.columns = new_column_names

    size = range(len(df.get('middlex').to_numpy()))

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
    body_v = round(body_v.ewm(alpha = 0.08, adjust= False).mean(), 5)
    body_v = body_v.tolist()

    return body_v

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
