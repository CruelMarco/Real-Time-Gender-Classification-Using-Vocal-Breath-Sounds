# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 20:25:22 2023

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
from Gender_predictor import user_gender


dir = 'C:/Users/Spirelab/Desktop/open_day/lab_members'

os.chdir(dir)

name = "shreya"

gen = user_gender(name)

if gen == 0:
    print("Predicted Gender is Male")
else:
    print("Predicted Gender is Female")


