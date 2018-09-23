/*
 * EOJ_LAB2_1_1.c
 *
 * Created: 9/12/2018 3:58:53 PM
 * Updated: 9/22/2018
 * Author : Evan Oskierko-Jeznacki & Christina Kim (Group 17)
 */ 

#include <avr/interrupt.h>
#include <avr/io.h>


int main(void)
{
	DDRB |= (0 << PORTB0);				//Set PB0 as an input for the pushbutton

	PORTB |= (1<<PORTB0);				//Enable Pushbutton pull-up
	
	DDRB |= (1<<PORTB5);				//Enable output for LED
	TIMSK1 |= (1 <<ICIE1);				// enable ICP1 input capture interrupt (corresponds to PB0)
	
	TCCR1B |= (1<<ICES1);				// capture rising edges bit 6

	TCCR1B |= (1<<CS10);				// start timer 1 without a prescaler

	sei();								//enable global interrupts

	while(1)
	{
										//do nothing here	
	}
}

ISR(TIMER1_CAPT_vect)
{
	PORTB ^= (1<<PORTB5);				// toggle PB5, corresponding to onboard LED pin 13
	TIFR1 |= (1<<ICF1);					// clear the input capture flag

}