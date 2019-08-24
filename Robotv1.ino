//********************************************
//* Robotic Arm 
//* for robotic arm 0
//* By Benny Lo
//* Jan 14 2018
//********************************************
#include <Servo.h>  
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#define ROBOT_NAME "BRobot-K"
#define CRAW_MIN 0 //open 
#define CRAW_MAX 58 //close
#define ELBOW_MIN   0
#define ELBOW_MAX 140
#define SHOULDER_MIN 0
#define SHOULDER_MAX 165
#define WRIST_X_MIN 0
#define WRIST_X_MAX 180
#define WRIST_Y_MIN 0
#define WRIST_Y_MAX 90
#define WRIST_Z_MIN 0
#define WRIST_Z_MAX 180
#define BASE_MIN 0
#define BASE_MAX 180
//#define ELBOW_DEFAULT 60
#define ELBOW_DEFAULT 50
//#define SHOULDER_DEFAULT 100
#define SHOULDER_DEFAULT 80
#define WRIST_X_DEFAULT 80
#define WRIST_Y_DEFAULT 90
#define WRIST_Z_DEFAULT 66
#define BASE_DEFAULT 90
//#define BASE_DEFAULT 65
#define CRAW_DEFAULT CRAW_MIN //fully opened
Servo myservoA;  
Servo myservoB;
Servo myservoC;
Servo myservoD;
Servo myservoE;
Servo myservoF;
Servo myservoG;//the craw
int i,pos,myspeed;
int sea,seb,sec,sed,see,sef,seg;


void myservosetup()  //set up the servo motors
{
   sea=myservoA.read();
   seb=myservoB.read();
   sec=myservoC.read();
   sed=myservoD.read();
   see=myservoE.read();
   sef=myservoF.read();
   seg=myservoG.read();
   
   myspeed=500;
   for(pos=0;pos<=myspeed;pos+=1)
   {
    myservoA.write(int(map(pos,1,myspeed,sea,ELBOW_DEFAULT)));
    myservoB.write(int(map(pos,1,myspeed,seb,SHOULDER_DEFAULT)));
    myservoC.write(int(map(pos,1,myspeed,sec,WRIST_X_DEFAULT)));
    myservoD.write(int(map(pos,1,myspeed,sed,WRIST_Y_DEFAULT)));
    myservoE.write(int(map(pos,1,myspeed,see,WRIST_Z_DEFAULT)));
    myservoF.write(int(map(pos,1,myspeed,sef,BASE_DEFAULT)));
    myservoG.write(int(map(pos,1,myspeed,seg,CRAW_DEFAULT)));    
    delay(1);
   }
}

void setup() 
{ 
  Serial.begin(9600);
  //pinMode(13, OUTPUT);   LED control
  
  myservoA.attach(2);  
  myservoB.attach(3); 
  myservoC.attach(4); 
  myservoD.attach(5); 
  myservoE.attach(6); 
  myservoF.attach(7);
  myservoG.attach(8); 
  
  myservoA.write(ELBOW_DEFAULT);
  myservoB.write(SHOULDER_DEFAULT);
  myservoC.write(WRIST_X_DEFAULT);
  myservoD.write(WRIST_Y_DEFAULT);
  myservoE.write(WRIST_Z_DEFAULT);
  myservoF.write(BASE_DEFAULT); 
  myservoG.write(CRAW_DEFAULT);    
 
  // advertise the service
   Serial.println(("Bluetooth device active, waiting for connections..."));
  Serial.print("Initialized");
}



void excution(char data[20])
{
  
  char* instruction[3];
  char* token = strtok(data, " ");
  int i = 0;
  while (token != NULL){
    instruction[i++] = token;
    token = strtok(NULL, " ");  
  }
  

  int degree = 0;  
  int this_max = 0;
  Servo *pointer = NULL;
  char buf[50];
  switch((int)*instruction[1]){
    case 65:
      pointer = &myservoA;
      this_max = ELBOW_MAX;
      break;
    case 66:
      pointer = &myservoB;
      this_max = SHOULDER_MAX;
      break;
    case 67:
      pointer = &myservoC;
      this_max = WRIST_X_MAX;
      break;
    case 68:
      pointer = &myservoD;
      this_max = WRIST_Y_MAX;
      break;
    case 69:
      pointer = &myservoE;
      this_max = WRIST_Z_MAX;
      break;
    case 70:
      pointer = &myservoF;
      this_max = BASE_MAX;
      break;
    case 71:
      pointer = &myservoG;
      this_max = CRAW_MAX;
      break;
    default:
//      sprintf(buf, "%s", "Command ERROR!");
//      Serial.println("Error");
      break;
  }
  
  if (strcmp(instruction[0], "SHOW") == 0){
    if (strcmp(instruction[1], "DEGREE") == 0){
      sprintf(buf, "%c %d %c %d %c %d %c %d %c %d %c %d %c %d %c", 'A', myservoA.read(),'B', myservoB.read(),'C', myservoC.read(),
      'D', myservoD.read(),'E', myservoE.read(),'F', myservoF.read(),'G', myservoG.read(), '\0');
      Serial.println(buf);
    }
 
    return;
  }
  else if (strcmp(instruction[0], "SET") == 0){
    degree = atoi(instruction[2]);
  }
  else if (strcmp(instruction[0], "ADD") == 0){
    degree = atoi(instruction[2]) + pointer->read();
  }
  else if (strcmp(instruction[0], "MINUS") == 0){
    degree = pointer->read() - atoi(instruction[2]);
  }
  else{
    return;
  }
  
  if (degree < 0){
    degree = 0;
    sprintf(buf, "%c %s %c", '\t', "Error, degree should not below 0;", '\0');
    Serial.println(buf);
    return;
  }
  
  if (degree > this_max){
    degree = this_max;
    sprintf(buf, "%c %s %d %c", '\t', "Error, degree should not over ", this_max, '\0');
    Serial.println(buf);
    return;
  }
  sprintf(buf, "%c %s %s %c %s %d %c %s %d", '\t', "Operation on: ", instruction[1], '\t',
          "Original: ", pointer->read(), '\t', "Current: ", degree);
  Serial.println(buf);
  pointer->write(degree);
}

int incomingByte = 0;
char instruction[20];
int start = 0;

char buffer[18];
void loop() {
  // Try to get the data from serial port
  if (Serial.available() > 0) {    
    int index = 0;
    delay(100);
    int numChar = Serial.available();
    if (numChar>15) {
      numChar=15;
    }
    char c;
    memset(buffer, '\0', sizeof(buffer));
    while (numChar--) {
      c = Serial.read();
      if (c != char(10)){
        buffer[index++] = c;
      }
    }
    Serial.println(buffer);
    excution(buffer);
    Serial.flush();
  }
 
}
