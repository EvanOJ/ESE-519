/*
 * Lab2_Part3.2.c
 *
 * Created: 9/20/2018 9:54:36 AM
 * Updated: 9/22/2018
 * Author : Evan Oskierko-Jeznacki & Christina Kim (Group 17)
 */ 

//Include all libraries/handles to use functions
#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include "uart.h"

int main(void)												//Main loop
{
	uart_init();											//Initializes/allows serial communication
	
	DDRB |= 0b00011100; 									//Sets PB 2-4 as outputs

	ADCSRA = (1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);				//Enables ADC s.t. FCPU/128=16MHz/125=125000Hz=125kHz which is in range of 50-200kHz
	ADMUX |= (1<<REFS0);									//Sets ADMUX (PC0) register to AVCC=Aref
	ADMUX &= ~(1<<REFS1);									//Sets AVCC (+5v) as reference voltage
	
	ADCSRB &= ((1<<ADTS2)|(1<<ADTS1)|(1<<ADTS0));			//ADC Control setting timer counter 1 capture
	ADCSRA |= (1<<ADATE);									//Enables auto-trigger
	ADCSRA |= (1<<ADEN);									//Enables  ADC
	
    while (1) 
    { 
		ADCSRA |= (1<<ADSC); 								//Start single conversion
		while(!(ADCSRA & (1<<ADIF))); 						//Wait for conversion to complete s.t. interrupt bit is 1 until done
		
		PORTB &= 0b111100011;								//Set Port B values focusing on turning off PB 2-4
		
		//min 336 max 765 from photo resistor 
		if(ADC<=389.625)									//If ADC value is less than 389.625...
		{			
			//do nothing
		}
		else if(ADC<=443.25 && ADC>389.625)					//If ADC value is between 389.625 and 443.25...
		{
			PORTB |= 0b00000100;							//Write 1 to PB2
		}
		else if(ADC<=496.873 && ADC>443.25)					//If ADC value is between 443.25 and 496.873...
		{
			PORTB |= 0b00001000;							//Write 1 to PB3
		}
		else if(ADC<=550.5 && ADC>496.873)					//If ADC value is between 496.873 and 550.5...
		{
			PORTB |=0b00001100;								//Write 1 to PB2 and PB3
		}
		else if(ADC<=604.125 && ADC>550.5)					//If ADC value is between 550.5 and 604.125...
		{
			PORTB |=0b00010000;								//Write 1 to PB4
		}
		else if(ADC<=657.75 && ADC>604.125)					//If ADC value is between 604.125 and 657.75...
		{
			PORTB |=0b00010100;								//Write one to PB2 an PB4
		}
		else if(ADC<=711.375 && ADC>657.75)					//If ADC value is between 657.75 and 711.375...
		{
			PORTB |=0b00011000;								//Write 1 to PB3 and PB4
		}
		else if(ADC>711.375)								//If ADC value is greater than 711.375...
		{
			PORTB |= 0b00011100;							//Write 1 to PB2-PB4
		}
		ADCSRA |= (1<<ADIF); 								//Clears ADIF(interrupt bit to be used after conversion is complete)

		printf("%d\n",ADC);									//Prints ADC value
    }
}
