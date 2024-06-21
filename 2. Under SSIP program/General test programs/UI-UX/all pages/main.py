import tkinter as tk
from page1 import Page1
from page2 import Page2
from page3 import Page3

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page App")
        self.attributes('-fullscreen', True)  # Make the application full screen
        self.resizable(False, False)  # Disable resizing

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}

        for PageClass in (Page1, Page2, Page3):
            page_name = PageClass.__name__
            page = PageClass(parent=self.container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("Page1")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()
        
        # Enable all buttons first
        for p_name, p in self.pages.items():
            p.enable_buttons()
        
        # Disable the button for the current page
        page.disable_current_page_button()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
