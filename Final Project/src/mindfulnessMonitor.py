from hapticFeedback import Haptic
import pdb

from Util.signalProcess import DataReader
from Util.signalProcess import DataProcessor
import os
import time
import sys

#add the package to the python directory
cur_path = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[0 : -1])
cur_path = os.path.join(cur_path, "ShareMemory")
sys.path.append(cur_path)
from MemShare import ShareMemWriter

class monitor(object):
    def __init__(self,prevState,currState,prevECG,prevACCEL,prevRR1,prevRR2,currECG,currACCEL,currRR1,currRR2):

        self.prevState = prevState
        self.currState = currState
        self.prevECG = prevECG
        self.prevACCEL = prevACCEL
        self.prevRR = (prevRR1 + prevRR2)/2
        self.currECG = currECG
        self.currACCEL = currACCEL
        self.currRR = (currRR1 + currRR2)/2


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
        self.accelDT = (self.currACCEL - self.prevACCEL)/(self.currACCEL + 0.0001) #avoid division 0
        self.rrDT = (self.currRR - self.prevRR)/self.currRR


class Patient_monitor(monitor):

    def __init__(self, prevState, currState, prevECG, prevACCEL, prevRR1, prevRR2, currECG, currACCEL, currRR1, currRR2, analysisPeriod = 60, samplingDelay = 0.1):

        super().__init__(prevState, currState, prevECG, prevACCEL, prevRR1, prevRR2, currECG, currACCEL, currRR1, currRR2)
        self.buzzer1 = Haptic(13, 1, 50)
        self.buzzer2 = Haptic(18, 1, 50)
        #self.share_mem = Sharem
        self.dr = DataReader()
        # set monitor parameters
        self.analysisPeriod = analysisPeriod  # roughly corresponds to 60 seconds worth of data
        self.samplingDelay = samplingDelay  # seconds between adc readings, to avoid noise and get clean peaks
        self.baseline_ecg = None
        self.baseline_rr = None
        self.baseline_accel = None

        self.target_ecg = None
        self.target_rr = None
        self.target_accel = None

        self.calibrate()

    def calibrate(self):
        # initialize adc

        self.dr.initADC(1000000)
        # initialize haptic feedback
        self.buzzer1.stopPWM()
        self.buzzer2.stopPWM()

    def update_baseline(self):
        #update the baseline value from the current state value
        self.baseline_ecg = self.currECG
        self.baseline_accel = self.currACCEL
        self.baseline_rr = self.currRR



    def checkProgression(self):

        self.ecgDT = (self.currECG - self.baseline_ecg) / self.baseline_ecg
        self.accelDT = (self.currACCEL - self.baseline_accel) / (self.baseline_accel + 0.0001)  # avoid division 0
        self.rrDT = (self.currRR - self.baseline_rr) / self.baseline_rr

    def warm_up(self, time_warmup):

        while self.currState == -1:
            print("Warming up...")
            time.sleep(5)
            # increment state to baseline collection
            self.updateState(0)
            # wait for button press, mouseclick, etc.#####################################################################
            # collect baseline data, state 0


    def collect_baseline(self):
        
        print("Collecting baseline data for {period} seconds.".format(period=self.analysisPeriod * self.samplingDelay))
        while self.currState == 0:
            ecg, accel, rr1, rr2, duration = self.dr.collectData(self.analysisPeriod, self.samplingDelay)
            ecgRate, agitation, rr1Rate, rr2Rate = calcRates(ecg, accel, rr1, rr2, duration)

            #		patient.ECG,patient.ACCEL,patient.RR1,patient.RR2 = calcRates(ecg,accel,rr1,rr2,duration)
            #		rrAvg = (rr1Rate + rr2Rate)/2
            # check for movement toward next state 0-10% decrease ecg,rr,accel
            self.updateVals(ecgRate, agitation, rr1Rate, rr2Rate)
            #update the base line
            self.update_baseline()
            # initialize the haptic feedback to match the baseline BPM
            self.buzzer1.startPWM()
            self.buzzer2.startPWM()
            self.buzzer1.changeFreq(ecgRate)
            self.buzzer2.changeFreq(ecgRate)

            # increment to next state
            self.updateState(1)

        print("Baseline data collected. ECG = {ecg}, Agitation={agitation}, Respiratory ={respiratory}".format(
            ecg=self.currECG, agitation=self.currACCEL, respiratory=self.currRR))

    def updateTarget(self, state):
        if state == 1:
            self.target_ecg = int(self.baseline_ecg * (1 - 0.05))
            self.target_rr = int(self.baseline_rr * (1 - 0.05))

        elif state == 2:

            self.target_ecg = int(self.baseline_ecg * (1 - 0.1))
            self.target_rr = int(self.baseline_rr * (1 - 0.1))

        elif state == 3:

            self.target_ecg = int(self.baseline_ecg * (1 + 0.05))
            self.target_rr = int(self.baseline_rr * (1 + 0.05))

        elif state == 4:

            self.target_ecg = int(self.baseline_ecg * (1 - 0.05))
            self.target_rr = int(self.baseline_rr * (1 - 0.05))

        elif state == 5:

            self.target_ecg = int(self.baseline_ecg * (1 + 0.05))
            self.target_rr = int(self.baseline_rr * (1 + 0.05))


    def checkECG(self, state):

        bReturn = False

        if state == 1:
            if self.ecgDT < 0 and self.ecgDT >= -0.1 and self.accelDT < 0 and self.accelDT >= -0.1 and self.rrDT < 0 and self.rrDT >= -0.1:
                bReturn = True

        elif state == 2:
            if self.ecgDT < 0.1 and self.accelDT < 0 and self.accelDT <= -0.1 and self.rrDT <= -0.1:
                bReturn = True

        elif state == 3:

            if self.ecgDT > 0 and self.ecgDT <= 0.1 and self.accelDT < 0 and self.accelDT >= -0.1 and self.rrDT > 0 and self.rrDT <= 0.1:

                bReturn = True

        elif state == 4:

            if self.ecgDT < 0 and self.ecgDT >= -0.1 and self.accelDT < 0 and self.accelDT >= -0.1 and self.rrDT < 0 and self.rrDT >= -0.1:

                bReturn = True

        elif state == 5:

            if self.ecgDT > 0 and self.ecgDT <= 0.1 and self.accelDT < 0 and self.accelDT >= -0.1 and self.rrDT > 0 and self.rrDT <= 0.1:

                bReturn = True

        return bReturn


    def alter_states(self, cur_state, next_state, time_min = 1):
        print("Now entering state {currState}. Meditate toward state {nextState}".format(currState=self.currState,
                                                                                         nextState=next_state))
        time_start = time.time()

        flag = False

        if self.currState == cur_state:

            while True:

                ecg, accel, rr1, rr2, duration = self.dr.collectData(self.analysisPeriod, self.samplingDelay)
                ecgRate, agitation, rr1Rate, rr2Rate = calcRates(ecg, accel, rr1, rr2, duration)
                self.updateVals(ecgRate, agitation, rr1Rate, rr2Rate)
                self.updateTarget()
                self.checkProgression()
                # check for progression to Pre-meditation routine
                print(self.ecgDT, self.accelDT, self.rrDT)

                if self.checkECG(cur_state):

                    print("Proceeding to next routine, waiting for current interval to finish")
                    self.updateState(2)
                    self.buzzer1.cleanup()
                    self.update_baseline()
                    #do something with the visual
                    flag = True

                else:
                    #print the current status
                    print(self.currState)
                    print(self.ecgDT, self.accelDT, self.rrDT)

                if (time.time() - time_start) > time_min * 60:

                    if flag:

                        break

                    else:
                        #reset the timer
                        time_start = time.time()

        else:
            print("wrong state")

def calcRates(ecg,accel,rr1,rr2,duration):

    dp_ecg = DataProcessor(duration)
    dp_accel = DataProcessor(duration)
    dp_rr1 = DataProcessor(duration)
    dp_rr2 = DataProcessor(duration)

    ecgPeaks = dp_ecg.findPeaks(ecg, 0)
    accelPeaks = dp_accel.findPeaks(accel, 0)
    rr1Peaks = dp_rr1.findPeaks(rr1, 0)
    rr2Peaks = dp_rr2.findPeaks(rr2, 0)

    agitation = dp_accel.calcBPM()
    ecgRate = dp_ecg.calcBPM()
    rr1Rate = dp_rr2.calcBPM()
    rr2Rate = dp_rr2.calcBPM()

    return (ecgRate,agitation,rr1Rate,rr2Rate)

def main():

    #initialize the monitor
    patient = Patient_monitor(-1,-1,0,0,0,0,0,0,0,0)
    patient.warm_up()
    patient.collect_baseline()
    for i in range(1, 5):
        patient.alter_states(i, i + 1, 4)


if __name__ == "__main__" :
    main()
