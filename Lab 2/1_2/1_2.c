/*
 * EOJ_LAB2_1_2_v2.c
 *
 * Created: 9/13/2018 1:08:26 PM
 * Updated: 9/21/2018
 * Author : Evan Oskierko-Jeznacki & Christina Kim (Group 17)
 */ 

//Include all libraries/handles to use functions
#include <avr/io.h>
#include <avr/interrupt.h>

unsigned int half_period=18;						//Defines/sets variable to 440 Hz with 16MHz clock and 1024 pre-scaler = 36362.36 for a FULL sine wave
													//halve for first edge and rounding up

ISR(TIMER0_COMPA_vect)								//Interrupt service routine for timer 0 output compare
{
    OCR0A += half_period;   						//Increments OCR0A by the half_period
}


int main(void)										//Main loop function to run
{	
	DDRD |= (1<<PORTD6);							//Enable PD6 as output
	
	TCCR0B |= (1<<CS02)|(1<<CS00);					//Set the pre-scaler to 1024 and start the timer
	TCCR0A |= 0x40;									//Toggle OC0A on Compare Match
	TCNT0 = 0;										//Set TCNT0 to 0, although not entirely necessary (works without this step)
	TIMSK0 = 0x02;									//Enable output compare A interrupt
	
	OCR0A += TCNT0 + half_period;					//toggle PD6

	sei();											//Enable global interrupts
	
	while(1)
	{
		//loop forever
		//do nothing here
	}

}


