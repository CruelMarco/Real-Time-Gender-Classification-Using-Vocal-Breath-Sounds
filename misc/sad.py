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
#from librosa.features import mfcc

dir = 'C:/Users/Spirelab/Desktop/open_day/lab_members'

model_dir = 'C:/Users/Spirelab/Desktop/open_day/saved_model'

os.chdir(dir)

files = os.listdir(dir)

audiofile = files[24]

#annotfile = txt_files[0]


def gender_classification(audio):
    
    #print(audio.shape)
    
    y,fs = librosa.load(audio, sr = 16000)

    mfcc_full = np.array(np.transpose(librosa.feature.mfcc(y , sr = fs , n_mfcc = 13 , n_fft = 320 , win_length = 320 , hop_length = 160)))

    mfcc_df = pd.DataFrame(mfcc_full , columns = ['F0' , 'F1' , 'F2' , 'F3' , 'F4' , 'F5' , 'F6' , 'F7' , 'F8' , 'F9' , 'F10' , 'F11' , 'F12'])

    mfcc_mean = np.array(np.transpose(mfcc_df[['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12']].mean())).reshape(1,-1)

    mfcc_median = np.array(mfcc_df[['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12']].median()).reshape(1,-1)

    mfcc_floor = np.array(mfcc_df[['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12']].apply(np.floor))

    mfcc_mode = stats.mode(mfcc_floor)[0].T.reshape(1,-1)

    mfcc_std = np.array(mfcc_df[['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12']].std()).reshape(1,-1)

    mfcc_stats = np.hstack((mfcc_mean, mfcc_median, mfcc_mode, mfcc_std))

    os.chdir(model_dir)

    json_file = open('model_2023_02_28_17_29.json' , 'r')

    loaded_model_json = json_file.read()

    json_file.close()

    loaded_model = model_from_json(loaded_model_json)
# load weights into new model
    loaded_model.load_weights("model_weights_2023_02_28_17_29.h5")

    print("Loaded model from disk")

    loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    prediction = loaded_model.predict(mfcc_stats)

    if prediction > 0.3:
    
        gender = 'Gender is Female'

    else:
    
        gender = 'Gender is Male'
    
    return(gender)

gender = gender_classification(audiofile)
