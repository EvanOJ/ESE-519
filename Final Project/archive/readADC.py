import spidev
import time
import os

#import RPi.GPIO as GPIO
# #initialize GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(18,GPIO.OUT)
# pwm = GPIO.PWM(18,1000)

#initialize SPI to read ADC values
def initSPI(freq):
	'''Initializes the RPi SPI. Args: spi max speed hz.'''
	spi = spidev.SpiDev()
	spi.open(0,0)
	spi.max_speed_hz = freq

def ReadChannel(channel):
	'''Get value from a particular channel on the ADC. Returns that value.'''
	adc = spi.xfer2([1,(8 + channel)<<4,0])
	data = ((adc[1]&3)<<8) + adc[2]
	return data

def convertVolts(data,places):
	'''Obsolete.'''
	volts = (data * 3.3)/ float(1023)
	volts = round(volts,places)
	return volts

# ecg_channel = 0
# accel1_channel = 1
# accel2_channel = 2

#zChannel = 0
#yChannel = 1
#xChannel = 2

# delay = 1

# while True:
#     ecg_raw = ReadChannel(ecg_channel)
#     accel1_raw = ReadChannel(accel1_channel)
#     accel2_raw = ReadChannel(accel2_channel)

#     # ecg_volt = convertVolts(ecg_raw,2)
#     # accel1_volt = convertVolts(accel1_raw,2)
#     # accel2_volt = convertVolts(accel2_raw,2)

#    # X = ReadChannel(xChannel)
#    # xVolt = convertVolts(X,2)
#    # Y = ReadChannel(yChannel)
#    # yVolt = convertVolts(Y,2)
#    # Z = ReadChannel(zChannel)
#    # zVolt = convertVolts(Z,2)

#    # print(X,xVolt,Y,yVolt,Z,zVolt)
#     print(ecg_raw,ecg_volt,accel1_raw,accel1_volt,accel2_raw,accel2_volt)
    

#     time.sleep(delay)
