from tkinter import *
import tkinter as tk
from tkinter import messagebox

from PIL import ImageTk


def login_page():
    selection_window.destroy()
    import login


def enroll_page():
    selection_window.destroy()
    import enroll


def delete_page():
    selection_window.destroy()
    import login


selection_window = Tk()
selection_window.attributes("-fullscreen", True)
selection_window.resizable(0, 0)
selection_window.title("selection window")

loginbuttion = Button(
    selection_window,
    text="Engine Start !!!",
    font=("Open Sans", 16, "bold"),
    fg="white",
    bg="firebrick1",
    activeforeground="white",
    activebackground="firebrick1",
    cursor="hand2",
    bd=0,
    width=14,
    command=login_page,
)
loginbuttion.place(relx=0.5, rely=0.30, anchor=tk.CENTER)
loginnote = Label(
    selection_window,
    text="NOTE: engin start button will action a verification process of persons driving licence login button will redirect you to the page where the licence will get verified in the system of vehical.",
    font=("microsoft yahei UI light", 10, "bold"),
    fg="firebrick1",
)
loginnote.place(relx=0.5, rely=0.35, anchor=tk.CENTER)


enrollbuttion = Button(
    selection_window,
    text="New Registration",
    font=("Open Sans", 16, "bold"),
    fg="white",
    bg="firebrick1",
    activeforeground="white",
    activebackground="firebrick1",
    cursor="hand2",
    bd=0,
    width=14,
    command=enroll_page,
)
enrollbuttion.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
enrollnote = Label(
    selection_window,
    text="NOTE: enroll button will redire\ct you to the page where you will enroll your licence in the system of vehical.",
    font=("microsoft yahei UI light", 10, "bold"),
    fg="firebrick1",
)
enrollnote.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
deletelbuttion = Button(
    selection_window,
    text="Delete",
    font=("Open Sans", 16, "bold"),
    fg="white",
    bg="firebrick1",
    activeforeground="white",
    activebackground="firebrick1",
    cursor="hand2",
    bd=0,
    width=14,
    command=delete_page
)
deletelbuttion.place(relx=0.5, rely=0.70, anchor=tk.CENTER)
deletenote = Label(
    selection_window,
    text="NOTE: delete button will redirect you to the page where you can remove your licence details from the vehical.",
    font=("microsoft yahei UI light", 10, "bold"),
    fg="firebrick1",
)
deletenote.place(relx=0.5, rely=0.75, anchor=tk.CENTER)



selection_window.mainloop()
