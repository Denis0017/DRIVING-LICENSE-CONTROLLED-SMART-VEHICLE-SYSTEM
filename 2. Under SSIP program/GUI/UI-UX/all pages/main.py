import tkinter as tk
from tkinter import messagebox
from page1 import Page1
from page2 import Page2
from page3 import Page3

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page App")
        self.attributes('-fullscreen', True)  # Make the application full screen
        self.resizable(False, False)  # Disable resizing

        self.container = tk.Frame(self, bg = "white")
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create navigation bar
        self.nav_bar = tk.Frame(self, bg="lightgray", height=50)
        self.nav_bar.pack(fill="x")

        # Define navigation buttons with custom background colors
        pages = [("Page 1", Page1), ("Page 2", Page2), ("Page 3", Page3)]
        self.pages = {}

        for text, PageClass in pages:
            button = tk.Button(self.nav_bar, text=text, command=lambda pc=PageClass: self.show_page(pc), relief=tk.FLAT, bg="lightblue", fg="black")
            button.pack(side="left", padx=10, pady=10)

            page_name = PageClass.__name__
            page = PageClass(parent=self.container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Close button with red background
        close_button = tk.Button(self, text="X", bg="red", fg="white", font=("Arial", 12, "bold"), command=self.on_closing, relief=tk.FLAT)
        close_button.place(x=self.winfo_screenwidth()-40, y=0, width=40, height=40)

        self.show_page(Page1)

    def show_page(self, PageClass):
        page_name = PageClass.__name__
        page = self.pages[page_name]
        page.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
