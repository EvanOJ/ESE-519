import numpy as np 

#generate random test data in the right ranges
from random import randint
fakeECG =[randint(50,100) for p in range(0,500)]
fakeRR =[randint(10,30) for p in range(0,500)]
fakeACCEL =[randint(0,10) for p in range(0,500)]


def mapRange(value,Amin,Amax,Bmin,Bmax):
	if value >= Amax:
		value = Amax
	elif(value <= Amin):
		value = Amin
	
    # aSpan = Amax - Amin
	# bSpan = Bmax - Bmin
	# scaled = float(value - aSpan)/float(aSpan)
	# return bSpan + (scaled * bSpan)

	interp = interp1d([Amin,Amax],[Bmin,Bmax])
	return(interp(value))

def main():
	running = True
	calibrating = True
	warmingUp = True

	feedbackCounter = 0
	processCounter = 0
	feedbackWindow = 6
	processWindow = 10
	calibPeriod = 100

	#haptic period
	#visual period
	#fixed/static for now

	#data buffers for feedback processing
	ecgBuffer = []
	rrBuffer = []
	accelBuffer = []

	#standard baselines, ideally this is calculated from first buffer, static for now
	# ecgSTD = 75
	# rrSTD = 20
	# accelSTD = 1
	ecgSTD = 0
	rrSTD = 0
	accelSTD = 0

	#for using fake data only
	fakeIndex = 0

	#cumulative output data storage
	outputECG = []
	outputRR = []
	outputACCEL = []

	while running:
		print("Warming up...")

		#warm up period for the device to settle
		while warmingUp:
			if processCounter < 100:
				processCounter += 1
			else:
				warmingUp = False
		print("Device warmed up.\n")
		print("Calibrating...")

		#calibration period to establish baseline data
		while calibrating:

			#collect baseline data
			if processCounter < calibPeriod:
				#collect data from sensors and append to temporary data buffers
				ecgBuffer.append(fakeECG[fakeIndex])		#bpm values, not raw ECG
				rrBuffer.append(fakeRR[fakeIndex])
				accelBuffer.append(fakeACCEL[fakeIndex])
				processCounter += 1
				print(processCounter)

			else:
				#calculate the baseline values for the calibration period to use as baseline for free-running analysis moving forward
				ecgSTD = np.mean(ecgBuffer)
				rrSTD = np.mean(rrBuffer)
				accelSTD = np.mean(accelBuffer)

				#append buffer to the cumulative output data file
				outputECG.extend(ecgBuffer)
				outputRR.extend(rrBuffer)
				outputACCEL.extend(accelBuffer)
				
				#clear out the buffers
				ecgBuffer = []
				rrBuffer = []
				accelBuffer = []

				#end calibration period
				calibrating = False

				#reset process counter
				processCounter = 1
		print("Calibration finished.\n")
		#proceed to running real-time analysis and feedback 
		if processCounter < processWindow:

			if feedbackCounter < feedbackWindow:
				#collect data from sensors and append to temporary data buffers
				ecgBuffer.append(fakeECG[fakeIndex])		#bpm values, not raw ECG
				rrBuffer.append(fakeRR[fakeIndex])
				accelBuffer.append(fakeACCEL[fakeIndex])

				#increment next haptic feedback value
				#increment next visual feedback value 

				fakeIndex += 1
				feedbackCounter += 1
			else:
				print("Recalculating feedback data")

				#visualFeedback = mapRange(bpm,50,100,1500,7000)


				#append buffer to the cumulative output data file
				outputECG.extend(ecgBuffer)
				outputRR.extend(rrBuffer)
				outputACCEL.extend(accelBuffer)

				#process the buffers into haptic and visual feedback

				#clear out the buffers
				ecgBuffer = []
				rrBuffer = []
				accelBuffer = []

				#reset feedback counter
				feedbackCounter = 0

				#inrement process counter
				processCounter += 1
		else:

			running = False

	print(len(outputECG))


main()
#main loop

	#feedbackCounter = 0
	#processCounter = 10 seconds ? how many ticks from this?
	#feedbackWindow = 6
	#processWindow = 10

	#haptic period
	#visual period 

	#ecgBuffer = []
	#rrBuffer = []
	#accelBuffer = []

	#outputDataECG = []
	#outputDataACCEL = []
	#outputDataRR = []

	#if feedbackCounter < feedbackWindow:
		#gather data from sensors

		#processing loop 1 per time step
		#get data from acceleromoeter & append to accelBuffer
		#get data from ecg & append to ecgBuffer
		#get data from rr and append to rrBuffer

		#toggle haptic feedback voltage, pwm freq @ hapticFeedback period
		#trigger visual feedback color change @ visualFeedback period

		#increment next haptic value for feedback
		#increment next visual feedback value

	#else
		#recalculate the next 6 feedback values 

		#while processCounter < processWindow

			#feedback loop 6 time steps, 10 seconds each, 1minute loop to update

			#function(ecgBuffer,accelBuffer,rrBuffer):
				#return the next 6 mapped values used by feedback processes
			#visual feedback values/colors = [] #6 values
			#haptic feeedback values = [] #6 values, PWM ?

			#processCounter += 1
		
		#processCounter = 0
		#ecgBuffer append to outputDataECG
		#accelBuffer append to outputDataACCEL
		#rrBuffer append to outputDataRR

	#write all outputdata to csv
	
	#exit



		
