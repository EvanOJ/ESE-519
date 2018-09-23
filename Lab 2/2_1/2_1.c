/*
 * Lab2_Part2_1.c
 *
 * Created: 9/13/2018 6:19:28 PM
 * Updated: 9/22/2018
 * Author : Evan Oskierko-Jeznacki & Christina Kim (Group 17)
 */ 

//Include all libraries/handles to use functions
#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>
#include "uart.h"

void timer0_init()                      //Function to initalize timer 0 and properties in main loop
{
  TCCR0A |= (1 <<WGM01);                //Set the timer mode to CTC (clear timer on compare), Pin OC0A disconnected
  TCCR0B |= (1<<CS02)|(1<<CS00);        //Set the prescaler to 1024 and start the timer

  OCR0A = 17;                           //Set OCR0A to 440 Hz with 16MHz clock and 1024 prescaler = 36362.36 for a FULL sine wave, halve for first edge = 17
  TCCR0A ^= (1<<COM0A0);                //Set OC0A bit for output enable output compare mode to toggle OC0A pin on match
  TIMSK0 |= (1<<OCIE0A);                //Unmask output compare match interrupt for register A
}

int main(void)                          //Main loop function to run
{ 
  DDRD |= (1<<PORTD6);                  //Enable PD6 as output
  timer0_init();                        //Run timer 0 initialize function
  sei();                                //Enable global interrupts
  
  for(;;)
  {
                                        //loop forever
                                        //do nothing here
  }

}

ISR(TIMER0_COMPA_vect)
{
                                        //interrupt service routine for output compare match
                                        //do nothing here
}
