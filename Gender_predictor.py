# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:43:01 2023

@author: Spirelab
"""

import tkinter as tk
import pyaudio
import wave
import librosa
from datetime import datetime
import pandas as pd
import numpy as np
import os
from scipy import stats
from keras.models import model_from_json
from Predictor_function import gender_classification
#from librosa.features import mfcc


def user_gender(user):
    
    files = os.listdir('C:/Users/Spirelab/Desktop/open_day/open_day_audios/Real Time Gender Classification Using Vocal Breath Sounds')
    
    user_files = [f for f in files if user in f]
    
    gender_list = []
    
    for i in user_files:
        
        gender, prediction = gender_classification(i)
        
        if gender == 1:
            
            gender_list.append(1)
        
            #print("Predicted Gender is Female")
        
        else:
            
            gender_list.append(0)
        
            #print("Predicted Gender is Male")
        
    sex = max(set(gender_list), key = gender_list.count)
    
    return(sex)



    
