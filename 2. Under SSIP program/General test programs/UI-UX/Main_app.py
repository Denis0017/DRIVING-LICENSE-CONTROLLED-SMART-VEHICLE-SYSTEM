import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page App")
        self.geometry("800x600")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

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

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="This is Page 1")
        label.pack(pady=10, padx=10)

        button2 = tk.Button(self, text="Go to Page 2", command=lambda: controller.show_page("Page2"))
        button2.pack()

        button3 = tk.Button(self, text="Go to Page 3", command=lambda: controller.show_page("Page3"))
        button3.pack()

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="This is Page 2")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Go to Page 1", command=lambda: controller.show_page("Page1"))
        button1.pack()

        button3 = tk.Button(self, text="Go to Page 3", command=lambda: controller.show_page("Page3"))
        button3.pack()

class Page3(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="This is Page 3")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Go to Page 1", command=lambda: controller.show_page("Page1"))
        button1.pack()

        button2 = tk.Button(self, text="Go to Page 2", command=lambda: controller.show_page("Page2"))
        button2.pack()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
