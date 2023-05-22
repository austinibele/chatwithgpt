import numpy as np
import tkinter as tk
from tkinter import ttk
import pygame
from PIL import Image, ImageTk
import sounddevice as sd
from scipy.io.wavfile import write
from threading import Thread
from src.transcribe import transcribe
from src.chatbot import Chatbot
from src.text_to_speech import text_to_speech
import soundfile as sf
import numpy as np

# initialize pygame mixer
pygame.mixer.init()

class Recorder:
    def __init__(self):
        self.blocks = []
        self.recording = False
        self.stream = None

    def start_recording(self):
        # Callback function to save the recorded data into a NumPy array
        def callback(indata, frames, time, status):
            self.blocks.append(indata.copy())

        self.recording = True
        self.blocks.clear()  # Clear any previous recording
        # Create a stream object
        self.stream = sd.InputStream(callback=callback, channels=1, samplerate=44100)
        self.stream.start()
        print("Recording started.")

    def stop_recording(self):
        if self.recording:
            self.stream.stop()
            self.stream.close()
            recording_array = np.concatenate(self.blocks)
            write("tmp/recording.wav", 44100, recording_array) 
            # Load the .wav file
            data, samplerate = sf.read('tmp/recording.wav')
            # Convert to 16 bit PCM
            data = np.int16(data/np.max(np.abs(data)) * 32767)
            # Save the .wav file in 16 bit PCM format
            sf.write('tmp/recording.wav', data, samplerate, subtype='PCM_16')

            print("Recording stopped and saved.")
        else:
            print("You are not recording right now.")


class ImageLabel(tk.Label):
    """A label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in range(1000):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError: pass

        try: self.delay = im.info['duration']
        except: self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.recorder = Recorder()
        self.create_widgets()
        self.chatbot = Chatbot()

    def create_widgets(self):
        self.master.geometry('300x300')

        self.start = ttk.Button(self, text="RECORD", command=self.start_recording)
        self.start.pack(pady=10)

        self.stop = ttk.Button(self, text="STOP", command=self.stop_recording)
        self.stop.pack(pady=10)

        self.send = ttk.Button(self, text="SEND", command=self.send_recording)
        self.send.pack(pady=10)

        # Load an animated GIF
        self.indicator = ImageLabel(self)
        self.indicator.pack(pady=10)

    def start_recording(self):
        Thread(target=self.recorder.start_recording).start()  
        self.indicator.load('assets/recording.gif')  # Load and play the GIF

    def stop_recording(self):
        self.recorder.stop_recording()  
        self.indicator.unload()  # Stop the GIF

    def send_recording(self):
        transcription = transcribe()
        recording = self.chatbot.send_message(transcription)
        text_to_speech(text=recording)
        pygame.mixer.music.load('tmp/response.wav')  # load the audio file
        pygame.mixer.music.play(loops=0)  # play the audio file  


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
