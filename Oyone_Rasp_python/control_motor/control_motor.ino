const int EnableL = 6;   //pwm,ENB
const int in3 = 8;       // LEFT SIDE MOTOR
const int in4 = 7;

const int EnableR = 11;    //pwm,ENA
const int in1 = 13;       //RIGHT SIDE MOTOR
const int in2 = 12; 

#define max_speed 255
#define min_speed 0
#define right_motor_power 200
#define left_motor_power 100 

void setup() 
{
  pinMode(EnableL, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  pinMode(EnableR, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  Serial.begin(115200);
}

void Forward()
{
  analogWrite(EnableL, 0);
  analogWrite(EnableR, 0);
  
  digitalWrite(in4, HIGH); //LOW HIGH
  digitalWrite(in3, LOW);
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(EnableL, left_motor_power); //120
  analogWrite(EnableR, right_motor_power);//30
//  delay(1000);
}

void Stop()
{
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(EnableL,0);

  digitalWrite(in2, HIGH);
  digitalWrite(in1, LOW);
  analogWrite(EnableR,0);
//  delay(1000);
  
}

void Back()
{
  analogWrite(EnableL, 0);
  analogWrite(EnableR, 0);
  
  digitalWrite(in4, LOW); //LOW HIGH
  digitalWrite(in3, HIGH);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(EnableL,left_motor_power); //120
  analogWrite(EnableR,right_motor_power);//30
}

// Function when you want to go left
void Left() 
{
 digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(EnableL,0); 
  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(EnableR,right_motor_power);
//  delay(1000);
  
}


// Function when you want to go right
void Right() 
{
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(EnableL,left_motor_power); 
  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(EnableR,0);
//  delay(1000);
  
}

void run_straight(){
  char instruction;
// Serial.flush();
    instruction = (char)Serial.read();
    if(instruction=='r'){
        Right();
    }
    else if(instruction=='l'){
        Left();
    }
    else if(instruction=='f'){
        Forward();
    }
    else if(instruction=='b'){
        Back();
    }
    else {
        Stop();
    }
    Serial.print(instruction);
}

void loop()
{
    if(Serial.available()){
        run_straight();
        
    }
}
