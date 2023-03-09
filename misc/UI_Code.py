import pyaudio
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tensorflow.keras.models import load_model

# Load the pre-trained gender classification model
model = load_model("gender_classifier_model.h5")

# Define the audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = int(RATE/10)  # 100 ms

# Create the Tkinter window
window = tk.Tk()
window.title("Gender Prediction")
window.geometry("300x200")

# Create the GUI elements
gender_label = tk.Label(window, text="Predicted gender: ")
gender_label.pack(pady=10)

start_button = tk.Button(window, text="Start", width=10)
start_button.pack(pady=10)

stop_button = tk.Button(window, text="Stop", width=10)
stop_button.pack(pady=10)

save_button = tk.Button(window, text="Save", width=10)
save_button.pack(pady=10)

# Define the audio stream
p = pyaudio.PyAudio()
stream = None

# Define a function to start the audio stream
def start_stream():
    global stream
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    gender_label.configure(text="Listening...")

# Define a function to stop the audio stream
def stop_stream():
    global stream
    if stream is not None:
        stream.stop_stream()
        stream.close()
        stream = None

# Define a function to save the audio recording to a file
def save_recording():
    global audio_data
    if audio_data is None:
        messagebox.showerror("Error", "No audio data to save.")
    else:
        filename = tk.filedialog.asksaveasfilename(defaultextension=".wav")
        if filename:
            # Write the audio data to a WAV file
            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(audio_data)
            wf.close()
            messagebox.showinfo("Success", "Recording saved.")

# Define a function to predict the gender from the audio data
def predict_gender():
    global audio_data
    if audio_data is None:
        messagebox.showerror("Error", "No audio data to predict.")
    else:
        # Normalize the audio data
        audio = audio_data / 32768.0

        # Reshape the audio data to match the input shape of the model
        audio = audio.reshape(1, -1, 1)

        # Make the gender prediction
        prediction = model.predict(audio)

        # Determine the predicted gender
        if prediction[0][0] > prediction[0][1]:
            gender = "male"
        else:
            gender = "female"

        # Update the GUI with the predicted gender
        gender_label.configure(text=f"Predicted gender: {gender}")

# Define a variable to hold the audio data
audio_data = None

# Bind the start and stop buttons to their respective functions
start_button.configure(command=start_stream)
stop_button.configure(command=stop_stream)

# Bind the save and predict buttons to their respective functions
save_button.configure(command=save_recording)
window.bind("<Return>", lambda event: predict_gender())

# Start the Tkinter event loop
window.mainloop()

# Stop the audio stream when the window is closed
stop_stream()
p.terminate()
