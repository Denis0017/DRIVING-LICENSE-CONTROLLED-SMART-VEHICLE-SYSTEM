import tkinter as tk
from tkinter import messagebox
from mfrc522 import SimpleMFRC522
import pymysql
import serial
import adafruit_fingerprint


connection = pymysql.connect(host="localhost",user="root",password="root",database="testdata")
cursor = connection.cursor()

uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def toggle_fullscreen(event):
    window.attributes("-fullscreen", not window.attributes("-fullscreen"))

def show_message_box(message):
    messagebox.showinfo("Message", message)

def get_fingerprint():
    show_message_box("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    show_message_box("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    show_message_box("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

def find_fingerprint():
    if get_fingerprint():
        message = "Fingerprint detected!\nID: {}\nConfidence: {}".format(finger.finger_id, finger.confidence)
        show_message_box(message)
    else:
        show_message_box("Fingerprint not found.")

def rfid_read():
    show_message_box("scane the rfid")
    rfid = SimpleMFRC522()
    id, text = rfid.read()
    return id

def verify_details():
    id = rfid_read()
    if id is not None:
        find_fingerprint()
        query = "SELECT name, location FROM data WHERE rfid = %s AND location = %s"
        cursor.execute(query, (id,finger.finger_id))
        result = cursor.fetchone()

        if result:
            name_label.config(text="license is verified successfully and person's Name:" + result[0])
        else:
            name_label.config(text="RFID and Fingerprint are mismatched or not enrolled in the system")

window = tk.Tk()

window.attributes("-fullscreen", True)
window.bind("<Escape>", toggle_fullscreen)

window.title("Fingerprint and RFID Management")
window.geometry("400x300")

verify_details_button = tk.Button(window, text="verify DetailV", command=verify_details)
verify_details_button.pack(pady=20)

name_label =  tk.Label(window, text="")
name_label.pack(pady=20)

window.mainloop()
