/*
 * Lab2_3.1.c
 *
 * Created: 9/18/2018 5:27:31 PM
 * Updated: 9/22/2018
 * Author : Evan Oskierko-Jeznacki & Christina Kim
 */ 

//Include all libraries/handles to use functions
#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include "uart.h"

long ADC_value;												//variable to store the value returned by the ADC and photoresistor

uint16_t inputADC(void)										//Function to find ADC returning value as 16 bit unsigned integer
{
	/*Function to read the input from the ADC*/
	ADCSRA |= (1<<ADSC);									//start single conversion
	while(!(ADCSRA & (1<<ADIF)));							//wait for conversion to complete
	ADCSRA |= (1<<ADIF);									//clear the ADIF ADC interrupt flag
	return(ADC);											//ADC value returned
}

int main(void)												//Main loop
{
	uart_init();											//Initializes/allows serial communication
	
	ADMUX = (1<<REFS0);										//Sets the ADMUX (PC0) register to AVCC=Aref
	ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);	//Enable ADC s.t. FCPU/128=16MHz/125=125000Hz=125kHz which is in range of 50-200kHz
	
    while (1) 
    {
		ADC_value=inputADC();								//Reads analog photoresistor value after running inputADC function
		printf("%d\n",ADC_value);							//Prints result to the console
    }
}
