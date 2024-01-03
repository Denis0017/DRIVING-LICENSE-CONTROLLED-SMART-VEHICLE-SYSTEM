import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

rfid = SimpleMFRC522()


#while True:
id, text = rfid.read()
#print(id)
#print(text)
if (id == 1043551885721):
    print("Denis")
elif (id == 207087804482):
    print("Dev")
elif (id == 830558643363):
    print("Tirth")
else :
    print("Unknown user")
           

      
               
