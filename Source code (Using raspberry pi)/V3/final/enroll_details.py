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

def clear():
    enroll_name.delete(0,END)

def toggle_fullscreen(event):
    enroll_details.attributes("-fullscreen", not enroll_details.attributes("-fullscreen"))

def show_message_box(message):
    messagebox.showinfo("Message", message)
    enroll_details.after(1000, clear_message)

def clear_message():
    message_label.configure(text="")

def get_num(existing_templates):
    i=0
    while (i > 127) or (i < 1) or (i in existing_templates):
        try:
            i = int(simpledialog.askstring("Fingerprint", "Enter ID # from 1-127: "))
            if i in existing_templates:
                messagebox.showerror("Fingerprint", "The entered location id is already occupied, Please enter another location id.")
        except ValueError:
            pass
    return i

def enroll_finger(location):
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            messagebox.showinfo("Fingerprint", "Place finger on sensor...")
        else:
            messagebox.showinfo("Fingerprint", "Place same finger again...")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                break
            if i == adafruit_fingerprint.NOFINGER:
                pass
            elif i == adafruit_fingerprint.IMAGEFAIL:
                messagebox.showinfo("Fingerprint", "Imaging error")
                return False
            else:
                messagebox.showinfo("Fingerprint", "Other error")
                return False

        messagebox.showinfo("Fingerprint", "Templating...")

        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            pass
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                messagebox.showinfo("Fingerprint", "Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                messagebox.showinfo("Fingerprint", "Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                messagebox.showinfo("Fingerprint", "Image invalid")
            else:
                messagebox.showinfo("Fingerprint", "Other error")
            return False

        if fingerimg == 1:
            messagebox.showinfo("Fingerprint", "Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    messagebox.showinfo("Fingerprint", "Creating model...")

    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        pass
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            messagebox.showinfo("Fingerprint", "Prints did not match")
        else:
            messagebox.showinfo("Fingerprint", "Other error")
        return False

    messagebox.showinfo("Fingerprint", f"Storing model #{location}...")

    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        pass
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            messagebox.showinfo("Fingerprint", "Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            messagebox.showinfo("Fingerprint", "Flash storage error")
        else:
            messagebox.showinfo("Fingerprint", "Other error")
        return False

    return True

def store_data_in_database(location, id):
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
        query = "create table data(id int auto_increment primary key not null, Name varchar(50), location varchar(50), rfid varchar(50))"
        cursor.execute(query)
    except:
        cursor.execute("use testdata")

    query='select * from data where rfid =%s'
    cursor.execute(query,(id))
    row=cursor.fetchone()
    query='select * from data where location =%s'
    cursor.execute(query,(location))
    row=cursor.fetchone()
    if row !=None:
        messagebox.showerror('error','rfid or fingerprint location alradey used')
    elif row !=None:
        messagebox.showerror('error','rfid or fingerprint location alradey used')
    else:
        try:
            query = "insert into data(Name, location, rfid) VALUES (%s, %s, %s)"
            cursor.execute(query,(enroll_name.get(), location, id))
            con.commit()
            show_message_box("Fingerprint and RFID data stored in database")
        except pymysql.Error as e:
            show_message_box("Database error: {}".format(e))
        finally:
            if con:
                con.close()
    clear()
    enroll_details.destroy()
    import verfiy_details

def rfid_read():
    # Your RFID reading code here
    show_message_box("scane the rfid")
    rfid = SimpleMFRC522()
    id, text = rfid.read()
    return id

def read_rfid_and_enroll_fingerprint():
    if enroll_name.get()=='':
        messagebox.showerror("error", "Name is requied")
    else:
        id = rfid_read()
        if id is not None:
            if finger.read_templates() != adafruit_fingerprint.OK:
                raise RuntimeError("Failed to read templates")
            existing_templates = finger.templates
            location = get_num(existing_templates)
            enroll_finger(location)
            store_data_in_database(location,id)
        else:
            show_message_box("Failed to read RFID")

enroll_details = tk.Tk()

enroll_details.attributes("-fullscreen", True)
enroll_details.bind("<Escape>", toggle_fullscreen)

enroll_details.title("Fingerprint and RFID Management")
enroll_details.geometry("400x300")

message_label = tk.Label(enroll_details, text="", wraplength=300)
message_label.pack(pady=20)

enroll_namelable = Label(enroll_details, text='Enter Your Name Here:')
enroll_namelable.pack(pady=20)

enroll_name = Entry(enroll_details,width=25)
enroll_name.pack(pady=20)

enroll_button = tk.Button(enroll_details, text="Enroll Fingerprint and Read RFID", command=read_rfid_and_enroll_fingerprint)
enroll_button.pack()

enroll_details.mainloop()
