import tkinter as tk
from database import execute_query

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = tk.Label(self, text="This is Page 2")
        label.grid(row=0, column=0, pady=10, padx=10, sticky="n")

        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")

        self.button1 = tk.Button(button_frame, text="Go to Page 1", command=lambda: controller.show_page("Page1"))
        self.button1.pack(side="left", padx=5)

        self.button2 = tk.Button(button_frame, text="Page 2", state="disabled")
        self.button2.pack(side="left", padx=5)

        self.button3 = tk.Button(button_frame, text="Go to Page 3", command=lambda: controller.show_page("Page3"))
        self.button3.pack(side="left", padx=5)

    def enable_buttons(self):
        self.button1.config(state="normal")
        self.button2.config(state="normal")
        self.button3.config(state="normal")

    def disable_current_page_button(self):
        self.button2.config(state="disabled")
