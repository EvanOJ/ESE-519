from hapticFeedback import *
from signalProcess import *
import time

class monitor():
	def __init__(self,prevState,currState,prevECG,prevACCEL,prevRR1,prevRR2,currECG,currACCEL,currRR1,currRR2,ecgDT,accelDT,rrDT):
		self.prevState = prevState
		self.currState = currState
		self.prevECG = prevECG
		self.prevACCEL = prevACCEL
		self.prevRR = (prevRR1 + prevRR2)/2
#		self.prevRR1 = prevRR1
#		self.prevRR2 = prevRR2
		self.currECG = currECG
		self.currACCEL = currACCEL
		self.currRR = (currRR1 + currRR2)/2
#		self.currRR1 = currRR1
#		self.currRR2 = currRR2
	def updateVals(self,ecg,accel,rr1,rr2):
		self.prevECG = self.currECG
		self.prevACCEL = self.currACCEL
		self.prevRR = self.currRR
		self.currECG = ecg
		self.currACCEL = accel
		self.currRR = (rr1+rr2)/2
	def updateState(self,state):
		self.prevState = self.currState
		self.currState = state
	def checkProgression(self):
		self.ecgDT = (self.currECG - self.prevECG)/self.currECG
		self.accelDT = (self.currACCEL - self.prevACCEL)/self.currACCEL
		self.rrDT = (self.currRR - self.prevRR)/self.currRR
		

def calcRates(ecg,accel,rr1,rr2,duration):
	ecgPeaks = findPeaks(ecg,0)
	accelPeaks = findPeaks(accel,0)
	rr1Peaks = findPeaks(rr1,0)
	rr2Peaks = findPeaks(rr2,0)

	agitation = calcBPM(accel,duration,accelPeaks)
	ecgRate = calcBPM(ecg,duration,ecgPeaks)
	rr1Rate = calcBPM(rr1,duration,rr1Peaks)
	rr2Rate = calcBPM(rr2,duration,rr2Peaks)

	return (ecgRate,agitation,rr1Rate,rr2Rate)

def main():
	#initialize adc
	spi = initADC(1000000)
	#initialize haptic feedback
	buzzer1 = Haptic(13,1,50)
	buzzer2 = Haptic(18,1,50)
	buzzer1.stopPWM()
	buzzer2.stopPWM()


	#initialize the monitor
	patient = monitor(-1,-1,0,0,0,0,0,0,0,0,0,0,0)

	#set monitor parameters
	analysisPeriod = 60 #roughly corresponds to 60 seconds worth of data
	samplingDelay = 0.1 #seconds between adc readings, to avoid noise and get clean peaks

	#warmup period, 5 seconds####################################################################################
	while patient.currState == -1:
		print("Warming up...")
		time.sleep(5)
		#increment state to baseline collection
		patient.updateState(0)
	#wait for button press, mouseclick, etc.#####################################################################
	#collect baseline data, state 0
	print("Collecting baseline data for {period} seconds.".format(period=analysisPeriod*samplingDelay))
	while patient.currState == 0:
		ecg,accel,rr1,rr2,duration = collectData(spi,analysisPeriod,samplingDelay)
		ecgRate,agitation,rr1Rate,rr2Rate  = calcRates(ecg,accel,rr1,rr2,duration)
#		patient.ECG,patient.ACCEL,patient.RR1,patient.RR2 = calcRates(ecg,accel,rr1,rr2,duration)
#		rrAvg = (rr1Rate + rr2Rate)/2
		#check for movement toward next state 0-10% decrease ecg,rr,accel
		patient.updateVals(ecgRate,agitation,rr1Rate,rr2Rate)
		#initialize the haptic feedback to match the baseline BPM
		buzzer1.startPWM()
		buzzer2.startPWM()
		buzzer1.changeFreq(ecgRate)
		buzzer2.changeFreq(ecgRate)
		
		#increment to next state
		patient.updateState(1)
	print("Baseline data collected. ECG = {ecg}, Agitation={agitation}, Respiratory ={respiratory}".format(ecg=patient.currECG,agitation=patient.currACCEL,respiratory=patient.currRR))

	#begin meditation############################################################################################
	print("Now entering state {currState}. Meditate toward state {nextState}".format(currState = patient.currState, nextState =patient.currState+1))	
	while patient.currState == 1:
		ecg,accel,rr1,rr2,duration = collectData(spi,analysisPeriod,samplingDelay)
		ecgRate,agitation,rr1Rate,rr2Rate  = calcRates(ecg,accel,rr1,rr2,duration)
		patient.updateVals(ecgRate,agitation,rr1Rate,rr2Rate)
                
		patient.checkProgression()
		#check for progression to Pre-meditation routine
		print(patient.ecgDT,patient.accelDT,patient.rrDT)
		if(((patient.ecgDT<0)&(patient.ecgDT>=-0.1)) & ((patient.accelDT<0)&(patient.accelDT>=-0.1)) & ((patient.rrDT<0)&(patient.rrDT>=-0.1))):
			print("Proceeding to Pre-meditation routine")
			patient.updateState(2)
			buzzer1.cleanup()
		else:
			print(patient.currState)
			print(patient.ecgDT,patient.accelDT,patient.rrDT)
			
#		patient.updateState(2)		
	#temporary. testing only so buzzer doesnt continue for ever
#	buzzer1.cleanup() #only need to cleanup one and cleans up all gpio

main()
