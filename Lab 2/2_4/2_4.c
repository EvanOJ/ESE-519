/*
 * Lab2_2_4.c
 *
 * Created: 9/20/2018 5:36:38 PM
 * Updated: 9/22/2018
 * Author : Evan Oskierko-Jeznacki & Christina Kim (Group 17)
 */ 

//Include all libraries/handles to use functions
#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include "uart.h"
#include <math.h>

//Sets/defines all variables as unsigned integers or long
unsigned int diff, edge1, edge2,edgeCount,overflows;
uint32_t pulse_width;

unsigned long freq_in = 1047;
unsigned long freq_out = 2093;

unsigned long freq_adj;

unsigned long pwm_max = 827;
unsigned long pwm_min = 95;

//Initializes/defines variables as integers
int freqMode = 0;																				//Variable to choose discrete or continuous frequency mode 
int buttonCount = 0;																			//Initialize button count at 0


ISR(TIMER1_COMPA_vect)																			//Interrupt service routine for timer 1 output compare
{
	overflows++;																				//Increments overflow counter up

	TCCR1B |= (1<<ICES1);																		//Enables input capture mode on rising edge
	TIMSK1 |= (1<<ICIE1);																		//Enables input capture interrupt
}


ISR(TIMER1_CAPT_vect)																			//Interrupt service routine for timer 1 input capture
{	
	TIMSK1 |= (0<<OCIE1A);																		//Turns off output compare interrupts (is this needed if TIMSK1 |= (1<<ICIE) should change everything else to 0)
	DDRB |= (0<<PORTB0);																		//Sets PB0 as input

	if(edgeCount %2 == 0)																		//If remainder ==0 (this is a falling edge)...
	{
		edge2 = ICR1;																			//Store time value of edge 2 in ICR1 register
		edgeCount++;																			//Increment edge counter up

		diff = edge2 - edge1;																	//Calculate difference between two edge times
		if(edge2 < edge1)																		//If edge2 occurs before edge 1...
		{
			overflows--;																		//Increment back down by full overflow count
		}
		pulse_width = (0.000004)*((long)overflows * 65536u +(long)diff);						//Calculate pulse width given the period and maximum number of clock ticks a 16-bit timer can have

		TIFR1 |= 0x20;																			//Clears input capture flag
		overflows = 0;																			//Reset overflows, should be ok parity maintained for %2 condition
	}
	else
	{
		edge1 = ICR1;																			//Store time value for edge 1 in ICR1 register
		edgeCount++;																			//Increment edge counter up

		TIFR1 |= 0x20;																			//Clears input capture flag
		TCCR1B ^= (1<<ICES1);																	//Toggles which edge to capture
	}
}


ISR(TIMER0_COMPA_vect)																			//Interrupt service routine for timer 0 output compare
{
	PORTD ^= (1<<PORTD6);																		//Toggles PD6 high and low
	TCNT0 = 0;																					//Clears counter
}


ISR(INT0_vect)																					//Interrupt service routine for external interrupt 0
{
	buttonCount ++;																				//Increments button count up
}


int contFreq(void)																				
{
	/*Function to convert the UHF pinger pulse width to a buzzer tone, between 
	the desired tonal range, in a continuous, linear manner (i.e., not discrete bins)*/
	freq_adj = freq_in + ((pulse_width-pwm_min)*((freq_out - freq_in)/(pwm_max-pwm_min)));		//Map PWM to frequency to buzzer
			
	TCCR0A ^=(1<<WGM01);																		//Toggle timer 0 in CTC Mode (to reduce noise)--Chris TA suggestion
	OCR0A = (8000000/(64*freq_adj))-1;															//Set OCR0A to the frequency mapped from the calculated pulse width value(freq_adj)
	TCCR0A ^=(1<<WGM01);																		//Toggle timer 0 in CTC Mode (to reduce noise)--Chris TA suggestion
}


