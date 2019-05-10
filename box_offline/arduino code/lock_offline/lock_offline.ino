
#include <Password.h> 
#include "Nextion.h"
#include <SoftwareSerial.h>

//------------------- Product ID --------------------------------

char ID[] ="boxy001" ;
char newPassword[6]; 
//--------------------------------------------------------------
// Master RX, TX, connect to Nextion TX, RX
SoftwareSerial HMISerial(10,11);


const int lockPin =  3;   
int count=0;

//char pass[12]="0066";
char* pass;
Password password = Password( "0066" );

char key;
// ------------Declaring nextion objects--------\\
NexText t0 = NexText(0, 13, "t0"); 
NexButton b0 = NexButton(0,2 , "b0");
NexButton b1 = NexButton(0,3 , "b1");
NexButton b2 = NexButton(0,4 , "b2");
NexButton b3 = NexButton(0,5 , "b3");
NexButton b4 = NexButton(0,6 , "b4");
NexButton b5 = NexButton(0,7 , "b5");
NexButton b6 = NexButton(0,8 , "b6");
NexButton b7 = NexButton(0,9 , "b7");
NexButton b8 = NexButton(0,10 , "b8");
NexButton b9 = NexButton(0,11 , "b9");
NexButton bEnter = NexButton(0,14 , "bEnter");
NexButton bReset = NexButton(0,12 , "bReset");


//----Register a button objects to the touch event list-----\\

NexTouch *nex_listen_list[] = {
  &b0,
  &b1,
  &b2,
  &b3,
  &b4,
  &b5,
  &b6,
  &b7,
  &b8,
  &b9,
  &bEnter,
  &bReset,
  NULL
};

void zero_PopCallback(void *ptr) {
  char num='0';
  password.append(num); 
}

void one_PopCallback(void *ptr) {
  
 char num='1';
  password.append(num);
}

void two_PopCallback(void *ptr) {
  
  char num='2';
  password.append(num);
}

void three_PopCallback(void *ptr) {
  
 char num='3';
  password.append(num);
}

void four_PopCallback(void *ptr) {
  
 char num='4';
  password.append(num);
}

void five_PopCallback(void *ptr) {
  
char num='5';
  password.append(num);
}

void six_PopCallback(void *ptr) {
  
 char num='6';
  password.append(num);
}

void seven_PopCallback(void *ptr) {
  char num='7';
  password.append(num);
}

void eight_PopCallback(void *ptr) {
  char num='8';
  password.append(num);
}

void nine_PopCallback(void *ptr) {
  
  char num='9';
  password.append(num);
}
void enter_PopCallback(void *ptr) {

  checkPassword();
// if(checkPassword())
// {
// t0.setText("unsuccessfull");
////  tState.setText("State: on");
//  }
}

void reset_PopCallback(void *ptr) {
  
  password.reset();
}


 

void setup() {

  pinMode(lockPin, OUTPUT);
  pinMode(lockPin, HIGH);
  
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
      

Serial.begin(9600);
 nexInit();

  HMISerial.begin(9600);
  //Serial.println("Hello Pi, I m ready");
 delay(500);
 //--------- Getting password from cloud API--------------- 
  
  Serial.println("query");
  delay(1000);
//  String incoming = "";  
//  incoming = Serial.readString();  
//  //Serial.println(incoming);     
//  incoming.toCharArray(newPassword, incoming.length()+1);
//  password.set(newPassword);


 //--- Register the pop event callback function of the key components

 b0.attachPop(zero_PopCallback, &b0);
 b1.attachPop(one_PopCallback, &b1);
 b2.attachPop(two_PopCallback, &b2);
 b3.attachPop(three_PopCallback, &b3);
 b4.attachPop(four_PopCallback, &b4);
 b5.attachPop(five_PopCallback, &b5);
 b6.attachPop(six_PopCallback, &b6);
 b7.attachPop(seven_PopCallback, &b7);
 b8.attachPop(eight_PopCallback, &b8);
 b9.attachPop(nine_PopCallback, &b9);
 bEnter.attachPop(enter_PopCallback, &bEnter);
 bReset.attachPop(reset_PopCallback, &bReset);
}

void loop() {
  // put your main code here, to run repeatedly:
 nexLoop(nex_listen_list);
 
//Serial.println(pass);

}

void checkPassword(){
  //bool flag;
  if (password.evaluate()){
    //Serial.println("Success");
   
    digitalWrite(lockPin, HIGH); // lock opens
    Serial.println("success");
    digitalWrite(LED_BUILTIN, HIGH);
    count=0;
    delay(15000);
    digitalWrite(lockPin, LOW);
    //return true
  }
  
  else{
   // Serial.println("Wrong");


   
    count++;
    if(count==3)
    {  // checks for three attmpts before generating API request for wrong password
    //add code to run if it didhh not work
    Serial.println("unsuccessfull");
       digitalWrite(LED_BUILTIN, LOW);
       delay(300);
              digitalWrite(LED_BUILTIN, HIGH);
       delay(300);
              digitalWrite(LED_BUILTIN, LOW);
       delay(300);
          digitalWrite(LED_BUILTIN, HIGH);
       delay(300);
              digitalWrite(LED_BUILTIN, LOW);
       delay(300);
       delay(300);
              digitalWrite(LED_BUILTIN, LOW);
       delay(300);
    count=0;
    }
   // return false;
  }
}
