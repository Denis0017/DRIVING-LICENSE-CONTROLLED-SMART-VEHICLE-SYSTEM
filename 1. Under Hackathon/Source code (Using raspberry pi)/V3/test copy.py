from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pymysql


def rfid_read():
    rfid = SimpleMFRC522()
    id, text = rfid.read()
    messagebox.showinfo('id',id)


enroll_window=Tk()
enroll_window.resizable(0,0)
enroll_window.title('EnrollPage')
bgImage=ImageTk.PhotoImage(file='bg.jpg')

bgLable =Label(enroll_window,image=bgImage)
bgLable.grid(row=0,column=0)

heading=Label(enroll_window,text='ENROLL USER',font=('microsoft yahei UI light',23,'bold'),bg='white',fg='firebrick1')
heading.place(x=605,y=120)

rfidbutton=Button(enroll_window,text='Licence',width=25,font=('microsoft yahei UI light',11,'bold'),bd=0,fg='firebrick1', command=rfid_read)
rfidbutton.place(x=580,y=200)

frame1=Frame(enroll_window,width=250,height=2,bg='firebrick1')
frame1.place(x=580,y=222)

frame2=Frame(enroll_window,width=250,height=2,bg='firebrick1').place(x=580,y=282)

enrollbuttion=Button(enroll_window,text='Enroll New Licence',font=('Open Sans',16,'bold'),fg='white',bg='firebrick1',activeforeground='white',activebackground='firebrick1',cursor='hand2',bd=0,width=19)
enrollbuttion.place(x=578,y=350)

enroll_window.mainloop()