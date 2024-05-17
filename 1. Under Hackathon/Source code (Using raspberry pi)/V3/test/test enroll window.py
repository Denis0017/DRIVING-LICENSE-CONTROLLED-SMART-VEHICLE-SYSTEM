from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk

def toggle_fullscreen(event):
    start_window.attributes('-fullscreen', not start_window.attributes('-fullscreen'))

def connect_database():
    rfid = SimpleMFRC522()
    id, text = rfid.read()
    
    try:
        con=pymysql.connect(host='localhost',user='root',password='root')
        mycursor=con.cursor()
    except:
        messagebox.showerror('error','database error')
        return
        
    try:
        query='create database testdata'
        mycursor.execute(query)
        query='use testdata'
        mycursor.execute(query)
        query='create table data(id int auto_increment primary key not null, rfid varchar(50))'
        mycursor.execute(query)
    except:
        mycursor.execute('use testdata')


    query='select * from data where rfid =%s'
    mycursor.execute(query,(id))
    row=mycursor.fetchone()
    if row !=None:
        messagebox.showerror('error','rfid alradey used')
    
    else:
        query='insert into data(rfid) values(%s)'
        mycursor.execute(query,(id))
        con.commit()
        con.close()
        messagebox.showinfo('success','registration is successful')
        enroll_window.destroy()
        import login


enroll_window = Tk()
enroll_window.attributes("-fullscreen", True)
enroll_window.resizable(0, 0)
enroll_window.title("start window")

enrollbutton = Button(
    enroll_window,
    text="start process",
    font=("Open Sans", 16, "bold"),
    fg="white",
    bg="firebrick1",
    activeforeground="white",
    activebackground="firebrick1",
    cursor="hand2",
    bd=0,
    width=14,
    
)
enrollbutton.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
enrollnote = Label(
    enroll_window,
    text="NOTE: enroll button will redire\ct you to the page where you will enroll your licence in the system of vehical.",
    font=("microsoft yahei UI light", 10, "bold"),
    fg="firebrick1",
)
enrollnote.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

enroll_window.mainloop()