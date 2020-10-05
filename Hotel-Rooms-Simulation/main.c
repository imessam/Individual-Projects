#include "tm4c123gh6pm.h"

#include "lcd.h"

#include "Keypad.h"

#include "string.h"

#include "UART.h"

#include <stdbool.h>


void init_portF(void); //Initiailze Port F

void toggleRedLed(void); // Toggle Red LED to indicate the guest has entered his room and is occupied instead of solenoid.

void toggleBlueLed(void); // Toggle Blue LED to indicate the room is locked.

void showMenu(void); // Show a menu to the user.

void setupRooms(void); // Setup rooms to enter the rooms number, set the status to "Locked" and password to "0000" for each room.

unsigned char selectOption(void); // Select an option from the menu.

int getRoomNumber(void); // Return the room number entered by the user.

void checkRoomStatus(int roomNo); /* Check a room status, status = 0 "Locked", status = 1 "Reserved", 
																	status = 2 "Occupied" status = 3 "Room Service"*/

void setRoomStatus(int roomNo); // Modify a room status from the receptionist.

void guestEntersRoom(int roomNo); /* A guest enters his reserved room by entering the room password from the keypad
																		, the room must be empty and reserved.*/

void guestCheckoutRoom(int roomNo); // Guest checkout from the receptionist a reserved room , the receptionist reset the password of the room.

unsigned char option;
int numberOfRooms;
int roomNumber;

char rooms[10][6]; /* Array of max 10 rooms,  rooms[i][0]=Room Status , rooms[i][1:4]= Room Password  , rooms[i][5]=Room Number
											status = 0 "Locked", status = 1 "Reserved", status = 2 "Occupied" status = 3 "Room Service" */
int main(void) {
	
	init_UART0(); // Initialize UART connection.
  LCD_init(); // Initialize LCD.
  init_portF();
	init_KEYPAD(); // Initialize Keypad.
  
		
		setupRooms();
		showMenu();

  while (1) {
		sendString("\n\r");
		
		option = selectOption();
		LCD_Show(option);
		sendChar(option);
		switch(option){
			case '1' : 
				if((roomNumber=getRoomNumber())==-1){
					LCD_Clear();
					LCD_Print("Invalid room","Number");
					delay();
				}
				else{
				checkRoomStatus(roomNumber);
				}
				break;
			case '2' :
				if((roomNumber=getRoomNumber())==-1){
					LCD_Clear();
					LCD_Print("Invalid room","Number");
					delay();
				}
				else{
				setRoomStatus(roomNumber);
				}
				break;
			case '3' :
				if((roomNumber=getRoomNumber())==-1){
					LCD_Clear();
					LCD_Print("Invalid room","Number");
					delay();
				}
				else{
				guestEntersRoom(roomNumber);
				}
					break;
			case '4' :
				if((roomNumber=getRoomNumber())==-1){
					LCD_Clear();
					LCD_Print("Invalid room","Number");
					delay();
				}
				else{
				guestCheckoutRoom(roomNumber);
				}
				break;
			case '0' :
				showMenu();
				break;
			default :
				showMenu();
		}
	}
	
}



void init_portF(void) {
	 SYSCTL -> RCGCGPIO |= 0x29;
  while ((SYSCTL -> PRGPIO & (0x29)) != (0x29)) {};
  GPIOF -> LOCK = 0x4C4F434B;
  GPIOF -> CR = 0x1F;
  GPIOF -> AMSEL = 0x00;
  GPIOF -> PCTL = 0x00;
  GPIOF -> DIR = 0x0E;
  GPIOF -> AFSEL = 0x00;
  GPIOF -> PUR = 0x11;
  GPIOF -> DEN = 0x1F;
			GPIOF -> DATA = 0x00;
}
	
