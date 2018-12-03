def initADC(freq):
    import spidev
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = freq
    return spi


def ReadChannel(channel, spi):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


def collectData(spi, length, delay):
    import time
    timeStart = time.time()

    ecgBuffer = []
    rrBuffer1 = []
    rrBuffer2 = []
    accelBuffer = []

    for i in range(length):
        ecgBuffer.append(ReadChannel(0, spi))
        accelBuffer.append(ReadChannel(1, spi))
        rrBuffer1.append(ReadChannel(2, spi))
        rrBuffer2.append(ReadChannel(3, spi))
        time.sleep(delay)
    duration = time.time() - timeStart
    return (ecgBuffer, accelBuffer, rrBuffer1, rrBuffer2, duration)


def findPeaks(dataBuffer, height):
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(dataBuffer, height=height)
    return peaks


def calcBPM(dataBuffer, duration, peaks):
    BPM = len(peaks) / duration
    return BPM


def main():
	import time
	spi = initADC(1000000)

	ecg,accel,rr1,rr2,duration = collectData(spi,60,0.1)
	ecgPeaks = findPeaks(ecg,0)
	accelPeaks = findPeaks(accel,0)
	rr1Peaks = findPeaks(rr1,0)
	rr2Peaks = findPeaks(rr2,0)
	agitation = calcBPM(accel,duration,accelPeaks)
	ecgRate = calcBPM(ecg,duration,ecgPeaks)
	rr1Rate = calcBPM(rr1,duration,rr1Peaks)
	rr2Rate = calcBPM(rr2,duration,rr2Peaks)
	print(ecgRate,agitation,rr1Rate,rr2Rate)

if __name__ =="__name__":
	main()
	

