'''
    Read wav file and record
'''
#import RPi.GPIO as GPIO

import wave
import pyaudio
import sys
import numpy as np
import json
from threading import Thread
from time import sleep
import time
from matplotlib import pyplot as plt
from cpufreq import cpuFreq

# RPI ZONE

import RPi.GPIO as GPIO
import time
import random
import math
GPIO.setmode(GPIO.BOARD)

PIN_CLK = 3
PIN_DATA = 5
PIN_CLR = 7

PIN_BIT0 = 37
PIN_BIT1 = 35
PIN_BIT2 = 33
PIN_CLK_BIT = 31

GPIO.setwarnings(False)
GPIO.setup(PIN_CLK, GPIO.OUT)
GPIO.setup(PIN_DATA, GPIO.OUT)
GPIO.setup(PIN_CLR, GPIO.OUT)
GPIO.setup(PIN_BIT0, GPIO.IN)
GPIO.setup(PIN_BIT1, GPIO.IN)
GPIO.setup(PIN_BIT2, GPIO.IN)
GPIO.setup(PIN_CLK_BIT, GPIO.IN)


def send_clk():
    GPIO.output(PIN_CLK, True)
    GPIO.output(PIN_CLK, False)


def send_clr():
    GPIO.output(PIN_CLR, True)
    GPIO.output(PIN_CLR, False)


SAMPLE_RATE = 8000
cpu = cpuFreq()
freqs = cpu.get_frequencies()
DELAY_TIME = freqs[0]/SAMPLE_RATE

# END OF RPI ZONE

JSON = open('song_list.json',)

filename = json.load(JSON)['song']

# print(filename)

JSON.close()

# constant variable
CHUNK = 1024
SAMPLE_fORMAT = pyaudio.paInt16
BITREAD = 16

# stop thread when program stop !
stop_all_thread = False

# global variable
PROGRAM_RUN = True
fs = 44100
wf = None
music_is_play = False
music_is_run = False
current_index = 0
p0 = p1 = p2 = b0 = b1 = b2 = None

N_SONG = len(filename)


def send_data_bit_thread():
    wf.rewind()
    buffer = wf.readframes(1)
    print(wf.getnchannels())
    c = 0
    while buffer != '':

        if stop_all_thread:
            return
        # if music_is_play and music_is_run:
        _16bits = int.from_bytes(buffer, byteorder='little')
        # print(_16bits)
        # send_time = time.time()
        stack = ""
        for i in range(16):
            GPIO.output(PIN_DATA, _16bits & 1)
            #stack += bin(_16bits)[-1]
            _16bits >>= 1
            send_clk()  # send clock to FPAG
        buffer = wf.readframes(1)
        # 8000: 0.00001
        # time.sleep(0.000005)
        #print("Sended:", stack[::-1])
        # print('send_time  :', time.time() - send_time)

        # buffer = wf.readframes(1)

        # if time.time() - test_time > 0.05:
        #     break


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

        if music_is_play and music_is_run:
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


def song_start():
    global wf
    global music_is_play
    global music_is_run

    try:
        wf = wave.open(r'./music/' + filename[current_index], 'rb')
    except:
        print("ERROR : can't open file")
    else:
        music_is_play = True
        music_is_run = True
        # thread_for_play_sound = Thread(target=play_sound_thread)
        # thread_for_play_sound.start()
        thread_for_send_data = Thread(target=send_data_bit_thread)
        thread_for_send_data.start()


def terminal():
    global p0
    global p1
    global p2
    global b0
    global b1
    global b2
    while PROGRAM_RUN:
        # input from terminal
        if stop_all_thread:
            return

        try:
            inp = input("State plz : ")
            b2, b1, b0 = tuple(map(int, inp.split()))
        except:
            print("ERROR : input fail plz try again.")
            continue

        if stop_all_thread:
            return

        if (p2, p1, p0) == (b2, b1, b0):
            print('same as previous command.')
            continue

        p2, p1, p0 = b2, b1, b0


if __name__ == "__main__":
    print(1/DELAY_TIME)
    PROGRAM_RUN = True
    send_clr()
    p2 = p1 = p0 = -1  # set_prev_state -> -1

    terminal_thread = Thread(target=terminal)
    terminal_thread.start()

    pi_clock = 0
    io_0 = io_1 = io_2 = 0
    b0 = b1 = b2 = 0
    one_shot_time = time.time()
    while PROGRAM_RUN:

        if GPIO.input(PIN_CLK_BIT) and time.time() - one_shot_time > 0.35:
            one_shot_time = time.time()
            io_0 = GPIO.input(PIN_BIT0)
            io_1 = GPIO.input(PIN_BIT1)
            io_2 = GPIO.input(PIN_BIT2)

            p2, p1, p0 = b2, b1, b0
            b2, b1, b0 = io_2, io_1, io_0

        if (b2, b1, b0) == (0, 0, 0):
            continue

        elif (b2, b1, b0) == (0, 0, 1):  # send data bit to Raspi..
            if not music_is_play and not music_is_run:
                song_start()
            elif music_is_run and not music_is_play:
                sleep(0.5)
                music_is_play = True

        elif (b2, b1, b0) == (0, 1, 0):
            if music_is_run and music_is_play:
                music_is_play = False
                send_clr()

        elif (b2, b1, b0) == (0, 1, 1):
            current_index = (current_index + 1) % N_SONG
            stop_all_thread = True
            sleep(1.0)
            stop_all_thread = False
            song_start()

        elif (b2, b1, b0) == (1, 0, 0):
            current_index = (current_index - 1) % N_SONG
            stop_all_thread = True
            sleep(1.0)
            stop_all_thread = False
            song_start()

        elif (b2, b1, b0) == (1, 0, 1):
            pass
        elif (b2, b1, b0) == (1, 1, 0):
            pass
        elif (b2, b1, b0) == (1, 1, 1):
            pass

        elif (b2, b1, b0) == (2, 2, 2) or b2 >= 2:  # for exit while true
            PROGRAM_RUN = False
            break
        else:
            print("ERROR : input fail plz try again.")

    stop_all_thread = True
    print('Exit program !')
    exit(0)

# 0 -> idle
# 1 -> play
# 2 -> stop
# 3 -> next
# 4 -> prev
# 5 ->
# 6 ->
# 7 ->
