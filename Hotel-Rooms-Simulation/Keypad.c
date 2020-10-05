#include "Keypad.h"


void init_KEYPAD(void){
	KEYPAD_ROW->LOCK = 0x4C4F434B;
	KEYPAD_ROW->CR=0xFF;	
	KEYPAD_ROW->AMSEL = (0x00);
	KEYPAD_ROW->PCTL = (0x00);
	KEYPAD_ROW->DIR =0x0F;
	KEYPAD_ROW->AFSEL = (0x00);
	KEYPAD_ROW->DEN =0x0F;
	KEYPAD_ROW->ODR =0x0F;
	

	KEYPAD_COL->AMSEL = (0x00);
	KEYPAD_COL->DIR = (0x0C);
	KEYPAD_COL->DEN |=0xFC;
	KEYPAD_COL->PUR |=0xF0;
}


unsigned char readKey(void){
unsigned char KEYS [4][4]={
{'1','2','3','A'},
{'4','5','6','B'},
{'7','8','9','C'},
{'*','0','#','D'}
};


int row,col;

KEYPAD_ROW->DATA=0x0F;
KEYPAD_COL->DATA=0xF4;
GPIOB->DATA|=(0x08);


while(1){

row=0;
	GPIOA->DATA&=~(0x04);
	delay();
	col=KEYPAD_COL->DATA&0xF0;
	if(col!=0xF0 && row==0){break;}
	

	row=1;
					GPIOB->DATA&=~(0x08);
	delay();
	col=KEYPAD_COL->DATA&0xF0;
	if(col!=0xF0 && row==1){break;}
	
	row=2;
	KEYPAD_ROW->DATA= ~(0xF4);
	delay();
	col=KEYPAD_COL->DATA&0xF0;
	if(col!=0xF0){break;}
	
	
	row=3;
	KEYPAD_ROW->DATA= ~(0xF8);
	delay();
	col=KEYPAD_COL->DATA&0xF0;
	if(col!=0xF0){break;}
	
	return 0 ;
	
}

if(col==(0xE0)){
col=0;
return KEYS[row][col];
}

else if(col==(0xD0)){
col=1;
return KEYS[row][col];
}

else if(col==(0xB0)){
col=2;
return KEYS[row][col];
}

if(col==(0x70)){
col=3;
return KEYS[row][col];
}



return 0;

}

void delay(void){
	unsigned long volatile time;
  time = 727240*200/91;  // 0.1sec
  while(time){
		time--;
  }
}