void toggleRedLed(void){
	GPIOF -> DATA = 0x02;
	delay();
	GPIOF -> DATA = 0x00;
}
void toggleBlueLed(void){
	GPIOF -> DATA = 0x04;
	delay();
	GPIOF -> DATA = 0x00;
}

	
void showMenu(void){
	
		LCD_Clear();
		LCD_Print("Option 1 :","Check room status");
		delay();
		
		LCD_Clear();
		LCD_Print("Option 2 :","Set room status");
		delay();
		
		LCD_Clear();
		LCD_Print("Option 3 :","Guest enters");
		delay();
		
		LCD_Clear();
		LCD_Print("Option 4 :","Guest checkout");
		delay();
		
		LCD_Clear();
		LCD_Print("Option 0 :","Show this menu");
		delay();
	
	}
void setupRooms(void){
		char no;
		char roomNo;
	
		LCD_Clear();
		LCD_Print("Enter no of","rooms (0-9)");
		delay();
		
		LCD_Clear();
		LCD_Print("Number is",":");
		delay();
		
		sendString("No of Rooms : ");
		no=getChar();
		sendChar(no);
		LCD_Cursor('1','1');
		LCD_Show(no);
		delay();
		
		numberOfRooms=no-'0';
		for(int i=0;i<numberOfRooms;i++){
			
			LCD_Clear();
			LCD_Print("Enter room ","number :");
			delay();
		
			sendString(" //Room number : ");
			roomNo=getChar();
			sendChar(roomNo);
			LCD_Cursor('1','8');
			LCD_Show(roomNo);
			delay();
			
			
			rooms[i][0] ='0';
			rooms[i][1] ='0';
			rooms[i][2] ='0';
			rooms[i][3] ='0';
			rooms[i][4] ='0';
			rooms[i][5]=roomNo-'0';	
			toggleBlueLed();
		}
	}
unsigned char selectOption(void){
			LCD_Clear();
			LCD_Print("Enter option",":");
			LCD_Cursor('1','1');
			sendString(" //Option : ");
			return getChar();
	}

void checkRoomStatus(int roomNo){
		LCD_Clear();
		switch(rooms[roomNo][0]){
			case '0' :
				LCD_Print("Room ","Locked");
				break;
			case '1' :
				LCD_Print("Room ","Reserved");
				break;
			case '2' :
				LCD_Print("Room ","Occupied");
				break;
			case '3' :
				LCD_Print("Room ","Room Service");
				break;
			}
	}
	
int getRoomNumber(void){
		unsigned char c;
		int roomNo;
		LCD_Clear();
		LCD_Print("Room Number",": ");
		sendString(" //Room Number : ");
		c=getChar();
		sendChar(c);
		LCD_Cursor('1','1');
		LCD_Show(c);
		roomNo=c-'0';
		for(int i=0;i<numberOfRooms;i++){
			if(rooms[i][5]==roomNo){
				return i;
			}
		}
		return -1;
	}
	
