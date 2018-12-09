import numpy as np
from scipy import signal
from Util.peak_detection import detect_peaks
from Util.peak_detection import _plot
rrt_signal = np.load("./Util/rrt1.npy")


def bandpass_filter(rrt_data, f1 = 0.2, f2 = 2, numtaps = 5, nyq = 50):
    filter = signal.firwin(numtaps, [f1, f2], pass_zero=False)


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



detect_peaks(filter_rrt_signal(rrt_signal), mpd=200 , show=False)