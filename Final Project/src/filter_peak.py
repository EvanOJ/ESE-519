import numpy as np
from scipy import signal
from Util.peak_detection import detect_peaks
from Util.peak_detection import _plot
rrt_signal = np.load("./Util/rrt1.npy")


def fourier_filter(rrt_data):
    rrt_fourier = np.abs(np.fft.fft())

def filter_rrt_signal(rrt_data, kernel_size = 4):
    rrt_data = np.convolve(rrt_data, np.ones(kernel_size) / kernel_size, mode = 'valid')
    return rrt_data

'''
import matplotlib.pyplot as plt
t = rrt_signal
sp = np.fft.fft(t)
freq = np.fft.fftfreq(t.shape[-1])
print(t.shape[-1])
print(freq)
plt.plot(freq, sp.real)

plt.show()
'''



detect_peaks(filter_rrt_signal(rrt_signal),mpd=200,show=False)