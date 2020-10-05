#include "tm4c123gh6pm.h"
#include "string.h"
#include "lcd.h"


void LCD_init() {

				SYSCTL->RCGCGPIO|=0x02;
	while((SYSCTL->PRGPIO&0x02) != 0x02){};
	
	LCDPORT->AMSEL=0x00;
	LCDPORT->PCTL=0x00;
	LCDPORT->DIR=0xFF;
	LCDPORT->AFSEL=0x00;
	LCDPORT->DEN=0xFF;	
	
        SysCtlDelay(50000);

        
		LCDPORT->DATA=(0x00);

        
    LCDPORT->DATA=0x30;    
		
LCDPORT->DATA|=0x02;      
		SysCtlDelay(10);
        
LCDPORT->DATA&=~(0x02);
        SysCtlDelay(50000);

       
				    LCDPORT->DATA=0x30;    
       
				LCDPORT->DATA|=0x02;      

        SysCtlDelay(10);
       
				LCDPORT->DATA&=~(0x02);


        SysCtlDelay(50000);


				    LCDPORT->DATA=0x30;    

     
				LCDPORT->DATA|=0x02;      

        SysCtlDelay(10);
        
				LCDPORT->DATA&=~(0x02);


        SysCtlDelay(50000);

        
				    LCDPORT->DATA=0x20;    

       
				LCDPORT->DATA|=0x02;      

        SysCtlDelay(10);
      
			 LCDPORT->DATA&=~(0x02);


        SysCtlDelay(50000);


        LCD_Command(0x0F); //Turn on Lcd
        LCD_Clear(); //Clear screen

}

void LCD_Command(unsigned char c) {
				
        
	LCDPORT->DATA=(c&0xF0);
        
	LCDPORT->DATA&=~(0x01);
       
	LCDPORT->DATA|=0x02;
        SysCtlDelay(50000);

        
	LCDPORT->DATA&=~(0x02);
        SysCtlDelay(50000);

        
					LCDPORT->DATA=((c & 0x0F)<<4);
				
        LCDPORT->DATA&=~(0x01);
				
		LCDPORT->DATA|=0x02;


        SysCtlDelay(10);

       
					LCDPORT->DATA&=~(0x02);


        SysCtlDelay(50000);

}

void LCD_Show(unsigned char d) {

        
		LCDPORT->DATA=(d&0xF0);

        
		LCDPORT->DATA|=0x01;

        
				LCDPORT->DATA|=0x02;

        SysCtlDelay(10);
       
						LCDPORT->DATA&=~(0x02);

        SysCtlDelay(50000);

        
						LCDPORT->DATA=((d & 0x0F)<<4);

        
			LCDPORT->DATA|=0x01;

        
								LCDPORT->DATA|=0x02;


        SysCtlDelay(10);
       
										LCDPORT->DATA&=~(0x02);

        SysCtlDelay(50000);

}

void LCD_Cursor(char x, char y){

    if (x==0) {
        LCD_Command(0x80 + (y % 16));
        return;
    }
    LCD_Command(0xC0 + (y % 16));

}

void LCD_Clear(void){

        LCD_Command(0x01);
        SysCtlDelay(10);

}


void LCD_Yaz(char* s){

    int j, p=1, i;
    for (j=0; j<strlen(s)||j<15; j++) {
        LCD_Cursor(0, 15-j);
        for (i=0; i<strlen(s); i++) {
            LCD_Show(s[i]);
        }

        SysCtlDelay(8000000/3);
    }


    if (strlen(s)>16) {
        while (p < strlen(s)-16) {
            LCD_Cursor(0,0);
            for (j=0; j<16; j++) {
                LCD_Show(s[p+j]);
            }
            SysCtlDelay(800000/3);
            p++;
        }
        i = p;
        while (p < strlen(s) + i) {
            LCD_Cursor(0,0);
            for (j=0; j<16; j++) {
                LCD_Show(s[(p + j) % strlen(s)]);
            }
            SysCtlDelay(800000/3);
            p++;
        }
    }
    LCD_Command(0xC0 + 16); //Hide cursor
}


void LCD_PrintJustify(char i, char *s, char *d) {
    if (i==0) {
        for (i=0; i<strlen(s); i++) {
            LCD_Cursor(0, i);
            LCD_Show(s[i]);
        }
        for (i=0; i<strlen(d); i++) {
            LCD_Cursor(0, 15-i);
            LCD_Show(d[strlen(d)-i-1]);
        }
        LCD_Command(0xC0 + 16);
        return;
    }
    for (i=0; i<strlen(s); i++) {
        LCD_Cursor(1, i);
        LCD_Show(s[i]);
    }
    for (i=0; i<strlen(d); i++) {
        LCD_Cursor(1, 15-i);
        LCD_Show(d[strlen(d)-i-1]);
    }
    LCD_Command(0xC0 + 16); //Hide cursor
}

void LCD_Print(char *s, char *d) {
    int j;
    for (j=0; j<16; j++) {
        if (j<strlen(s)) {
            LCD_Cursor(0,j);
            LCD_Show(s[j]);
        }
        if (j<strlen(d)) {
            LCD_Cursor(1,j);
            LCD_Show(d[j]);
        }
    }
    LCD_Command(0xC0 + 16); //Hide cursor
}

void LCD_PrintLn(char i, char *s) {
    LCD_Cursor(i, 0);
    for (i=0; i<strlen(s); i++) {
        LCD_Show(s[i]);
    }
    LCD_Command(0xC0 + 16); //Hide cursor
}

void SysCtlDelay(long delay){
	unsigned long volatile time;
  time = 727240*20/91;  // 0.1sec
  while(time){
		time--;
  }
}
