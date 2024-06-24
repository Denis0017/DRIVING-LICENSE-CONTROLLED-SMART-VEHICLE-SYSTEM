import tkinter as tk
from database import execute_query

class Page3(tk.Frame):
    def __init__(self, parent, controller, bg="white"):
        super().__init__(parent, bg=bg)
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = tk.Label(self, text="This is Page 3", bg=bg)
        label.grid(row=0, column=0, pady=10, padx=10, sticky="n")