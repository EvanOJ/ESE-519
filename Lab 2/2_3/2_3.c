/*
 * Lab2_2.3.c
 *
 * Created: 9/19/2018 12:18:57 PM
 * Updated: 9/22/2018
 * Author : Christina Kim & Evan Oskierko-Jeznacki (Group 17)
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


ISR(TIMER1_COMPA_vect)																				//Interrupt service routine for timer 1 output compare
{
	overflows++;																					//Increments overflow counter up

	TCCR1B |= (1<<ICES1);																			//Enables input capture mode on rising edge
	TIMSK1 |= (1<<ICIE1);																			//Enables input capture interrupt
}

ISR(TIMER1_CAPT_vect)
{
	TIMSK1 |= (0<<OCIE1A);																			//Turns off output compare interrupts (is this needed if TIMSK1 |= (1<<ICIE) should change everything else to 0)
	DDRB |= (0<<PORTB0);																			//Sets PB0 as input

	if(edgeCount %2 == 0)																			//If remainder ==0 (this is a falling edge)...
	{
		edge2 = ICR1;																				//Store time value of edge 2 in ICR1 register
		edgeCount++;																				//Increment edge counter up

		diff = edge2 - edge1;																		//Calculate difference between two edge times
		if(edge2 < edge1)																			//If edge2 occurs before edge 1...
		{
			overflows--;																			//Increment back down by 1 full overflow count
		}

		pulse_width = (0.000004)*((long)overflows * 65536u +(long)diff);							//Calculate pulse width given the period and maximum number of clock ticks a 16-bit timer can have
		
		TIFR1 |= 0x20;																				//Clears input capture flag
		overflows = 0;																				//Resets overflows (should be ok parity maintained for %2 condition)
	}
	else																							//If the "if" statement does not hold true...
	{
		edge1 = ICR1;																				//Store time value for edge 1 in ICR1 register
		edgeCount++;																				//Increment edge counter up

		TIFR1 |= 0x20;																				//Clears input capture flag
		TCCR1B ^= (1<<ICES1);																		//Toggles which edge to capture
	}
}


ISR(TIMER0_COMPA_vect)																				//Interrupt service routine for timer 0 output compare
{
	PORTD ^= (1<<PORTD6);								  										   //Toggles PD6 high and low
	TCNT0 = 0;											   										   //Clears counter
}


int main(void)																						//Main loop
{
	uart_init();																					//Initializes/allows serial communication

	DDRB |= (1 << PORTB1);																			//Set PB1 as output
	PORTB |= (1 << PORTB1);																			//Set PB1 as high (pull-up)

	overflows = 0;																					//Initializes overflow count at 0
	edgeCount = 0;																					//Initializes edge count at 0

	TCNT1 = 0;																						//Clears counter
	OCR1A = TCNT1 + 10;																				//Pull OCRA pin high quickly and initiate using 10us pinger
	TCCR1A |= (1 << COM1A0);																		//Toggle OC1A on compare match
	TCCR1B |= (1 << WGM12)|(1 << CS11);																//Enable CTC for output compare using 8-bit prescaler clock
	TIMSK1 |= (1 << OCIE1A);																		//Enable output compare interrupt
	sei();																							//Enable global interrupts

	//enable clock for PWM output
	TCCR0A |=(1<<WGM01);																			//Enable timer 0 in CTC Mode
	TCNT0 = 0;																						//Clears counter
	TIMSK0 |= (1<<OCIE0A);																			//Set ISR compare vector
	TCCR0B |= (1<<CS01)|(1<<CS00);																	//Enable timer 0 with 64 pre-scaler

	DDRD |= (1<<PORTD6);																			//Enable PD6 as output
	PORTD |= (1<<PORTD6);																			//Set PD6 as high (pull-up)
	
	//at this point will trigger and go to ISR functionality>>>>>
	
	while (1)
	{
 		//Calculate PWM
		freq_adj = freq_in + ((pulse_width-pwm_min)*((freq_out - freq_in)/(pwm_max-pwm_min)));		//Mapping equation output = output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)
		TCCR0A ^=(1<<WGM01);																		//Toggle timer 0 in CTC Mode (to reduce noise)

		OCR0A = (8000000/(64*freq_adj))-1;															//Set OCR0A to the frequency mapped from the calculated pulse width value (freq_adj)
		TCCR0A ^=(1<<WGM01);																		//Toggle timer 0 in CTC Mode (to reduce noise)

		printf("pulse_width= %lu\n", pulse_width);									//Print pulse width as an unsigned long s.t. pulse width is calculated using 64 prescaler and divided by 2 again to increase signal stability
	}
}