void setRoomStatus(int roomNo){
		unsigned char status;
		unsigned char enteredPass[4];
		bool wrong=false;
		
		LCD_Clear();
		LCD_Print("Room Status 1 =","Reserved");
		delay();
		
		LCD_Clear();
		LCD_Print("Room Status 3 =","Room Service");
		delay();
		
		LCD_Clear();
		LCD_Print("Room Status",": ");
		LCD_Cursor('1','1');
		sendString(" //Room Status : ");
		
		
		status=getChar();
		sendChar(status);
		LCD_Show(status);		
		
		switch (status){
			case '1' :	{
				LCD_Clear();
				if(rooms[roomNo][0]!='0'){
					LCD_Print("Room already","reserved");
					break;
				}
				LCD_Print("Set Password",": ");
				LCD_Cursor('1','1');
				sendString(" //Set Password : ");
				
				rooms[roomNo][1]=getChar();
				sendChar(rooms[roomNo][1]);
				LCD_Show(rooms[roomNo][1]);
				
				rooms[roomNo][2]=getChar();
				sendChar(rooms[roomNo][2]);
				LCD_Show(rooms[roomNo][2]);
			
				rooms[roomNo][3]=getChar();
				sendChar(rooms[roomNo][3]);
				LCD_Show(rooms[roomNo][3]);
			
				rooms[roomNo][4]=getChar();
				sendChar(rooms[roomNo][4]);
				LCD_Show(rooms[roomNo][4]);
			
				rooms[roomNo][0]='1';
				break;
			}
			case '3' :	{
				if(rooms[roomNo][0]=='2'){
									LCD_Print("Cannot,someone","in the room");
					break;
				}
				LCD_Clear();
				LCD_Print("Enter Password",": ");
				LCD_Cursor('1','1');
				sendString(" //Enter Password : ");

				
			enteredPass[0]=getChar();
			sendChar(enteredPass[0]);
			LCD_Show(enteredPass[0]);
			
			enteredPass[1]=getChar();
			sendChar(enteredPass[1]);
			LCD_Show(enteredPass[1]);
			
			enteredPass[2]=getChar();
			sendChar(enteredPass[2]);
			LCD_Show(enteredPass[2]);
			
			enteredPass[3]=getChar();
			sendChar(enteredPass[3]);
			LCD_Show(enteredPass[3]);
			
			for(int i=1;i<5;i++){
				if(rooms[roomNo][i]!= enteredPass[i-1]){
					wrong=true;
					break;
				}
			}
			if(wrong){
				LCD_Clear();
				LCD_Print("Wrong Password","");
			}else{
				LCD_Clear();
				LCD_Print("Right Password","");
				rooms[roomNo][0]='3';
			}
			break;
		}
	}
}
	
void guestEntersRoom(int roomNo){
			LCD_Clear();
	if((rooms[roomNo][0]=='0') || (rooms[roomNo][0]=='2')){
		LCD_Print("Room Locked","or occupied");
	}else{
	unsigned char enteredPass[4];
	bool wrong=false;
	
	LCD_Print("Enter Password",": ");
	LCD_Cursor('1','1');
	sendString(" //Enter Password : ");
			
			//enteredPass[0]=getChar();
			while ((enteredPass[0] = readKey()) == 0) {}
      delay();
			while ((enteredPass[0] = readKey()) == 0) {}
			sendChar(enteredPass[0]);
			LCD_Show(enteredPass[0]);
			
			//enteredPass[1]=getChar();
			while ((enteredPass[1] = readKey()) == 0) {}
      delay();
			while ((enteredPass[1] = readKey()) == 0) {}
			sendChar(enteredPass[1]);
			LCD_Show(enteredPass[1]);
			
			//enteredPass[2]=getChar();
			while ((enteredPass[2] = readKey()) == 0) {}
      delay();
			while ((enteredPass[2] = readKey()) == 0) {}
			sendChar(enteredPass[2]);
			LCD_Show(enteredPass[2]);
			
			//enteredPass[3]=getChar();
			while ((enteredPass[3] = readKey()) == 0) {}
      delay();
			while ((enteredPass[3] = readKey()) == 0) {}
			sendChar(enteredPass[3]);
			LCD_Show(enteredPass[3]);
			
			for(int i=1;i<5;i++){
				if(rooms[roomNo][i]!= enteredPass[i-1]){
					wrong=true;
					break;
				}
			}
			if(wrong){
				LCD_Clear();
				LCD_Print("Wrong Password!","Try again later");
			}else{
				LCD_Clear();
				LCD_Print("Right Password!","Occupied");
				rooms[roomNo][0]='2';
				toggleRedLed();
			}
		}
}

void guestCheckoutRoom(int roomNo){
		LCD_Clear();
	if(rooms[roomNo][0]=='0'){
		LCD_Print("Cannot,this room","is locked ");
	
	}else{
				LCD_Print("Resetting Password",": ");
				
				rooms[roomNo][1]='0';
				rooms[roomNo][2]='0';
				rooms[roomNo][3]='0';
				rooms[roomNo][4]='0';
			
				rooms[roomNo][0]='0';
		toggleBlueLed();
	}

}

