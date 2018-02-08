
#include "GY_85.h"
#include <Wire.h>

GY_85 GY85;     //create the object
GY_85 second;

int oldgx = 0;

void setup()
{
    Wire.begin();
    delay(10);
    Serial.begin(9600);
    delay(10);
    GY85.init();
    delay(10);
}


void loop()
{
    int ax = GY85.accelerometer_x( GY85.readFromAccelerometer() );
    int ay = GY85.accelerometer_y( GY85.readFromAccelerometer() );
    int az = GY85.accelerometer_z( GY85.readFromAccelerometer() );
    
    int cx = GY85.compass_x( GY85.readFromCompass() );
    int cy = GY85.compass_y( GY85.readFromCompass() );
    int cz = GY85.compass_z( GY85.readFromCompass() );

    int cx2 = second.compass_x( second.readFromCompass() );

    float gx = GY85.gyro_x( GY85.readGyro() );
    float gy = GY85.gyro_y( GY85.readGyro() );
    float gz = GY85.gyro_z( GY85.readGyro() );
    float gt = GY85.temp  ( GY85.readGyro() );

//    Serial.println  ( "accelerometer" );
//    Serial.print  ( " x:" );
//    Serial.print  ( ax );
//    Serial.print  ( " y:" );
//    Serial.print  ( ay );
//    Serial.print  ( " z:" );
//    Serial.println  ( az );
    
//    Serial.println  ( "  compass" );
//    Serial.print  ( " x:" );
//    Serial.print  ( cx );
//    Serial.print  ( " y:" );
//    Serial.print  ( cy );
//    Serial.print  (" z:");
//    Serial.println  ( cz );
    
//    Serial.println  ( "  gyro" );
//    Serial.print  ( " x:" );
//    Serial.print  ( gx );
//    Serial.print  ( " y:" );
//    Serial.print  ( gy );
//    Serial.print  ( " z:" );
//    Serial.print  ( gz );
//    Serial.print  ( " gyro temp:" );
//    Serial.println( gt );


    Serial.print("LShoulderPitch ");
    Serial.print(ay*(-1)); //Shoulder Pitch Ranges from -119 to 120
    Serial.println();

    Serial.print("LShoulderRoll ");
    Serial.print( (((cx - (-600))*90)/700) + (77) - 20 ); //Shoulder Roll Ranges from -18 to 77
    Serial.println();
//
////oldrange: 100 to -600
////new range: -18 to 77
////newvalue = ((cx - oldmin)*newrange)/oldrange + newmin
//
//    Serial.print("LElbowRoll ");
//    Serial.print("0"); //Elbow Roll Ranges from -88 to -3
//    Serial.println();

    if(abs(gx) > 10)
    {
      oldgx = gx + oldgx;
      Serial.print("LWristYaw ");
      Serial.print(oldgx); //Wrist Yaw Ranges from -104 to 105
      Serial.println();
    }
    
    delay(2000);             // only read every 0,5 seconds, 10ms for 100Hz, 20ms for 50Hz
}
