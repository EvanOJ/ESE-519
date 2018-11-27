


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
				'''return the next 6 mapped values used by feedback processes'
			#visual feedback values/colors = [] #6 values
			#haptic feeedback values = [] #6 values, PWM ?

			processCounter += 1
		
		processCounter = 0
		ecgBuffer append to outputDataECG
		accelBuffer append to outputDataACCEL
		rrBuffer append to outputDataRR

	#write all outputdata to csv
	
	#exit




		
