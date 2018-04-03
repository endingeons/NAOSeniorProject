const int buttonPin = 7;
int buttonState = 0;

void setup() {
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH)
  {
    Serial.println("push");
  }
  else
  {
    Serial.println("not push");
  }
}
