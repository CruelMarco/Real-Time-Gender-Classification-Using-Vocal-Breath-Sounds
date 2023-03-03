# importing everything from tkinter
from tkinter import *
# importing the styling module ttk from tkinter
from tkinter import ttk
# importing the message boxes from tkinter
from tkinter.messagebox import showinfo, showerror, askokcancel
# this is for recording the actual voice
import sounddevice
# this is for saving the recorded file to wav file format
from scipy.io.wavfile import write
# threading will help the app's tasks run concurrently
import threading
# importing datetime from datetime to handle dates
from datetime import datetime
# this will handle time
import time
# os module will be used for renaming files
import os
import numpy as np
import soundfile as sf
import wave
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import random
from Predictor_function import gender_classification
from Gender_predictor import user_gender
from tkinter import Toplevel
import tkinter as tk


# the function for closing the main window
def close_window():
    # here we are checking if the value of askokcancel is True
    if askokcancel(title='Close Voice Recorder', message='Are you sure you want to close the Voice Recorder?'):
        # this kills the window
        window.destroy()




# function for recording sound
def record_voice():
    # the try statement is for 
    global name
    try:
        # this is the frequence at which the record will happen   
        freq = 16000
        # getting the recording duration from the entry
        duration = int(duration_entry.get())
        name_label= name_entry.get()    
        # calling the recorder via the rec() function
        name= name_label
        recording  = sounddevice.rec(duration*freq, samplerate=freq, channels=2)

        # declaring the counter
        counter = 0
        # the loop is for displaying the recording progress
        while counter < duration:
            # updating the window
            window.update()
            # this will help update the window after every 1 second
            time.sleep(1)
            # incrementing the counter by 1
            counter += 1
            # displaying the recording duration
            progress_label.config(text=str(counter))

        # this records audio for the specified duration 
        sounddevice.wait()
       
        # writing the audio data to recording.wav
        write('recording.wav', freq, recording)
       
        
        
        #plt.rcParams["figure.figsize"] = [7.50, 3.50]
        #plt.rcParams["figure.autolayout"] = True
        input_data = read("recording.wav")
        audio = input_data[1]
        plt.plot(audio)
        plt.title('Waveform Plot')
        plt.ylabel("Amplitude")
        plt.xlabel("Samples")
        plt.show()

     
        # looping through all the files in the current folder
        for file in os.listdir():
            # checking if the file name is recording.wav
            if file=='recording.wav':
                
                # spliting the base and the extension
                base, ext = os.path.splitext(file)
                # getting current time
                current_time = datetime.now()
                # creating a new name for the recorded file
                a=random.randint(0,10000)
                new_name = 'recording_' + name_label+'_'+str(a) + ext
                
                # renaming the file
                os.rename(file, new_name)
        # display a message when recording is done  
        showinfo('Recording complete', 'Your recording is complete')
        
        
    # function for catching all errors   
    except:
        # display a message when an error is caught
        showerror(title='Error', message='An error occurred' \
                   '\nThe following could ' \
                    'be the causes:\n->Bad duration value\n->An empty entry field\n' \
                    'Do not leave the entry empty and make sure to enter a valid duration value')
        
# the function to run record_voice as a thread
def recording_thread():
    # creating the thread whose target is record_voice()
    t1 = threading.Thread(target=record_voice)
    # starting the thread
    t1.start()

def predict_thread():
    '''
    Import the wav file stored in the folder and read it, and take the whole boundaries as the entire thing as breath, calculate mfcc
    Run it through the model, put the sex in a list
    Run it 3 times,append list
    Take max(variable) from the list and display it in a label
    
    '''
    global name
    gen=user_gender(name)
    show_gender(gen)
    



def show_gender(gen):
    answer_window = tk.Toplevel(window)
    # Create a Text widget in the new window
    #answer_window.configure(bg='#FF0000')
    #answer_window.configure(bg='blue')
    answer_text = tk.Text(answer_window)
    answer_text.pack()
    # Insert the answer into the Text widget
    if(gen==0):
        answer="Predicted Sex is Male"
        answer_text.insert(tk.END, answer)
        answer_text.tag_configure('blue', foreground='blue')
        answer_text.tag_add('blue', '1.0', 'end')
    else:
        answer="Predicted Sex is Female"
        answer_text.insert(tk.END, answer)
        answer_text.tag_configure('blue', foreground='blue')
        answer_text.tag_add('blue', '1.0', 'end')

    



# creates the window using Tk() fucntion
window = tk.Tk()

# this will listen to the close window event
window.protocol('WM_DELETE_WINDOW', close_window)

# creates title for the window
window.title('Spire Lab Voice Recorder')

# the icon for the application, this replaces the default icon
#window.iconbitmap(window, 'voice_recorder_icon.ico')

# dimensions and position of the window
window.geometry('500x450+440+180')
# makes the window non-resizable
window.resizable(height=FALSE, width=FALSE)


"""Styles for the widgets"""
# style for the label 
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 15))

# style for the entry
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))

# style for the button
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font='DotumChe')


# creates the canvas for containing all the widgets
canvas = Canvas(window, width=500, height=400)
canvas.pack()

# loading the logo
logo = PhotoImage(file='recorder.png')
# creates dimensions of the logo
logo = logo.subsample(2, 2)
# adding the logo to the canvas
canvas.create_image(240, 135, image=logo)


# creating a ttk label
duration_label = ttk.Label(window, text='Enter Recording Duration in Seconds:', style='TLabel')
name_label = ttk.Label(window, text='Enter your name:', style='TLabel')
#entry=Entry(window).pack()
# creating a ttk entry
duration_entry = ttk.Entry(window, width=76, style='TEntry')
name_entry = ttk.Entry(window, width=40, style='TEntry')

# adding the label to the canvas
canvas.create_window(235, 290, window=duration_label)
canvas.create_window(100,350,window=name_label)
# adding the entry to the canvas
canvas.create_window(250, 315, window=duration_entry)
canvas.create_window(325, 350, window=name_entry)


# creating the empty label for displaying download progress
progress_label = ttk.Label(window, text='')
# creating the button
record_button = ttk.Button(window, text='Record', style='TButton', command=recording_thread)

predict_button = ttk.Button(window, text='Predict Sex', style='TButton', command=predict_thread)

# adding the label to the canvas
canvas.create_window(250, 395, window=progress_label)
# adding the button to the canvas
canvas.create_window(120, 410, window=record_button)

canvas.create_window(375, 410, window=predict_button)




# this will run the main window infinetly
window.mainloop()