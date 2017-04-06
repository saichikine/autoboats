/*******************************************************************************

    This file was written to be used with SerialControl.

    SerialControl is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

*******************************************************************************/

void rampWriteFunc(){
  int pin = parseArgument(AR1);
  float value = parseArgument(AR2);
  int t = parseArgument(AR3);
  float val = 0;
  int curr;
  if(pin == 3){
    curr = glob3;
  }
  if(pin == 9){
    curr = glob9;
  }
  float m = (value-curr)/t;
  int ii = 1;
  while(ii<t+1){
    val = m*ii+curr;
    if(val>255){
      val = 255;
    }
    analogWrite(pin,val);
    ii++;
    delay(1);
  }
  if(answer){
    Serial << "-" << ownID << "- rp " << pin << " " << value << " " << t <<"\n";
  }
  if(pin == 3){
    glob3 = val;
  }
  if(pin == 9){
    glob9 = val;
  }
}
