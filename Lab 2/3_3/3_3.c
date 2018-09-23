/*
 * Lab2_3.3.c
 *
 * Created: 9/20/2018 7:07:50 PM
 * Author : Evan Oskierko-Jeznacki & Christina Kim
 */ 

//Include all libraries/handles to use functions
#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include "uart.h"
#include <math.h>

//Defines/set all variables as unsigned integer or long
unsigned int diff, edge1, edge2,edgeCount,overflows;
uint32_t pulse_width;

unsigned long freq_in = 1047;													//C6 frequency
unsigned long freq_out = 2093;													//C7 frequency

unsigned long freq_adj;

unsigned long pwm_max = 827;													//Maximum measured PWM
unsigned long pwm_min = 95;														//Minimum measured PWM

//Defines/sets all variables as integers
int freqMode = 0;																//Variable choose discrete or continuous frequency mode 
int buttonCount = 0;															//Sets button count to start at 0


ISR(TIMER1_COMPA_vect)															//Interrupt service routine for timer 1 output compare
{
	overflows++;																//Increments overflow counter up

	TCCR1B |= (1<<ICES1);														//Enables input capture mode on rising edge
	TIMSK1 |= (1<<ICIE1);														//Enables input capture interrupt
}

ISR(TIMER1_CAPT_vect)															//Interrupt service routine for timer 1 input capture
{
	TIMSK1 |= (0<<OCIE1A);														//Turns off output compare interrupts (is this needed if TIMSK1 |= (1<<ICIE) should change everything else to 0)
	DDRB |= (0<<PORTB0);														//Sets PB0 as input

	if(edgeCount %2 == 0)														//If remainder ==0 (this is a falling edge)...
	{
		edge2 = ICR1;															//Store time value of edge 2 in ICR1 register
		edgeCount++;															//Increment edge counter up

		diff = edge2 - edge1;													//Calculate difference between two edge times

		if(edge2 < edge1)														//If edge2 occurs before edge 1...
		{
			overflows--;														//Increment back down by full overflow count
		}
		pulse_width = (0.000004)*((long)overflows * 65536u +(long)diff);		//Calculate pulse width given the period and maximum number of clock ticks a 16-bit timer can have

		TIFR1 |= 0x20;															//Clears input capture flag
		overflows = 0;															//Reset overflows, should be ok parity maintained for %2 condition
	}
	else
	{
		edge1 = ICR1;															//Store time value for edge 1 in ICR1 register
		edgeCount++;															//Increment edge counter up

		TIFR1 |= 0x20;															//Clears input capture flag
		TCCR1B ^= (1<<ICES1);													//Toggles which edge to capture
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
int contFreq(void)																				//Function for continuous frequency
{
	freq_adj = freq_in + ((pulse_width-pwm_min)*((freq_out - freq_in)/(pwm_max-pwm_min)));		//Map PWM to frequency to buzzer
			
	TCCR0A ^=(1<<WGM01);																		//Toggle timer 0 in CTC Mode (to reduce noise)--Chris TA suggestion
	OCR0A = (8000000/(64*freq_adj))-1;															//Set OCR0A to the frequency mapped from the calculated pulse width value(freq_adj)
	TCCR0A ^=(1<<WGM01);																		//Toggle timer 0 in CTC Mode (to reduce noise)--Chris TA suggestion	
}


int discFreq(void)																				//Function for discrete frequency (*Note: OCR0A values were divided by 2 to lower octave)
{
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


int photoInit(void)																				//Function to intialize registers and properties
{
	DDRB |= 0b00011100; 																		//Sets PB 2-4 as outputs

	ADCSRA = (1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);													//Enables ADC s.t. FCPU/128=16MHz/125=125000Hz=125kHz which is in range of 50-200kHz
	ADMUX |= (1<<REFS0);																		//Sets ADMUX (PC0) register to AVCC=Aref
	ADMUX &= ~(1<<REFS1);																		//Sets AVCC (+5v) as reference voltage
	
	ADCSRB &= ((1<<ADTS2)|(1<<ADTS1)|(1<<ADTS0));												//ADC Control setting timer counter 1 capture
	ADCSRA |= (1<<ADATE);																		//Enables auto-trigger
	ADCSRA |= (1<<ADEN);																		//Enables  ADC
}

void photoRead(void)																			//Function writing bits to light sensitive resistor for volume control
{
	ADCSRA |= (1<<ADSC); 																		//Start single conversion
	while(!(ADCSRA & (1<<ADIF))); 																//Wait for conversion to complete s.t. interrupt bit is 1 until done
		
	PORTB &= 0b111100011;																		//Set Port B values focusing on turning off PB 2-4
		
	//min 336 max 765 from photo resistor 
	if(ADC<=389.625)																			//If ADC value is less than 389.625...
	{			
																								//do nothing for the first group
	}
	else if(ADC<=443.25 && ADC>389.625)															//If ADC value is between 389.625 and 443.25...
	{
		PORTB |= 0b00000100;																	//Write 1 to PB2
	}
	else if(ADC<=496.873 && ADC>443.25)															//If ADC value is between 443.25 and 496.873...
	{
		PORTB |= 0b00001000;																	//Write 1 to PB3
	}
	else if(ADC<=550.5 && ADC>496.873)															//If ADC value is between 496.873 and 550.5...
	{
		PORTB |=0b00001100;																		//Write 1 to PB2 and PB3
	}
	else if(ADC<=604.125 && ADC>550.5)															//If ADC value is between 550.5 and 604.125...
	{
		PORTB |=0b00010000;																		//Write 1 to PB4
	}
	else if(ADC<=657.75 && ADC>604.125)															//If ADC value is between 604.125 and 657.75...
	{
		PORTB |=0b00010100;																		//Write one to PB2 an PB4
	}
	else if(ADC<=711.375 && ADC>657.75)															//If ADC value is between 657.75 and 711.375...
	{
		PORTB |=0b00011000;																		//Write 1 to PB3 and PB4
	}
	else if(ADC>711.375)																		//If ADC value is greater than 711.375...
	{
		PORTB |= 0b00011100;																	//Write 1 to PB2-PB4
	}
	ADCSRA |= (1<<ADIF); 																		//Clears ADIF(interrupt bit to be used after conversion is complete)
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
		
	//read photo resitor and set voltage (amplitude)
	photoRead();																				//Runs function to get volume control
	}
}
