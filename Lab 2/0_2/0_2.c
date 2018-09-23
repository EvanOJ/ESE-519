/*
 * EOJ_LAB2_0_2.c
 *
 * Created: 9/9/2018 5:15:28 PM
 * Author : Evan Oskierko-Jeznacki & Christina Kim (Group 17)
 */ 

#include <avr/io.h>


int main(void)
{
	DDRB = 0x20;								//set PB5 as output
	PORTB = 0x01;								//set PB1, connected to pushbutton to active low, to energize the LED when the pushbutton is engaged
    while (1) 
    {
		if(!(PINB & 0x01))						//poll PB1 for a button press via PINB, if button is depressed set PB5 (onboard LED) high
		{
			PORTB |= 0x20;						//if PB5 is off (low), turn it on (high)

		}
		else
		{
												//after polling for a button press via PINB, if button is not depressed toggle PB5 
		}
		{
			PORTB ^= (0x20);					//toggle PB5
		}
    }
}

