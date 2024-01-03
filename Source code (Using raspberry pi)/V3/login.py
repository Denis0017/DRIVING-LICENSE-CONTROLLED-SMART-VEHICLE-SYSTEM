from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
#import RPi.GPIO as GPIO
#from mfrc522 import SimpleMFRC522
# import pymysql

def rfid_read():
    rfid = SimpleMFRC522()
    id, text = rfid.read()
    "messagebox.showinfo('id',id)"
    try:
        con=pymysql.connect(host='localhost',user='root',password='root')
        mycursor=con.cursor()
    except:
        messagebox.showerror('error','database error')
        return
    query='use userdata'
    mycursor.execute(query)
    query='select * from data where rfid =%s '
    mycursor.execute(query,(id))
    row=mycursor.fetchone()
     if row ==None:
        messagebox.showerror('erorr','invalid licence')
    else:
        messagebox.showinfo('welcome','login sucessful=%s')


def selection_page():
    login_window.destroy()
    import selection




login_window=Tk()
login_window.resizable(0,0)
login_window.title('LoginPage')
bgImage=ImageTk.PhotoImage(file='bg.jpg')

bgLable =Label(login_window,image=bgImage)
bgLable.grid(row=0,column=0)

heading=Label(login_window,text='USER LOGIN',font=('microsoft yahei UI light',23,'bold'),bg='white',fg='firebrick1')
heading.place(x=605,y=120)

frame1=Frame(login_window,width=250,height=2,bg='firebrick1').place(x=580,y=222)


rfidbutton=Button(login_window,text='Licence',width=25,font=('microsoft yahei UI light',11,'bold'),bd=0,fg='firebrick1')
rfidbutton.place(x=577,y=237)

frame2=Frame(login_window,width=250,height=2,bg='firebrick1').place(x=580,y=282)

 
backbuttion=Button(login_window,text='<Back',font=('Open Sans',9,'bold underline'),fg='blue',bg='white',activeforeground='firebrick1',activebackground='blue',cursor='hand2',bd=0, command=selection_page)
backbuttion.place(x=555,y=100)


login_window.mainloop()