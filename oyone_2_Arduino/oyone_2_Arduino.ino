#include <QMC5883LCompass.h>
QMC5883LCompass compass;

const int EnableL = 6;   //pwm,ENB
const int in3 = 8;       // LEFT SIDE MOTOR
const int in4 = 7;

const int EnableR = 11;    //pwm,ENA
const int in1 = 12;       //RIGHT SIDE MOTOR
const int in2 = 13; 

#define max_speed 255
#define min_speed 0

int data;
int temp=0;
int x, y/*, z*/;
float Yaw,yawRaw,deltaYaw = 0;


void setup() 
{
  pinMode(EnableL, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  pinMode(EnableR, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  Serial.begin(9600, SERIAL_8N2);
  compass.init();
}

void Data()
{ //get the order from Raspberry Pi
  if(Serial.available()){
    data = Serial.read(); //input order(Serial)
  }
  else{
    data = 0; //no data:Stop
  }
}

void Forward()
{
  analogWrite(EnableL, 0);
  analogWrite(EnableR, 0);
  
  digitalWrite(in3, HIGH); //LOW HIGH
  digitalWrite(in4, LOW);
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(EnableL,200); //120
  analogWrite(EnableR,200);//30
  delay(1000);
}

void Stop()
{
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(EnableL,0);

  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(EnableR,0);
  
}

void Left() 
{
 digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(EnableL,0); 
  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(EnableR,150);
  
}

void Right() 
{
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(EnableL,150); 
  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(EnableR,0);
  
}

void turnRight() 
{
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(EnableL,120); 
  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(EnableR,60);
}

/*void turnLeft() 
{
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(EnableL,60); 
  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(EnableR,120);
  
}*/


float getYaw()
{ // Read compass values
  compass.read();

  // Return the values
  x = compass.getX();
  y = compass.getY();
  /*z = compass.getZ();*///kore_iru?
 
  float xHeading = atan2(y, x);

  // 0 <= xHeading < 2π
  if(xHeading < 0) xHeading += 2*PI;
  if(xHeading >= 2*PI) xHeading -= 2*PI;

  float xDegrees = xHeading * 180/PI;
  return xDegrees;
}

void loop() 
{
  float xDegrees = getYaw();   // = the angle from (magnetic) north

  int dir = ((int)xDegrees + 5) / 10; //10の位以上の数値を整数値(四捨五入)で取得(bit数の関係)
  dir = dir % 36;  //0<=dir<36
  if(Serial.available()){
    Serial.write(dir); //output(Serial)
  }
  Data();
  
  if(data==0) // No Signal
  {
    Stop();
  }
   
  else if(data==1)
  {
    Forward();
  }

  else if(data==2)
  {
    Right();
  }
     
  else if(data==3)
  {
    Left();
  }
     
  else if(data>4)
  {
    temp+=1;                     // creat parameter temp to count the number of turning
    if(temp==1||temp==2)     
    {
      yawRaw=getYaw();            //get the raw value of Yaw angle
      while(deltaYaw<=90)         // turn right until the deltaYaw =90
      {
        turnRight();
        delay(1000);
        Yaw=getYaw();             //update new Yaw value
        deltaYaw=fabs(Yaw-yawRaw);//calculate the deltaYaw
  
        delay(100); 
      }   
    }
    
    else if(temp==3||temp==4)
    {
      while(deltaYaw<=90)
      {
        turnRight();
        delay(1000);
        Yaw=getYaw();
        deltaYaw=fabs(Yaw-xDegrees);
        delay(100); 
      }
    }
    
    temp%=4;
  }
}
