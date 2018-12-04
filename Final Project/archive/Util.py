import spidev
import time
from scipy.signal import find_peaks

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

    def collectData(self , length, delay):

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
        return (ecgBuffer, accelBuffer, rrBuffer1, rrBuffer2, duration)

class DataProcessor:

    def __init__(self, duration, ):


    def findPeaks(dataBuffer, height):

        peaks, _ = find_peaks(dataBuffer, height=height)
        return peaks


    def calcBPM(dataBuffer, duration, peaks):
        BPM = len(peaks) / duration
        return BPM
