#include <Servo.h>

#define BASE 3 //본체
#define ELBOW 5 //2관절
#define GRIPPER 6 //집게관절
#define GRIP 9 //3관절
#define WRIST 10 //1관절
#define SHOULDER 11 //집기

Servo myservo,S1,S2,S3,S4,S5,S6; 

int pos1 = 0;
int pos2 = 0;
int pos3 = 0;
int pos4 = 0;
int pos5 = 0;
int pos6 = 0;
//각도 설정    
int PUL = 8; //PULSE 8번핀
int DIR = 7; //DIRECT 7번핀
int microStep; //1 증가시킬때마다 레일이 0.5cm씩 이동
int rotation = 1500; //회전수
unsigned int i;
char value = 'Z';
byte val[5];
int val2[5];


void setup() {
  S1.attach(BASE);
  S2.attach(ELBOW);
  S3.attach(GRIPPER);
  S4.attach(GRIP);
  S5.attach(WRIST);
  S6.attach(SHOULDER);
  Serial.begin(9600);
  while(!Serial);
  Serial.setTimeout(5);

  

  S1.write(180);
  S2.write(90);
  S3.write(90);
  S4.write(90);
  S5.write(90);
  S6.write(90);
  delay(1500); //초기값 설정, 로봇팔의 위치를 고정시킴
  
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT);
  delay(100);
 
}

