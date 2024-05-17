from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

import serial
import adafruit_fingerprint

uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)


def toggle_fullscreen(event):
    enroll_window.attributes("-fullscreen", not enroll_window.attributes("-fullscreen"))


def show_message_box(message):
    messagebox.showinfo("Message", message)
    enroll_window.after(5000, clear_message)

def clear_message():
    message_label.configure(text="")


def enroll_fingerprint():
    for finger_id in range(128):
        if finger.read_templates() != adafruit_fingerprint.OK:
            show_message_box("Failed to read templates")
            break

        if finger.templates[finger_id] == 0:
            if enroll_finger(finger_id):
                show_message_box("Fingerprint enrolled successfully at position {}".format(finger_id))
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


def get_num():
    i = 0
    while (i > 127) or (i < 1):
        try:
            i = simpledialog.askinteger("Enter ID", "Enter ID # from 1-127:")
        except ValueError:
            pass
    return i

def connect_database():
    rfid = SimpleMFRC522()
    id, text = rfid.read()

    try:
        con = pymysql.connect(host="localhost", user="root", password="root")
        mycursor = con.cursor()
    except:
        messagebox.showerror("error", "database error")
        return

    try:
        query = "create database testdata"
        mycursor.execute(query)
        query = "use testdata"
        mycursor.execute(query)
        query = "create table data(id int auto_increment primary key not null, rfid varchar(50), finger varchar(3))"
        mycursor.execute(query)
    except:
        mycursor.execute("use testdata")

    query = "select * from data where rfid =%s"
    mycursor.execute(query, (id))
    row = mycursor.fetchone()
    if row != None:
        messagebox.showerror("error", "rfid alradey used")
    else:
        query = "insert into data(rfid) values(%s) data(finger) values(%d)"
        mycursor.execute(query, (id))
        con.commit()
        con.close()
        messagebox.showinfo("success", "registration is successful")
        enroll_window.destroy()
        # import login


enroll_window = Tk()
enroll_window.attributes("-fullscreen", True)
enroll_window.bind("<Escape>", toggle_fullscreen)
enroll_window.title("start window")

message_label = tk.Label(enroll_window, text="", wraplength=300)
message_label.pack(pady=20)

rfidbutton = Button(
    enroll_window,
    text="ENROLL RFID",
    font=("Open Sans", 16, "bold"),
    fg="white",
    bg="firebrick1",
    activeforeground="white",
    activebackground="firebrick1",
    cursor="hand2",
    bd=0,
    width=14,
)
rfidbutton.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
rfidnote = Label(
    enroll_window,
    text="NOTE: enroll RFID button will register your rfid in to system of vehical.",
    font=("microsoft yahei UI light", 10, "bold"),
    fg="firebrick1",
)
rfidnote.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

fingerbutton = Button(
    enroll_window,
    text="ENROLL FINGERPRINT",
    font=("Open Sans", 16, "bold"),
    fg="white",
    bg="firebrick1",
    activeforeground="white",
    activebackground="firebrick1",
    cursor="hand2",
    bd=0,
    width=14,
)
fingerbutton.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
fingernote = Label(
    enroll_window,
    text="NOTE: enroll FINGERPRINT button will register your fingerprint in to system of vehical.",
    font=("microsoft yahei UI light", 10, "bold"),
    fg="firebrick1",
)
fingernote.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

enrollbutton = Button(
    enroll_window,
    text="Finish process",
    font=("Open Sans", 16, "bold"),
    fg="white",
    bg="firebrick1",
    activeforeground="white",
    activebackground="firebrick1",
    cursor="hand2",
    bd=0,
    width=14,
)
enrollbutton.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
# enrollnote = Label(
#     enroll_window,
#     text="NOTE: enroll button will redire\ct you to the page where you will enroll your licence in the system of vehical.",
#     font=("microsoft yahei UI light", 10, "bold"),
#     fg="firebrick1",
# )
# enrollnote.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

enroll_window.mainloop()
