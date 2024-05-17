import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import serial
import adafruit_fingerprint
import pymysql
from tkinter import simpledialog


uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def toggle_fullscreen(event):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def show_message_box(message):
    messagebox.showinfo("Message", message)
    root.after(5000, clear_message)

def clear_message():
    message_label.configure(text="")

def enroll_fingerprint(rfid_data):
    for finger_id in range(128):
        if finger.read_templates() != adafruit_fingerprint.OK:
            show_message_box("Failed to read templates")
            break

        if finger.templates[finger_id] == 0:
            if enroll_finger(finger_id):
                show_message_box("Fingerprint enrolled successfully at position {}".format(finger_id))
                store_data_in_database(finger_id, rfid_data)
            else:
                show_message_box("Failed to enroll fingerprint")
            break

def enroll_finger(location):
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            show_message_box("Place finger on sensor...")
        else:
            show_message_box("Place same finger again...")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                show_message_box("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                show_message_box(".")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                show_message_box("Imaging error")
                return False
            else:
                show_message_box("Other error")
                return False

        show_message_box("Templating...")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            show_message_box("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                show_message_box("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                show_message_box("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                show_message_box("Image invalid")
            else:
                show_message_box("Other error")
            return False

        if fingerimg == 1:
            show_message_box("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    show_message_box("Creating model...")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        show_message_box("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            show_message_box("Prints did not match")
        else:
            show_message_box("Other error")
        return False

    show_message_box("Storing model #%d..." % location)
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        show_message_box("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            show_message_box("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            show_message_box("Flash storage error")
        else:
            show_message_box("Other error")
        return False
    return True

def store_data_in_database(location, rfid_data):
    try:
        con = pymysql.connect(host="localhost", user="root", password="root")
        cursor = con.cursor()
    except:
        messagebox.showerror("error", "database error")
        return
    try:
        query = "create database testdata"
        cursor.execute(query)
        query = "use testdata"
        cursor.execute(query)
        query = "create table data(id int auto_increment primary key not null, location varchar(50), rfid varchar(3))"
        cursor.execute(query)
    except:
        cursor.execute("use testdata")

    try:
        query = "insert into data(location, rfid) VALUES (%s, %s)"
        cursor.execute(query, (location, rfid_data))
        con.commit()
        show_message_box("Fingerprint and RFID data stored in database")
    except pymysql.Error as e:
        show_message_box("Database error: {}".format(e))
    finally:
        if con:
            con.close()

def read_rfid_and_enroll_fingerprint():
    id = rfid_read()
    if id is not None:
        enroll_fingerprint(id)
    else:
        show_message_box("Failed to read RFID")

def get_num():
    i = 0
    while (i > 127) or (i < 1):
        try:
            i = simpledialog.askinteger("Enter ID", "Enter ID # from 1-127:")
        except ValueError:
            pass
    return i

def rfid_read():
    # Your RFID reading code here
    show_message_box("scane the rfid")
    rfid = SimpleMFRC522()
    id, text = rfid.read()
    return id

root = tk.Tk()

root.attributes("-fullscreen", True)
root.bind("<Escape>", toggle_fullscreen)

root.title("Fingerprint and RFID Management")
root.geometry("400x300")

message_label = tk.Label(root, text="", wraplength=300)
message_label.pack(pady=20)

enroll_button = tk.Button(root, text="Enroll Fingerprint and Read RFID", command=read_rfid_and_enroll_fingerprint)
enroll_button.pack()

root.mainloop()
