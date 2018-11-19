import spidev
from time import sleep
import os
import math

spi = spidev.SpiDev()
spi.open(0,0)



def getReading(channel):
    rawData = spi.xfer([1,(8+channel)<<4,0])
    #last two positions of the second bit shifted over 8 places
    #with the rawData's 3rd bit attached at the end
    processedData = ((rawData[1] & 3) <<8)+rawData[2]
    return processedData

def accel(raw):
    val = raw/65535
    val -=0.5
    val = val*3.0
    return (val)
    
    
    
while True:
    rawX = getReading(0)
    rawY = getReading(1)
    rawZ = getReading(2)
    
    print "x: " + str(rawX)
    print "y: " + str(rawY)
    print "x: " + str(rawZ)
    sleep(.2)
    #percent = (raw/10.24)
    #volt = (percent/100.0)*3.3   
    #PCT = ",PCT={0:.2f}".format(percent)+"%"
    #VOLT = ",Volts={0:.2f}".format(volt)+"V"
    #print "Raw="+str(raw),PCT,VOLT
   
    

