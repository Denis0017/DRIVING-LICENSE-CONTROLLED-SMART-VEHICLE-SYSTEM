from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk


# def rfid_read():
#         rfid = SimpleMFRC522()
#         id, text = rfid.read()
#         "messagebox.showinfo('id',id)"
#         try:
#             con=pymysql.connect(host='localhost',user='start_window',password='start_window')
#             mycursor=con.cursor()
#         except:
#             messagebox.showerror('error','database error')
#             return
#         query='use userdata'
#         mycursor.execute(query)
#         query='select * from data where rfid =%s '
#         mycursor.execute(query,(id))
#         row=mycursor.fetchone()
#         if row == None:
#             messagebox.showerror('erorr','invalid licence')
#         else:
#             messagebox.showinfo('welcome','login sucessful=%s')


start_window = Tk()
def toggle_fullscreen(event):
    start_window.attributes('-fullscreen', not start_window.attributes('-fullscreen'))

start_window.attributes('-fullscreen', True)
start_window.bind('<Escape>', toggle_fullscreen)
start_window.title("start window")

startbutton = Button(
    start_window,
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
startbutton.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
startnote = Label(
    start_window,
    text="NOTE: engin start button will action a verification process of persons driving licence login button will redirect you to the page where the licence will get verified in the system of vehical.",
    font=("microsoft yahei UI light", 10, "bold"),
    fg="firebrick1",
)
startnote.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

start_window.mainloop()