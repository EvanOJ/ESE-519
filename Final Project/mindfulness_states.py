
def physChange(oldVals,currentVals):
	ecg_old = oldVals[0]
	rr_old = oldVals[1]
	accel_old = oldVals[2]

	ecg_new = currentVals[0]	
	rr_new = currentVals[1]
	accel_new = currentVals[2]

	#calculate change
	ecg_dt	=	int(round((((ecg_new - ecg_old)/ecg_new)*100),0))
	rr_dt	=	int(round((((rr_new - rr_old)/rr_new)*100),0))
	accel_dt	=	int(round((((accel_new - accel_old)/accel_new)*100),0))

	print(ecg_dt,rr_dt,accel_dt)
	return(ecg_dt,rr_dt,accel_dt)


def stateChange(prevState,oldVals,currentVals,thresh):
	if prevState == 0:
		ecg_objective = currentVals[0]-(currentVals[0]*thresh)
		rr_objective = currentVals[1]-(currentVals[1]*thresh)

		print("proceeding from baseline to pre-meditation states")
		print("reduce heart rate by up to 10% to: %s" % (ecg_objective))
		print("reduce Respiratory rate by up to 10% to: %s" % (rr_objective))
		objectiveState = 1

	elif prevState == 1:
		ecg_objective = currentVals[0]-(currentVals[0]*thresh)
		rr_objective = currentVals[1]-(currentVals[1]*thresh)

		print("proceeding from pre-meditation to concentration")
		print("reduce heart rate by above 10% to %s" % (ecg_objective))
		print("reduce Respiratory rate by above 10% to: %s" %(rr_objective))
		objectiveState = 2

	elif prevState == 2:
		ecg_objective = currentVals[0]+(currentVals[0]*thresh)
		rr_objective = currentVals[1]+(currentVals[1]*thresh)

		print("proceeding from concentration to rapture")
		print("increase heart rate by up to 10% to: %s" %(ecg_objective))
		print("increase Respiratory rate by up to 10% to: %s" %(rr_objective))
		objectiveState = 3

	elif prevState == 3:
		ecg_objective = currentVals[0]-(currentVals[0]*thresh)
		rr_objective = currentVals[1]-(currentVals[1]*thresh)

		print("proceeding from rapture to reflection")
		print("decrease heart rate by up to 10% to: %s" %(ecg_objective))
		print("decrease Respiratory rate by up to 10% to: %s" % (rr_objective))
		print("decrease heart rate toand Respiratory rate by 10% to %s" % (ecg_objective))
		objectiveState = 4
	elif prevState == 4:
		print("proceeding from reflection to Conclusion")
		print("increase heart rate and Respiratory rate by 10% to %s" % (ecg_objective))
		objectiveState = 5
	else:
		print("done. terminate.")
		objectiveState = 6

	return objectiveState


import time
from random import randint
import math

basestate = (75,25,10)

currentState = basestate


def detectState(currentVals,oldVals,thresh):
	'''Takes basestate values (3) and compares to current (3).
	#pre-meditation routine
	#Heart Rate change from baseline 		0-10% decrease
	#Respiratory rate change from baseline 	0-10% decrease
	#Movement (hand/head, etc.)				Moderate (adjusting posture, etc.)

	#Concentration
	#Heart Rate change from baseline 		>10% decrease
	#Respiratory rate change from baseline 	>10% decrease
	#Movement (hand/head, etc.)				Low

	#Rapture
	#Heart Rate change from baseline 		0-10% increase
	#Respiratory rate change from baseline 	0-10% increase
	#Movement (hand/head, etc.)				Low

	#Reflection
	#Heart Rate change from baseline 		0-10% decrease
	#Respiratory rate change from baseline 	0-10% decrease
	#Movement (hand/head, etc.)				Low

	#Conclusion
	#Heart Rate change from baseline 		0-10% increase
	#Respiratory rate change from baseline 	0-10% increase
	#Movement (hand/head, etc.)				Moderate'''

	ecg_old = oldVals[0]
	rr_old = oldVals[1]
	accel_old = oldVals[2]

	ecg_new = currentVals[0]	
	rr_new = currentVals[1]
	accel_new = currentVals[2]

	#calculate change
	ecg_dt	=	int(round((((ecg_new - ecg_old)/ecg_new)*100),0))
	rr_dt	=	int(round((((rr_new - rr_old)/rr_new)*100),0))
	accel_dt	=	int(round((((accel_new - accel_old)/accel_new)*100),0))

	print(ecg_dt,rr_dt,accel_dt)

	if currentVals == oldVals:
		print("baseline")
		return 0
	elif((ecg_dt>=-thresh & ecg_dt<0) & (rr_dt>=-thresh & rr_dt<=0) & accel_new<=5):
		print("pre-meditation")
		return 1
	elif((ecg_dt<-thresh) & (rr_dt<-thresh & rr_dt<0) & accel_new < 2):
		print("concentration")
		return 2
	elif((ecg_dt<=thresh & ecg_dt>=0) & (rr_dt<=thresh & rr_dt>=0) & accel_new < 2):
		print("rapture")
		return 3
	elif((ecg_dt>=-thresh & ecg_dt<0) & (rr_dt>=-thresh & rr_dt<=0) & accel_new<=5):
		print("reflection")
		return 3
	elif((ecg_dt<=thresh & ecg_dt>=0) & (rr_dt<=thresh & rr_dt>=0) & accel_new <=5):
		print("Conclusion")
		return 4
	else:
		print("inconclusive")

def main():
	# fakeECG = randint(50,100)
	# fakeRR = randint(10,30)
	# fakeACCEL = randint(0,10)
	fakeECG = [100,95,95,90,88,86,83,76,75,76,70,69,69,70,75,79,80,]
	fakeRR = randint(10,30)
	fakeACCEL = randint(0,10)
	baseVals = (fakeECG,fakeRR,fakeACCEL)

	print("basestate: " + str(baseVals))

	basestate = (1,1,1)

	for i in range(50):
		fakeECG = randint(50,100)
		fakeRR = randint(10,30)
		fakeACCEL = randint(0,10)
		currentVals = (fakeECG,fakeRR,fakeACCEL)

		if i == 0:
			basestate = detectState(baseVals,currentVals,10)
		else:
			currentState = detectState(baseVals,currentVals,10)

			time.sleep(1)

main()
