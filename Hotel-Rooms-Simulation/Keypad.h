#include "tm4c123gh6pm.h"

#ifndef KEYPAD_H_
#define KEYPAD_H_

#define KEYPAD_ROW GPIOD
#define KEYPAD_COL GPIOA

void init_KEYPAD(void);
void delay(void);
unsigned char readKey(void);



#endif /* KEYPAD_H_ */
