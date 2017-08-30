int buttonInput = 7;
int buttonState = HIGH;

int state = 0;

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  pinMode(buttonInput, INPUT_PULLUP);
//  digitalWrite(buttonInput, HIGH);

}

void loop() {
  // put your main code here, to run repeatedly:
  buttonState = digitalRead(buttonInput);
  if(buttonState == LOW)
  {
    if(state == 0)
    {
      state = 1;
      Serial.println(state);
      delay(500);
    }

    else if(state == 1)
    {
      state = 0;  
      Serial.println(state);
      delay(500);
    }
  }


//  if(state == 0)
//  {
//    Serial.println("ArmModule");
//  }
//  else if(state == 1)
//  {
//    Serial.println("LegModule");
//  }
  
  delay(100);
}
