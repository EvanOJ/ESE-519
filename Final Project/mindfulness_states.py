import time
from random import randint
import math

basestate = (75,25,10)

currentState = basestate


def detectState(currentVals,baseVals,thresh):
	'''Takes basestate values (3) and compares to current (3).'''

	ecg_old = baseVals[0]
	rr_old = baseVals[1]
	accel_old = baseVals[2]

	ecg_new = currentVals[0]	
	rr_new = currentVals[1]
	accel_new = currentVals[2]

	ecg_dt	=	int(round((((ecg_new - ecg_old)/ecg_new)*100),0))
	rr_dt	=	int(round((((rr_new - rr_old)/rr_new)*100),0))
	accel_dt	=	int(round((((accel_new - accel_old)/accel_new)*100),0))

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
	#Movement (hand/head, etc.)				Moderate
	print(ecg_dt,rr_dt,accel_dt)

	if currentVals == baseVals:
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
