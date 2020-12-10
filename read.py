'''
    Read wav file and record
'''
#import RPi.GPIO as GPIO

import wave
import pyaudio
import sys
import numpy as np
from threading import Thread
from time import sleep
import time
from matplotlib import pyplot as plt

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)

# constant variable
CHUNK = 1024
SAMPLE_fORMAT = pyaudio.paInt16
BITREAD = 16

# stop thread when program stop !
stop_all_thread = False

# global variable
fs = 44100
filename = 'SuperMarioMono.wav'
wf = None


def setup_pin():
    # print('setup pin')
    # for x in led_lst:
    #     GPIO.setup(x, GPIO.OUT, initial=GPIO.HIGH)
    pass


def send_data_bit_thread():
    wf.rewind()
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    frames_per_buffer=CHUNK,
                    output=True)

    buffer = wf.readframes(1)
    test_time = time.time()
    while buffer != '':

        if stop_all_thread:
            stream.close()
            p.terminate()
            return

        _16bits = int.from_bytes(buffer, byteorder='big')

        # send_time = time.time()

        for i in range(16):
            if _16bits & 1 == 1:
                pass
                # GPIO.output(led_lst[n], GPIO.HIGH)
            else:
                pass
                # GPIO.output(led_lst[n], GPIO.LOW)
            _16bits >>= 1

        # print('send_time  :', time.time() - send_time)

        # stream.write(buffer)
        # buffer = wf.readframes(1)

        # if time.time() - test_time > 0.05:
        #     break

    # terminate all
    stream.close()
    p.terminate()


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

        if stop_all_thread:
            stream.close()
            p.terminate()
            return
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
    setup_pin()

    while PROGRAM_RUN:

        # input from terminal
        try:
            inp = input("State plz : ")
            b2, b1, b0 = tuple(map(int, inp.split()))
        except:
            print("ERROR : input fail plz try again.")
            continue

        if (b2, b1, b0) == (0, 0, 0):  # play sound on computer
            try:
                wf = wave.open(r'./music/' + filename, 'rb')
            except:
                print("ERROR : can't open file")
            else:
                thread_for_play_sound = Thread(target=play_sound_thread)
                thread_for_play_sound.start()

        elif (b2, b1, b0) == (0, 0, 1):  # send data bit to Raspi..
            try:
                wf = wave.open(r'./music/' + filename, 'rb')
            except:
                print("ERROR : can't open file")
            else:
                thread_for_send_data = Thread(target=send_data_bit_thread)
                thread_for_send_data.start()

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

    stop_all_thread = True
    print('Exit program !')
    exit(0)
