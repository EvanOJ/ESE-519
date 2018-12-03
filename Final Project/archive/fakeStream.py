
import time 

def readALL(inPath):
	import pandas as pd 
	import numpy as np
	inData = pd.read_csv(inPath)
	inData = np.array(inData)
	inData = inData[:,1] #just ekg data
	return inData

def fakeStream(dataItem,outPath):
	import csv
	outfile = open(outPath,'a')
	outfile.write(str(dataItem)+"\n")
	outfile.close()

	# print("Now Streaming: %s" %dataItem)

if __name__ == '__main__':


	fullData = readALL("C:/Users/EOJ/Desktop/matOut.csv")
	counter = 0
	lenCounter = 0
	freq = 120
	while ((counter <= freq) & (lenCounter<len(fullData))):
		if counter ==freq:
			counter = 0
			time.sleep(1) #upload 60 samples then pause for a second 
		else:
			counter += 1
			lenCounter +=1
			#print(fullData[lenCounter])	
			fakeStream(float(fullData[lenCounter]),"C:/Users/EOJ/Desktop/data_stream.csv")
		