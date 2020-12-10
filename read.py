'''
    Read wav file and record
'''

import wave
import pyaudio
import sys
import numpy as np
from threading import Thread
import time
from time import sleep
from matplotlib import pyplot as plt

# constant variable
CHUNK = 1024
SAMPLE_fORMAT = pyaudio.paInt16
BITREAD = 16

# global variable
fs = 44100
filename = 'SuperMario.wav'
wf = None


def play_sound_thread():
    wf.rewind()
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    frames_per_buffer=CHUNK,
                    output=True)

    loop_start_time = time.time()
    data = wf.readframes(CHUNK)

    # Enable if you want to set second
    # second = 10
    # for i in range(0, int(fs / CHUNK * second)):
    #     stream.write(data)
    #     data = wf.readframes(CHUNK)

    # while song isn't end
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    loop_end_time = time.time()
    print("This song have been play with : ",
          loop_end_time - loop_start_time, 'second')
    # terminate all
    stream.close()
    p.terminate()


# ----- bug ----- #
def show_wave_thread():
    buffer = wf.readframes(-1)
    signal = np.frombuffer(buffer, dtype="int16")
    f_rate = wf.getframerate()
    t = np.linspace(0, len(signal) / f_rate, num=len(signal))
    plt.figure(figsize=(20, 8))
    plt.title("Sound Wave")
    plt.xlabel("Time")
    plt.plot(t, signal, 'm')
    plt.show()


if __name__ == "__main__":
    PROGRAM_RUN = True
    while PROGRAM_RUN:
        try:
            inp = input("State plz : ")
            b2, b1, b0 = tuple(map(int, inp.split()))
        except:
            print("ERROR : input fail plz try again.")
            continue
        if (b2, b1, b0) == (0, 0, 0):  # play sound
            try:
                wf = wave.open(filename, 'rb')
            except:
                print("ERROR can't open file")
            else:
                thread_for_play_sound = Thread(target=play_sound_thread)
                thread_for_play_sound.start()
        elif (b2, b1, b0) == (0, 0, 1):
            pass
        elif (b2, b1, b0) == (0, 1, 0):
            pass
        elif (b2, b1, b0) == (0, 1, 1):
            pass
        elif (b2, b1, b0) == (1, 0, 0):
            pass
        elif (b2, b1, b0) == (1, 0, 1):
            pass
        elif (b2, b1, b0) == (1, 1, 0):
            pass
        elif (b2, b1, b0) == (1, 1, 1):
            pass
        elif (b2, b1, b0) == (2, 2, 2):  # for exit while true
            PROGRAM_RUN = False
        else:
            print("ERROR : input fail plz try again.")
    print('Exit program !')
    exit()
