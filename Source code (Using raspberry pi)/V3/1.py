import time
import serial
import tkinter as tk
from tkinter import messagebox
import adafruit_fingerprint

uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def enroll_finger(location):
    for fingerimg in range(1, 3):
        print("Place finger on sensor...", end="")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True

def get_num(existing_templates):
    i = 0
    while (i > 127) or (i < 1) or (i in existing_templates):
        try:
            i = int(input("Enter ID # from 1-127: "))
            if i in existing_templates:
                print("Error: Number already exists. Please enter a different number.")
        except ValueError:
            pass
    return i

def enroll_print():
    existing_templates = []

    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    existing_templates = finger.templates

    def enroll():
        id_num = int(id_entry.get())

        if id_num < 1 or id_num > 127:
            messagebox.showerror("Error", "ID number must be between 1 and 127")
            return

        if id_num in existing_templates:
            messagebox.showerror("Error", "ID number already exists")
            return

        result = enroll_finger(id_num)
        if result:
            messagebox.showinfo("Success", "Fingerprint enrollment successful")
        else:
            messagebox.showerror("Error", "Fingerprint enrollment failed")

    window = tk.Tk()
    window.title("Fingerprint Enrollment")

    label = tk.Label(window, text="Fingerprint Enrollment")
    label.pack()

    id_label = tk.Label(window, text="Enter ID # from 1-127:")
    id_label.pack()

    id_entry = tk.Entry(window)
    id_entry.pack()

    enroll_button = tk.Button(window, text="Enroll", command=enroll)
    enroll_button.pack()

    window.mainloop()

enroll_print()
