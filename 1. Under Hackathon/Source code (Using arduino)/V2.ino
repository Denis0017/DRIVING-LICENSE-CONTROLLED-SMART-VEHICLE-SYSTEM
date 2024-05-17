#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <LiquidCrystal_I2C.h>

#define SS_PIN 10  
#define RST_PIN 9  
String scanTagID = "";
MFRC522 mfrc522(SS_PIN, RST_PIN);
LiquidCrystal_I2C lcd(0x27, 16, 2);

#include <Adafruit_Fingerprint.h>
#if (defined(__AVR__) || defined(ESP8266)) && !defined(__AVR_ATmega2560__)
SoftwareSerial mySerial(2, 3);
#else
#define mySerial Serial1
#endif
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);


void setup() 
{
  lcd.init();
  lcd.init();
  lcd.backlight();

  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  delay(2000);

  finger.begin(57600);
  delay(5);
  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
  } else {
    lcd.print("finger scn1 eror");
    Serial.println("Did not find fingerprint sensor :(");
    while (1) { delay(1); }
  }

  finger.getTemplateCount();

  if (finger.templateCount == 0) {
    lcd.clear();
    lcd.print("finger scn2 eror");
    Serial.print("Sensor doesn't contain any fingerprint data. Please run the 'enroll' example.");
  }
  else {
    Serial.println("Waiting for valid finger...");
      Serial.print("Sensor contains "); Serial.print(finger.templateCount); Serial.println(" templates");
  }



    
}

void loop()
{
  lcd.clear();
  lcd.print("put tag");
  Serial.println("tag");
  while (readTagID())
  {
    Serial.println("tag");
    if (scanTagID == "F2F88A19" ) 
    {
      lcd.clear();
      lcd.print("put finger");
      Serial.println("finger");
      while (getFingerprintID())
      {
        Serial.print("finger detected.");
      }
    }
    if (scanTagID == "C1612724" ) 
    {
      lcd.clear();
      lcd.print("put finger");
      Serial.println("finger");
      while (getFingerprintID2())
      {
        Serial.print("finger detected.");
      }
    }
    if (scanTagID == "30376520" ) 
    {
      lcd.clear();
      lcd.print("put finger");
      Serial.println("finger");
      while (getFingerprintID3())
      {
        Serial.print("finger detected.");
      }
    }
    else
    {
      Serial.print("Access Denied  ");
    }
  }
}




boolean readTagID() 
{
  if ( ! mfrc522.PICC_IsNewCardPresent())
  {
    return false;
  }
  if ( ! mfrc522.PICC_ReadCardSerial())
  {
    return false;
  }
  /* Clear the string */
  scanTagID = "";
  for ( uint8_t i = 0; i < 4; i++) 
  {
    scanTagID += String(mfrc522.uid.uidByte[i], HEX);
  }
  scanTagID.toUpperCase();
  mfrc522.PICC_HaltA();
  return true;
}

uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.println("No finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK success!

  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    Serial.println("Found a print match!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    lcd.clear();
    lcd.print("try again");
    Serial.println("Did not find a match");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }

  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID);
  Serial.print(" with confidence of "); Serial.println(finger.confidence);
  if (finger.fingerID == 11 || finger.fingerID == 12 || finger.fingerID == 13 || finger.fingerID == 14)
  {
    lcd.clear();
    lcd.print("engin start...");
    Serial.print("engin start...");
    while(1);
  }
  else{
    lcd.clear();
    lcd.print("try again");
    delay(2000);
  }
  return finger.fingerID;
}

uint8_t getFingerprintID2() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.println("No finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK success!

  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    Serial.println("Found a print match!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    lcd.clear();
    lcd.print("try again");
    Serial.println("Did not find a match");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }

  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID);
  Serial.print(" with confidence of "); Serial.println(finger.confidence);
  if (finger.fingerID == 21 || finger.fingerID == 22 || finger.fingerID == 23 || finger.fingerID == 24)
  {
    lcd.clear();
    lcd.print("engin start...");
    Serial.print("engin start...");
    while(1);
  }
  else{
    lcd.clear();
    lcd.print("try again");
    delay(2000);
  }
  return finger.fingerID;
}

uint8_t getFingerprintID3() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      break;
    case FINGERPRINT_NOFINGER:
      Serial.println("No finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK success!

  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  p = finger.fingerSearch();
  if (p == FINGERPRINT_OK) {
    Serial.println("Found a print match!");
  } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  } else if (p == FINGERPRINT_NOTFOUND) {
    lcd.clear();
    lcd.print("try again");
    Serial.println("Did not find a match");
    return p;
  } else {
    Serial.println("Unknown error");
    return p;
  }

  // found a match!
  Serial.print("Found ID #"); Serial.print(finger.fingerID);
  Serial.print(" with confidence of "); Serial.println(finger.confidence);
  if (finger.fingerID == 31 || finger.fingerID == 32 || finger.fingerID == 33 || finger.fingerID == 34)
  {
    lcd.clear();
    lcd.print("engin start...");
    Serial.print("engin start...");
    while(1);
  }
  else{
    lcd.clear();
    lcd.print("try again");
    delay(2000);
  }
  return finger.fingerID;
}
