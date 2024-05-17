//__________________________________FINGERPRINT_____________________________________

#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>
SoftwareSerial mySerial(2, 3);

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);
int fingerprintID = 0;
String IDname;

//__________________________________RFID_____________________________________
int count = 0;
char c;
String id;

//__________________________________L293D_____________________________________
int in1 = 4;
int in2 = 5;

//__________________________________setup_____________________________________
void setup(){

  Serial.begin(9600);
  Serial.println("Please scan your RFID TAG");
  finger.begin(57600);
  
  if (finger.verifyPassword()) { 
    Serial.println("Found fingerprint sensor!");
  } 
  else {
    Serial.println("Did not find fingerprint sensor :(");
    while (1) { delay(1); }
  }


}

//__________________________________loop_____________________________________
void loop(){
  Serial.println("Please scan your RFID TAG");
  fingerprintID = getFingerprintIDez();
  delay(50);

//__________________________________RFID_____________________________________

  while(Serial.available()>0)
  {
    c = Serial.read();
   count++;
   id += c;
   if(count == 12)  
    {
      Serial.print(id);
      //break;
     
      if(id=="AB123456789A")
      {
        Serial.println("Valid TAG");

//__________________________________FINGERPRINT_____________________________________
        if(fingerprintID == 1 || fingerprintID == 3 || fingerprintID == 4 || fingerprintID == 5){
            IDname = "Sara";
            Serial.print(IDname);            
            digitalWrite(in1,HIGH);
            digitalWrite(in2,LOW);
            while(1);
          }  
          else if(fingerprintID == 2){
            IDname = "Rui";  
            Serial.print(IDname);
            digitalWrite(in1,HIGH);
            digitalWrite(in2,LOW);            
            while(1);            
          }
//exit
      }
      else if(id=="AB123456789D")
      {
        Serial.println("Valid TAG");

//__________________________________FINGERPRINT_____________________________________
        if(fingerprintID == 1 || fingerprintID == 3 || fingerprintID == 4 || fingerprintID == 5){
            IDname = "Sara";
            Serial.print(IDname);
            digitalWrite(in1,HIGH);
            digitalWrite(in2,LOW);            
            while(1);
          }  
          else if(fingerprintID == 2){
            IDname = "Rui";  
            Serial.print(IDname);
            digitalWrite(in1,HIGH);
            digitalWrite(in2,LOW);            
            while(1);            
          }
//exit
      else
      {
      
      Serial.println("Invalid TAG");
      }
    }
  }
  count = 0;
  id="";
  delay(500);

}
}

// returns -1 if failed, otherwise returns ID #
int getFingerprintIDez() {
  uint8_t p = finger.getImage();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.image2Tz();
  if (p != FINGERPRINT_OK)  return -1;

  p = finger.fingerFastSearch();
  if (p != FINGERPRINT_OK)  return -1;
  
  // found a match!
  Serial.print("Found ID #"); 
  Serial.print(finger.fingerID); 
  Serial.print(" with confidence of "); 
  Serial.println(finger.confidence);
  return finger.fingerID; 
}