void loop() {
   delay(1000);//초기값 설정을 위한 시간 지연

   if(Serial.available()>0)
   {
    Serial.readBytes(val, sizeof(val));
    
    for(int i = 0; i< sizeof(val);i++) {
    val2[i] = int(val[i]);
    }
   
  
  /*if문 시작*/




  if(val2[0]== 2)//인식한 물체가 플라스틱인 경우{

   microStep = val2[1];
   digitalWrite(DIR,LOW);
  for(i=0;i<(microStep*rotation);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10);
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//집을 물체까지 레일 오른쪽으로 이동
  
  for (pos5 = 90; pos5 <= 170; pos5 += 1) {
    S5.write(pos5);              
    delay(10);
  }//제 1관절 170도까지 앞으로 꺾이게



  for (pos2 = 90; pos2 >= val2[2]; pos2 -= 1) {
    S2.write(pos2);              
    delay(10); //S5가 160일때 라즈베리파이에서 전송받은 y축위치로 이동
  }
  
  for (pos6 = 90; pos6 <= 145; pos6 += 1) {
    S6.write(pos6);              
    delay(10);//집게로 물체 집기
  }
  for (pos5 = 170; pos5 >=110; pos5 -= 1) {
    S5.write(pos5);              
    delay(10);//제 1관절 살짝 들기
  }

  for (pos2= val2[2]; pos2 <= 90; pos2 += 1) {
    S2.write(pos2);              
    delay(10);// y축위치 원위치         
  }

   digitalWrite(DIR,LOW);
  for(i=0;i<(65000-microStep*rotation);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10);
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//기준점으로 레일 오른쪽으로 이동
    
  digitalWrite(DIR,LOW);
  for(i=0;i<(27000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10);
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//레일 오른쪽으로 이동

  

  digitalWrite(DIR,LOW);
  for(i=0;i<(28000);i++)
  {
    digitalWrite(PUL,HIGH);
    
    delayMicroseconds(10);
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//해당 쓰레기통 위치로 레일 오른쪽으로 이동

  digitalWrite(DIR,LOW);
  for(i=0;i<(27000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10);
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//해당 쓰레기통 위치로 레일 오른쪽으로 이동

  

  digitalWrite(DIR,LOW);
  for(i=0;i<(28000);i++)
  {
    digitalWrite(PUL,HIGH);
    
    delayMicroseconds(10);
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//해당 쓰레기통 위치로 레일 오른쪽으로 이동

  for (pos5 = 110; pos5 >=90; pos5 -= 1) {
    S5.write(pos5);              
    delay(10);//제 1관절 초기값대로 원위치
   }

  for (pos6 = 145; pos6 >= 90; pos6 -= 1) {
    S6.write(pos6);              
    delay(10);
  }//쓰레기통 위치에서 물체 놔버리기

  digitalWrite(DIR,HIGH);
  for(i=0;i<(30000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10); //속도
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//레일 초기값으로 왼쪽으로 이동

  digitalWrite(DIR,HIGH);
  for(i=0;i<(35000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10); //속도
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//레일 초기값으로 왼쪽으로 이동

  
  digitalWrite(DIR,HIGH);
  for(i=0;i<(28000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10); //속도
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//레일 초기값으로 왼쪽으로 이동

 digitalWrite(DIR,HIGH);
  for(i=0;i<(27000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10); //속도
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//레일 초기값으로 왼쪽으로 이동

  
  digitalWrite(DIR,HIGH);
  for(i=0;i<(28000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10); //속도
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//레일 초기값으로 왼쪽으로 이동

 digitalWrite(DIR,HIGH);
  for(i=0;i<(27000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10); //속도
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//레일 초기값으로 왼쪽으로 이동
  
 }
  
  else if(val2[0]== 1)//인식한 물체가 캔인경우{

    microStep = val2[1];
   digitalWrite(DIR,LOW);
  for(i=0;i<(microStep*rotation);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10);
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//레일 해당 물체위치로 오른쪽으로 이동
  
  for (pos5 = 90; pos5 <= 170; pos5 += 1) {
    S5.write(pos5);              
    delay(10);
  }//제 1관절 170도까지 앞으로 꺾이게



  for (pos2 = 90; pos2 >= val2[2]; pos2 -= 1) {
    S2.write(pos2);              
    delay(10); //S5가 170일때 라즈베리파이에서 전송한 y좌표값으로 이동
  }
  for (pos6 = 90; pos6 <= 155; pos6 += 1) {
    S6.write(pos6);              
    delay(10);//집게로 물체 집기
  }
  for (pos5 = 170; pos5 >=130; pos5 -= 1) {
    S5.write(pos5);              
    delay(10);//제 1관절 살짝 들기
  }

  for (pos2= val2[2]; pos2 <= 90; pos2 += 1) {
    S2.write(pos2);              
    delay(10);//y좌표 원위치
  }

  for (pos5 = 130; pos5 >=90; pos5 -= 1) {
    S5.write(pos5);              
    delay(10);//제 1관절 초기값대로 원위치
   }

   digitalWrite(DIR,LOW);
  for(i=0;i<(65000-microStep*rotation);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10);
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//레일 해당 쓰레기통으로 오른쪽으로 이동
    
  digitalWrite(DIR,LOW);
  for(i=0;i<(28000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10);
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//레일 해당 쓰레기통으로 오른쪽으로 이동

   digitalWrite(DIR,LOW);
  for(i=0;i<(27000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10);
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//레일 해당 쓰레기통으로 오른쪽으로 이동


  for (pos6 = 155; pos6 >= 90; pos6 -= 1) {
    S6.write(pos6);              
    delay(10);
  }//쓰레기통 위치에서 물체 놔버리기

  digitalWrite(DIR,HIGH);
  for(i=0;i<(30000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10); //속도
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//초기값으로 왼쪽으로 이동

  digitalWrite(DIR,HIGH);
  for(i=0;i<(35000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10); //속도
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//초기값으로 왼쪽으로 이동

  
  digitalWrite(DIR,HIGH);
  for(i=0;i<(27000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10); //속도
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//초기값으로 왼쪽으로 이동

  digitalWrite(DIR,HIGH);
  for(i=0;i<(28000);i++)
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(10); //속도
    digitalWrite(PUL,LOW);
    delayMicroseconds(10);
  }//초기값으로 왼쪽으로 이동
 }



}
  delay(1000);
  

 }
