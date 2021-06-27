
#define S0 8
#define S1 9
#define S2 12
#define S3 11
#define sensorOut 10
#define but 13


int rpin = 4;
int gpin = 3;
int bpin = 2;

int frequency = 0;
int red = 0;
int green = 0;
int blue = 0;
int buttonState = 0;

int no_r  = 340;
int max_r = 80;
int no_g  = 330;
int max_g = 80;
int no_b  = 235;
int max_b = 59;


void light_glow(int r, int g, int b, int rpin, int gpin, int bpin) {
  analogWrite(rpin,r);
  analogWrite(gpin,g);
  analogWrite(bpin,b);
}


void light_down(int rpin, int gpin, int bpin) {
  analogWrite(rpin,0);
  analogWrite(gpin,0);
  analogWrite(bpin,0);
}

void twinkling(int sec) {
  digitalWrite(rpin,LOW);
  digitalWrite(gpin,LOW);  
  digitalWrite(bpin,LOW);
  for (int i=0;i<sec;i++) {
    for (int j=0;j<5;j++) {
      light_glow(57, 197, 187, rpin, gpin, bpin);
      delay(100);
      light_down(rpin, gpin, bpin);
      delay(100);
    }
  }
}


int look_r() {
  // Setting red filtered photodiodes to be read
  digitalWrite(S2,LOW);
  digitalWrite(S3,LOW);
  
  // Reading the output frequency
  frequency = pulseIn(sensorOut, LOW);

  return frequency;
}


int map_r(int no_r, int max_r, int frequency) {

  //Remaping the value of the frequency to the RGB Model of 0 to 255
  //red = map(frequency, 80,340,255,0);
  red = map(frequency, max_r, no_r, 255, 0);
  if (red < 0) {
    red = 0;
  }
  if (red > 255) {
    red = 255;
  }   
  // Printing the value on the serial monitor
  Serial.print("R= ");//printing name
  Serial.print(frequency);//printing RED color frequency
  Serial.print("  ");
  //delay(100);

  return red;
}

int look_g() {
  // Setting Green filtered photodiodes to be read
  digitalWrite(S2,HIGH);
  digitalWrite(S3,HIGH);
  
  // Reading the output frequency
  frequency = pulseIn(sensorOut, LOW);

  return frequency;
}
  
int map_g(int no_g, int max_g, int frequency) {

  //Remaping the value of the frequency to the RGB Model of 0 to 255
  //green = map(frequency, 80,330,255,0);
  green = map(frequency, max_g, no_g,255,0);
  if (green < 0) {
    green = 0;
  }
  if (green > 255) {
    green = 255;
  } 
  // Printing the value on the serial monitor
  Serial.print("G= ");//printing name
  Serial.print(frequency);//printing RED color frequency
  Serial.print("  ");
  //delay(100);

  return green;
}

int look_b() {
  // Setting Blue filtered photodiodes to be read
  digitalWrite(S2,LOW);
  digitalWrite(S3,HIGH);
  // Reading the output frequency
  frequency = pulseIn(sensorOut, LOW);

  return frequency;
}

int map_b(int no_b, int max_b, int frequency) {

  //Remaping the value of the frequency to the RGB Model of 0 to 255
  //blue = map(frequency, 59,235,255,0);
  blue = map(frequency, max_b,no_b,255,0);
  if (blue < 0) {
    blue = 0;
  } 
  if (blue > 255) {
    blue = 255;
  } 
  // Printing the value on the serial monitor
  Serial.print("B= ");//printing name
  Serial.print(frequency);//printing RED color frequency
  Serial.print("  ");

  return blue;
}



void setup() {
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(rpin, OUTPUT);
  pinMode(gpin, OUTPUT);
  pinMode(bpin, OUTPUT);
  pinMode(sensorOut, INPUT);
  pinMode(but, INPUT);
  
  // Setting frequency-scaling to 20%
  digitalWrite(S0,HIGH);
  digitalWrite(S1,LOW);
  
  Serial.begin(9600);
}

//80 80 59
//340 330 235
void loop() {

  buttonState = digitalRead(but);  //讀取按鍵的狀態
  
  if (!buttonState) {
    twinkling(3);
    light_glow(57, 197, 187, rpin, gpin, bpin);
    delay(1000);
    light_down(rpin, gpin, bpin);
    //white
    max_r = look_r();
    max_g = look_g();
    max_b = look_b();
    
    twinkling(3);
    light_glow(57, 197, 187, rpin, gpin, bpin);
    delay(1000);
    light_down(rpin, gpin, bpin);
    //black
    no_r = look_r();
    no_g = look_g();
    no_b = look_b();
    
  }
  
  red   = map_r(no_r, max_r, look_r());
  green = map_g(no_g, max_g, look_g());
  blue  = map_b(no_b, max_b, look_b());


  Serial.print("(");
  Serial.print(red);
  Serial.print(",");
  Serial.print(green);
  Serial.print(",");
  Serial.print(blue);
  Serial.print(")");
  Serial.print("  ");
  Serial.print(buttonState);
  Serial.println("  ");

  analogWrite(rpin,red);
  analogWrite(gpin,green);
  analogWrite(bpin,blue);

  delay(100);
}