int discFreq(void)																				
{
	/*Function to convert ther UHG pinger pulse width to a buzzer tone within discrete frequency 
	bins corresponding to the actual notes in the desired tonal range C6-C7. 
	(*Note: OCR0A values were divided by 2 to lower the tone by a octave)*/

	if(pulse_width<=199.57)																		//If pulse widths are less than 199.57...
	{
		//C6
		OCR0A = 8;																				//Set OCR0A to 8
	}
	else if(pulse_width>199.57 && pulse_width<=304.14)											//If pulse widths are between 199,57 and 304.14...
	{
		//D6
		OCR0A = 9;																				//Set OCR0A to 9
	}
	else if(pulse_width>304.14 && pulse_width<=408.71)											//If pulse widths are between 304.14 and 408.71...
	{
		//E6
		OCR0A = 10;																				//Set OCR0A to 10
	}
	else if(pulse_width>408.71 && pulse_width<=513.28)											//If pulse widths are between 408.71 and 513.28...
	{
		//F6
		OCR0A = 11;																				//Set OCR0A to 11
	}
	else if(pulse_width>513.28 && pulse_width<=617.85)											//If pulse widths are between 513.28 and 617.85...
	{
		//G6
		OCR0A = 13;																				//Set OCR0A to 13
	}
	else if(pulse_width>617.85 && pulse_width<=722.42)											//If pulse widths are between 617.85 and 722.42...
	{
		//A6
		OCR0A = 14;																				//Set OCR0A to 14
	}
	else if(pulse_width>722.42 && pulse_width<=826.99)											//If pulse widths are between 722.42 and 826.99...
	{
		//B6
		OCR0A = 16;																				//Set OCR0A to 16
	}
	else if(pulse_width>826.99)																	//If pulse widths are geater than 826.99...
	{
		//C7
		OCR0A = 17;																				//Set OCR0A to 17
	}
}


int main(void)																					//Main loop
{
	uart_init();																				//Initializes/allows serial communication

	DDRB |= (1 << PORTB1);																		//Set PB1 as output
	PORTB |= (1 << PORTB1);																		//Set PB1 as high

	overflows = 0;																				//Initializes overflow count at 0
	edgeCount = 0;																				//Initializes edge count at 0

	TCNT1 = 0;																					//Clears counter
	OCR1A = TCNT1 + 10;																			//Pull OCRA pin high quickly and initiate using 10us pinger
	TCCR1A |= (1 << COM1A0);																	//Toggle OC1A on compare match
	TCCR1B |= (1 << WGM12)|(1 << CS11);															//Enable CTC for output compare using 8-bit prescaler clock
	TIMSK1 |= (1 << OCIE1A);																	//Enable output compare interrupt
 	sei();																						//Enable global interrupts

	//enable clock for PWM output
	TCCR0A |=(1<<WGM01);																		//Enable timer 0 in CTC Mode
	TCNT0 = 0;																					//Clears counter
	TIMSK0 |= (1<<OCIE0A);																		//Set ISR compare vector
	TCCR0B |= (1<<CS01)|(1<<CS00);																//Enable timer 0 with 64 pre-scaler

	DDRD |= (1<<PORTD6);																		//enable PD6 as output
	PORTD |= (1<<PORTD6);																		//Set PD6 as high (pull-up)
	
	
	DDRD |= (0<<PORTD2);																		//Set PD2 as input
	PORTD |= (1<<PORTD2);																		//Set PD2 as high (pull-up)
	
	EICRA |= (1 << ISC00);    																	// Set INT0 to trigger on ANY logic change
	EIMSK |= (1 << INT0);    																	// Turns on INT0

	sei();                    																	//Enable global interrupts
	
	while (1)
	{
		if((buttonCount/2)%2==0)																//If button count divided by 2 and remainder equals 0...
		{
			//continuous = even button count
			contFreq();																			//Run continuous frequency function
		}
		else if((buttonCount/2)%2!=0)															//If button count divided by 2 and remainder does not equal 0...
		{
			discFreq();																			//Run discrete frequency function
		}
		
 		printf("pulse_width= %lu\n", pulse_width);												//Print pulse width as an unsigned long
	}
}
