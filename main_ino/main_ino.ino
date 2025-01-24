#include <Wire.h> 
#include <PRIZM.h>
PRIZM prizm;

String inputString = "";
boolean stringComplete = false;
String outputString = "";

int cmd = 0;
String cmdStr = "";

void setup() {
  prizm.PrizmBegin();
  prizm.setMotorInvert(1,1);                             
  
  // reserve 20/10 bytes for the string:
  inputString.reserve(20);
  outputString.reserve(20);
  cmdStr.reserve(10);
  
  Serial.begin(9600);
}

void loop() {
  if (stringComplete) {
    inputString.trim();
    cmd = inputString.substring(0,1).toInt(); 
    if(inputString.length() > 1) {
        cmdStr = inputString.substring(1);
        cmdStr.trim();
    }

    switch (cmd) {

      case 0:{// Acknowledge
        outputString += "0";
        break;
      }
      case 1:{ // move forward
        outputString += "1";
        int power = cmdStr.toInt();
        prizm.setMotorPowers(power, power);
        break;
      }
      case 2:{ // turn left
        outputString += "2";
        int power = cmdStr.toInt();
        prizm.setMotorPowers(power * -1, power);
        break;
      }
      case 3:{ // turn right
        outputString += "3";
        int power = cmdStr.toInt();
        prizm.setMotorPowers(power, power * -1);
        break;
      }
      case 4:{ // move backward
        outputString += "4";
        int power = cmdStr.toInt();
        power = power * (-1); // Invert
        prizm.setMotorPowers(power, power);
        break;
      }
      case 5:{ // break the motor
        outputString += "5";
        prizm.setMotorPowers(125,125);
        break;
      }
      case 6:{ // read sonic sensor
        int port = cmdStr.toInt();
        outputString += prizm.readSonicSensorIN(port);
        break;
      }
      default: {
        outputString += "ack-error";
        break;
      }
    }
    
    Serial.println(outputString);
    resetVariables();
  }
}

// Reads input from the Serial and adds it to inputString.
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read(); 
    inputString += inChar;

    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}

void resetVariables() {
    inputString = "";
    outputString = "";
    cmdStr = "";
    cmd = 0;
    stringComplete = false;
}
