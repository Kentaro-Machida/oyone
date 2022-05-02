
const int EnableL = 6;   //pwm,ENB
const int in3 = 8;       // LEFT SIDE MOTOR
const int in4 = 7;

const int EnableR = 11;    //pwm,ENA
const int in1 = 12;       //RIGHT SIDE MOTOR
const int in2 = 13; 

#define max_speed 255
#define min_speed 0

void setup() 
{
  pinMode(EnableL, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  pinMode(EnableR, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  Serial.begin(9600);
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
//  delay(1000);
}

void Stop()
{
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(EnableL,0);

  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(EnableR,0);
//  delay(1000);
  
}

void Right() 
{
 digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(EnableL,0); 
  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(EnableR,150);
//  delay(1000);
  
}

void Left() 
{
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(EnableL,150); 
  
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
