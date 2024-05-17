from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
#import RPi.GPIO as GPIO
#from mfrc522 import SimpleMFRC522
# import pymysql

# def connect_database():
#     rfid = SimpleMFRC522()
#     id, text = rfid.read()
    
#     try:
#         con=pymysql.connect(host='localhost',user='root',password='root')
#         mycursor=con.cursor()
#     except:
#         messagebox.showerror('error','database error')
#         return
        
#     try:
#         query='create database userdata'
#         mycursor.execute(query)
#         query='use userdata'
#         mycursor.execute(query)
#         query='create table data(id int auto_increment primary key not null, rfid varchar(50))'
#         mycursor.execute(query)
#     except:
#         mycursor.execute('use userdata')


#     query='select * from data where rfid =%s'
#     mycursor.execute(query,(id))
#     row=mycursor.fetchone()
#     if row !=None:
#         messagebox.showerror('error','rfid alradey used')
    
#     else:
#         query='insert into data(rfid) values(%s)'
#         mycursor.execute(query,(id))
#         con.commit()
#         con.close()
#         messagebox.showinfo('success','registration is successful')
#         enroll_window.destroy()
#         import login



def selection_page():
    enroll_window.destroy()
    import selection



enroll_window=Tk()
enroll_window.resizable(0,0)
enroll_window.title('EnrollPage')
bgImage=ImageTk.PhotoImage(file='bg.jpg')

bgLable =Label(enroll_window,image=bgImage)
bgLable.grid(row=0,column=0)

heading=Label(enroll_window,text='ENROLL USER',font=('microsoft yahei UI light',23,'bold'),bg='white',fg='firebrick1')
heading.place(x=605,y=120)


frame1=Frame(enroll_window,width=250,height=2,bg='firebrick1').place(x=580,y=222)


rfidbutton=Button(enroll_window,text='Licence',width=25,font=('microsoft yahei UI light',11,'bold'),bd=0,fg='firebrick1')
rfidbutton.place(x=577,y=237)

frame2=Frame(enroll_window,width=250,height=2,bg='firebrick1').place(x=580,y=282)


backbuttion=Button(enroll_window,text='<Back',font=('Open Sans',9,'bold underline'),fg='blue',bg='white',activeforeground='firebrick1',activebackground='blue',cursor='hand2',bd=0,command=selection_page)
backbuttion.place(x=555,y=100)

enroll_window.mainloop()