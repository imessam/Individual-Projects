#include "UART.h"

void init_UART0(){
	
	SYSCTL->RCGCUART |= 1; /* provide clock to UART0 */
 SYSCTL->RCGCGPIO |= 1; /* enable clock to PORTA */
	while((SYSCTL->PPGPIO & 0x01)!=0x01){};
		UART0->CTL &= ~0x01; /* disable UART0 */
		UART0->CC = 0; /* use system clock */
		UART0->IBRD = 52; /* IBRD = int(16,000,000/(16*19,200)) = int(52.083)*/
		UART0->FBRD = 5; /* fraction part, int(0.083*64)=5 */
		UART0->LCRH = 0x70; /* 8-bit, no parity, 1-stop bit, no FIFO */
		UART0->CTL |= 0x301; /* enable UART0, TXE, RXE */
	 
		GPIOA->DEN |= 0x03; /* Make PA0 and PA1 as digital */
		GPIOA->AFSEL |= 0x03; /* Use PA0,PA1 alternate function */
		GPIOA->PCTL = (GPIOA->PCTL&0xFFFFFF00)+0x00000011;
		GPIOA->AMSEL &= ~0x03;          // disable analog functionality on PA1,PA0
}

 unsigned char getChar(void){
	while((UART0->FR& 0x0010)!=0){};
	return ((unsigned char)(UART0->DR&0xFF));
}
 
void sendChar( unsigned char CHAR){
	while((UART0->FR & 0x0020)!=0){};
	UART0->DR=CHAR;
}

void sendString(char* string){
	while(*string){
		sendChar(*(string++));
	}
}

