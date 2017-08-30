#include <Wire.h>
#include "paj7620.h"
#include "GY_85.h"

GY_85 GY85;     //create the object
int buttonInput = 7; //PIN the button is connected to
int buttonState = HIGH;
int state = 0;

int oldgx = 0;

/* 
Notice: When you want to recognize the Forward/Backward gestures, your gestures' reaction time must less than GES_ENTRY_TIME(0.8s). 
        You also can adjust the reaction time according to the actual circumstance.
*/
#define GES_REACTION_TIME   900       // You can adjust the reaction time according to the actual circumstance.
#define GES_ENTRY_TIME      800       // When you want to recognize the Forward/Backward gestures, your gestures' reaction time must less than GES_ENTRY_TIME(0.8s). 
#define GES_QUIT_TIME       1200
#define GES_FWD_BWD_TIME    2000

void setup()
{
  Serial.begin(9600);
  pinMode(buttonInput, INPUT_PULLUP);

  /* Arm Module Setup Begin */
  Wire.begin();
  delay(10);
  delay(10);
  GY85.init();
  delay(10);
  /* Arm Module Setup End */
    
  /* Leg Module Setup Begin */
  uint8_t error = 0;
  /* Leg Module Setup End */
}

void loop()
{
//  buttonState = digitalRead(buttonInput);
//  if(buttonState == LOW)
//  {
//    if(state == 0)
//    {
//      state = 1;
//      Serial.println(state);
//      delay(500);
//    }
//
//    else if(state == 1)
//    {
//      state = 0;  
//      Serial.println(state);
//      delay(500);
//    }
//  }
  ArmModule();
  LegModule();
}

void ArmModule()
{
  int ax = GY85.accelerometer_x( GY85.readFromAccelerometer() );
  int ay = GY85.accelerometer_y( GY85.readFromAccelerometer() );
  int az = GY85.accelerometer_z( GY85.readFromAccelerometer() );
    
  int cx = GY85.compass_x( GY85.readFromCompass() );
  int cy = GY85.compass_y( GY85.readFromCompass() );
  int cz = GY85.compass_z( GY85.readFromCompass() );

  float gx = GY85.gyro_x( GY85.readGyro() );
  float gy = GY85.gyro_y( GY85.readGyro() );
  float gz = GY85.gyro_z( GY85.readGyro() );
  float gt = GY85.temp  ( GY85.readGyro() );

  Serial.println();
  Serial.print("LShoulderPitch ");
  Serial.print(ay*(-1)); //Shoulder Pitch Ranges from -119 to 120
  Serial.println();

  Serial.print("LShoulderRoll ");
  Serial.print( (((cx - (-600))*90)/700) + (77) * (1) ); //Shoulder Roll Ranges from -18 to 77
  Serial.println();

//oldrange: 100 to -600
//new range: -18 to 77
//newvalue = ((cx - oldmin)*newrange)/oldrange + newmin

//    Serial.println((((cx - 100)*90)/700) + (-18));

  Serial.print("LElbowRoll ");
  Serial.print("0"); //Elbow Roll Ranges from -88 to -3
  Serial.println();

  if(abs(gx) > 10)
  {
    oldgx = gx + oldgx;
    Serial.print("LWristYaw ");
    Serial.print(oldgx); //Wrist Yaw Ranges from -104 to 105
    Serial.println();
  }

  else{Serial.println();}
    
  delay(1000);             // only read every 0,5 seconds, 10ms for 100Hz, 20ms for 50Hz
}

void LegModule()
{
  uint8_t data = 0, data1 = 0, error;
  
  error = paj7620ReadReg(0x43, 1, &data);       // Read Bank_0_Reg_0x43/0x44 for gesture result.
  if (!error) 
  {
    switch (data)                   // When different gestures are detected, the variable 'data' will be set to different values by paj7620ReadReg(0x43, 1, &data).
    {
      case GES_RIGHT_FLAG:
        delay(GES_ENTRY_TIME);
        paj7620ReadReg(0x43, 1, &data);
        if(data == GES_FORWARD_FLAG) 
        {
          Serial.println("s");
          delay(GES_QUIT_TIME);
        }
        else if(data == GES_BACKWARD_FLAG) 
        {
          Serial.println("ignore");
          delay(GES_QUIT_TIME);
        }
        else
        {
          Serial.println("r");
        }          
        break;
      case GES_LEFT_FLAG: 
        delay(GES_ENTRY_TIME);
        paj7620ReadReg(0x43, 1, &data);
        if(data == GES_FORWARD_FLAG) 
        {
          Serial.println("s");
          delay(GES_QUIT_TIME);
        }
        else if(data == GES_BACKWARD_FLAG) 
        {
          Serial.println("ignore");
          delay(GES_QUIT_TIME);
        }
        else
        {
          Serial.println("l");
        }          
        break;
      case GES_UP_FLAG:
        delay(GES_ENTRY_TIME);
        paj7620ReadReg(0x43, 1, &data);
        if(data == GES_FORWARD_FLAG) 
        {
          Serial.println("s");
          delay(GES_QUIT_TIME);
        }
        else if(data == GES_BACKWARD_FLAG) 
        {
          Serial.println("ignore");
          delay(GES_QUIT_TIME);
        }
        else
        {
          Serial.println("f");
        }          
        break;
      case GES_DOWN_FLAG:
        delay(GES_ENTRY_TIME);
        paj7620ReadReg(0x43, 1, &data);
        if(data == GES_FORWARD_FLAG) 
        {
          Serial.println("s");
          delay(GES_QUIT_TIME);
        }
        else if(data == GES_BACKWARD_FLAG) 
        {
          Serial.println("ignore");
          delay(GES_QUIT_TIME);
        }
        else
        {
          Serial.println("b");
        }          
        break;
      case GES_FORWARD_FLAG:
        Serial.println("s");
        delay(GES_FWD_BWD_TIME); 
       paj7620ReadReg(0x43, 1, &data);
        /*if(data == GES_BACKWARD_FLAG) 
        {
          //Serial.println("Backward after forward");
          delay(GES_QUIT_TIME);
        }*/
        delay(GES_QUIT_TIME);
        break;
      case GES_BACKWARD_FLAG: 
        Serial.println("ignore");
        delay(GES_QUIT_TIME);
        break;
      case GES_CLOCKWISE_FLAG:
        Serial.println("c");
        break;
      case GES_COUNT_CLOCKWISE_FLAG:
        Serial.println("k");
        break;  
      default:
        paj7620ReadReg(0x44, 1, &data1);
        if (data1 == GES_WAVE_FLAG) 
        {
          Serial.println("w");
        }
        break;
    }
  }
  delay(100);
}



