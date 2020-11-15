import wave
import pyaudio
import sys
import numpy as np

from matplotlib import pyplot as plt

CHUNK = 1024

filename = 'SuperMario.wav'
wf = wave.open(filename, 'rb')
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

buffer = wf.readframes(-1)
print(max(buffer),min(buffer))

# for i in range(4000):
#     stream.write(buffer[4096 * i:4096 * (i+1)])

# signal = np.frombuffer(buffer, dtype="int16")
# f_rate = wf.getframerate()
# time = np.linspace(0, len(signal) / f_rate, num=len(signal))
# plt.figure(figsize=(20,8))
# plt.title("Sound Wave")
# plt.xlabel("Time")
# plt.plot(time, signal, 'm')
# plt.show()
