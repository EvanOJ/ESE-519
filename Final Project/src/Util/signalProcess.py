import spidev
import time
from scipy.signal import find_peaks
from scipy import signal
import matplotlib.pyplot as plt
#from scipy.signal import
import sys
import os
import numpy as np
import pdb
#from ShareMemory.MemShare import ShareMemWriter

#add the package to the python directory
cur_path = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[0 : -1])
cur_path = os.path.join(cur_path, "ShareMemory")
sys.path.append(cur_path)
#from MemShare import ShareMemWriter
import time

class DataReader:

    def __init__(self):

        self.spi = spidev.SpiDev()

    def initADC(self, freq):
        self.spi.open(0, 0)
        self.spi.max_speed_hz = freq

    def ReadChannel(self, channel, spi):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def count_peaks(data, threshold = 480):
        count = 0
        flag = False
        for i in range(len(data)):
            if data[i] > 480 and not flag:
                flag = True
                count = count + 1
            if data[i] < 480 and flag:
                flag = False
        
        return count

    def moving_average(self, data, window):
        cumsum = np.cumsum(np.insert(data, 0, 0))
        return (cumsum[window:] - cumsum[:-window]) /float(window)

    def collectData(self , length, delay, ecg_window = 1, rr_window = 40):

        timeStart = time.time()

        ecgBuffer = []
        rrBuffer1 = []
        rrBuffer2 = []
        accelBuffer = []

        for i in range(length):
            ecgBuffer.append(self.ReadChannel(0, self.spi))
            accelBuffer.append(self.ReadChannel(1, self.spi))
            rrBuffer1.append(self.ReadChannel(2, self.spi))
            rrBuffer2.append(self.ReadChannel(3, self.spi))
            time.sleep(delay)
        duration = time.time() - timeStart

        #rrBuffer1 = self.moving_average(np.array(rrBuffer1), rr_window)
        rrBuffer2 = self.moving_average(np.array(rrBuffer2), rr_window)

        #rrBuffer1 = rrBuffer1.tolist()
        rrBuffer2 = rrBuffer2.tolist()
        return (ecgBuffer, accelBuffer, rrBuffer1, rrBuffer2, duration)

class DataProcessor:

    def __init__(self, duration):
        self.duration = duration
        self.buffer = None
        self.peaks = None
        self.BPM = None

    def count_peaks(self, data, threshold = 400):
        count = 0
        flag = False
        for i in range(len(data)):
            if data[i] > threshold and not flag:
                flag = True
                count = count + 1
            if data[i] < threshold and flag:
                flag = False
        self.peaks = np.arange(count)

    def findPeaks(self, dataBuffer, height = 0, threshold = 0, distance = 1):

        peaks, _ = find_peaks(dataBuffer, height = height, threshold = threshold, distance = distance)
        self.peaks = peaks
        return peaks


    def calcBPM(self):

        BPM = len(self.peaks) / self.duration
        self.BPM = BPM
        return self.BPM


def main():
    fig = plt.figure("1")
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    dr = DataReader()
    dr.initADC(1000000)
    data = []
    print("start")
    tic = time.time()
    for i in range(1):
        ecg,accel,rr1,rr2,duration = dr.collectData(6000,0.01)
        print(len(data))
        print(len(rr1))
        data.extend(rr1)
        dp_ecg = DataProcessor(duration)
        dp_accel = DataProcessor(duration)
        dp_rr1 = DataProcessor(duration)
        dp_rr2 = DataProcessor(duration)

        ecgPeaks = dp_ecg.findPeaks(ecg,0)
        accelPeaks = dp_accel.findPeaks(accel,0)
        #rr1Peaks = dp_rr1.findPeaks(rr1,0, distance = 50)
        rr1Peaks = dp_rr1.count_peaks(rr1)
        rr2Peaks = dp_rr2.findPeaks(rr2,0)

        agitation = dp_accel.calcBPM()
        ecgRate = dp_ecg.calcBPM()
        rr1Rate = dp_rr1.calcBPM()
        rr2Rate = dp_rr2.calcBPM()
        print(ecgRate,agitation,rr1Rate,rr2Rate)
    data = np.array(data)
    np.save("rrt1", data)
   # window = signal.general_gaussian(51, p = 0.5, sig = 20)
   # filtered = signal.fftconvolve(window, data)
   # filtered = np.average(data) /np.average(filtered) * filtered
   # filtered = np.roll(filtered, -25)
    #peaks2 = find_peaks(filtered)
   # print(data)
    data_fft = np.abs(np.fft.fft(data))
    print(data_fft)
    numtaps = 3
    f = 0.1
    fil = signal.firwin(numtaps, f)
    data3 = np.convolve(data, fil, 'same') 
    toc = time.time()
    print("time", toc - tic)
   # print(data_fft)
   # data_fft[3:] = 0
    #smoothed = np.fft.irfft(data_fft)
    #print(np.arange(data.shape[0]))
    #pdb.set_trace()
    ax1.plot(np.arange(data.shape[0]),data, 'r')
    ax2.plot(100 /np.arange(data_fft.shape[0]), data_fft)
    ax3.plot(data3)
    plt.show()
if __name__ =="__main__":
    main()


