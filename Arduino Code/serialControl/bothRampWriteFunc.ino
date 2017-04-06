/*******************************************************************************

    This file was written to be used with SerialControl.

    SerialControl is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

*******************************************************************************/

void bothRampWriteFunc(){
  float valueL = parseArgument(AR1);
  float valueR =  parseArgument(AR2);
  int t = parseArgument(AR3);
  float valL = 0;
  float valR = 0;
  int currL = glob3;
  int currR = glob9;
  if(valueL>255){
    valueL=currL;
  }
  if(valueR>255){
    valueR=currR;
  }
  float mL = (valueL-currL)/t;
  float mR = (valueR-currR)/t;
  int ii = 1;
  while(ii<t+1){
      valL = mL*ii+currL;
      valR = mR*ii+currR;
    if(valL>255){
      valL = 255;
    }
    if(valR>255){
      valR = 255;
    }
    if(valL != glob3){
      analogWrite(3,valL);
    }
    if(valR != glob9){
      analogWrite(9,valR);
    }
    
    Serial << valL << " " << valR << "\n";
    ii++;
    delay(1);
  }
  if(answer){
    Serial << "-" << ownID << "- br " << valL << " " << valR << " " << t <<"\n";
  }
    glob3 = valL;
    glob9 = valR;
}
