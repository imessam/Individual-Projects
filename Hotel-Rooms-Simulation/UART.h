#include "tm4c123gh6pm.h"

#ifndef UART_H_
#define UART_H_

void init_UART0(void);
 unsigned char getChar(void);
 unsigned char getCharNonBlocking(void);
 char * getString(void);
void sendChar( unsigned char CHAR);
void sendString(char* string);

#endif /* UART_H_ */

