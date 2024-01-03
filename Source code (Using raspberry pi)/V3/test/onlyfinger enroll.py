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

def enroll_fingerprint():
    finger_id = get_num()
    if finger_id is None:
        return

    if finger.read_templates() != adafruit_fingerprint.OK:
        show_message_box("Failed to read templates")
        return

    if finger.templates[finger_id] != 0:
        show_message_box("Fingerprint already enrolled at position {}".format(finger_id))
        return

    if enroll_finger(finger_id):
        show_message_box("Fingerprint enrolled successfully at position {}".format(finger_id))
    else:
        show_message_box("Failed to enroll fingerprint")

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

def get_num():
    i = None
    while (i is None) or (i > 127) or (i < 0):
        try:
            i = simpledialog.askinteger("Enter ID", "Enter ID # from 0-127:")
        except ValueError:
            pass
    return i


root = tk.Tk()

root.attributes("-fullscreen", True)
root.bind("<Escape>", toggle_fullscreen)

root.title("Fingerprint Management")
root.geometry("400x300")

message_label = tk.Label(root, text="", wraplength=300)
message_label.pack(pady=20)

enroll_button = tk.Button(root, text="Enroll Fingerprint", command=enroll_fingerprint)
enroll_button.pack()

root.mainloop()
