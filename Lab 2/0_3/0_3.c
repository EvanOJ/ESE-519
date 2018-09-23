/*
 * EOJ_LAB2_0_3.c
 *
 * Created: 9/9/2018 5:30:09 PM
 * Updated: 9/22/2018
 * Author : Evan Oskierko-Jeznacki & Christina Kim (Group 17)
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>

volatile uint8_t tot_overflow;										//create variable to store overflow count

void timer0_init()
{
	TCCR0A |= (1<< CS00);											//start timer 0 with no pre-scaling
	TCNT0 = 0;														//initialize counter and clear timer counter register
}

ISR(TIMER0_OVF_vect)
{
	tot_overflow++;													//keep track of number of timer 0 overflows
}

int main(void)
{
	DDRD |= (1 << PORTD6);											//set PD6 to OUTPUT mode
	
	timer0_init();													//initialize timer 0 
	
    /* loop forever */
    while (1) 
    {
		if(tot_overflow)											//if overflow...
		{	
			PORTD ^= (1 << PORTD6);									//toggle the buzzer pin output
			TCNT0 = 0;												//reset timer counter register
		}
	}
}

