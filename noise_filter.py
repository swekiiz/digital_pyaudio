import sounddevice as sd
import numpy as np

duration = 200


def print_sound(indata, outdata, frames, time, status):
    l = indata[::8]
    print(*l)


with sd.Stream(callback=print_sound, channels=1):
    sd.sleep(100000000000000000)
