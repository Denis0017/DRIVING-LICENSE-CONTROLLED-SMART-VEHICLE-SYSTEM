import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

# Connect to the database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1223',
    database='userdata'
)

# Execute your SQL query
with conn.cursor() as cursor:
    your_query = "SELECT * FROM data"
    cursor.execute(your_query)

    # Get the column names
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

# Function to sort columns
def sort_column(tree, col, reverse=False):
    data = [(tree.set(child, col), child) for child in tree.get_children("")]
    data.sort(reverse=reverse)
    for index, item in enumerate(data):
        tree.move(item[1], "", index)
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page App")
        self.geometry("800x600")

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

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        label = tk.Label(self, text="This is Page 1")
        label.grid(row=0, column=0, pady=10, padx=10, sticky="n")

        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")

        self.button1 = tk.Button(button_frame, text="Page 1", state="disabled")
        self.button1.pack(side="left", padx=5)

        self.button2 = tk.Button(button_frame, text="Go to Page 2", command=lambda: controller.show_page("Page2"))
        self.button2.pack(side="left", padx=5)

        self.button3 = tk.Button(button_frame, text="Go to Page 3", command=lambda: controller.show_page("Page3"))
        self.button3.pack(side="left", padx=5)
        
        # Button for data modification
        self.modify_button = tk.Button(button_frame, text="Modify Data", command=self.modify_data)
        self.modify_button.pack(side="left", padx=5)
        
        # Button for data deletion
        self.delete_button = tk.Button(button_frame, text="Delete Data", command=self.delete_data)
        self.delete_button.pack(side="left", padx=5)
        
        # Create a frame for the table
        table_frame = ttk.Frame(self)
        table_frame.grid(row=2, column=0, pady=10, sticky="nsew")

        self.grid_rowconfigure(2, weight=1)

        # Create the Treeview widget
        self.my_table = ttk.Treeview(table_frame, columns=column_names, show='headings')

        # Set column headings
        for col in column_names:
            self.my_table.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.my_table.column(col, width=100)  # Adjust the column width as needed

        # Insert data rows
        for row in rows:
            self.my_table.insert("", "end", values=row)

        # Pack the Treeview
        self.my_table.pack(fill="both", expand=True)

    def enable_buttons(self):
        self.button1.config(state="normal")
        self.button2.config(state="normal")
        self.button3.config(state="normal")
        self.modify_button.config(state="normal")
        self.delete_button.config(state="normal")

    def disable_current_page_button(self):
        self.button1.config(state="disabled")
        
    def sort_column(self, col):
        data = [(self.my_table.set(child, col), child) for child in self.my_table.get_children("")]
        data.sort()
        for index, item in enumerate(data):
            self.my_table.move(item[1], "", index)
        self.my_table.heading(col, command=lambda: self.sort_column(col))

    def modify_data(self):
        selected_item = self.my_table.focus()
        if selected_item:
            values = self.my_table.item(selected_item, 'values')
            # Implement your modification logic here
            print(f"Modify data: {values}")
        else:
            messagebox.showwarning("No Selection", "Please select a record to modify.")

    def delete_data(self):
        selected_item = self.my_table.focus()
        if selected_item:
            values = self.my_table.item(selected_item, 'values')
            # Implement your deletion logic here
            print(f"Delete data: {values}")
            # Example: You can delete based on an identifier like an ID
            record_id = values[0]  # Assuming ID is the first column
            # Example SQL query to delete
            with conn.cursor() as cursor:
                try:
                    cursor.execute("DELETE FROM data WHERE id = %s", (record_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Record deleted successfully.")
                    # Refresh the table after deletion (optional)
                    self.refresh_table()
                except pymysql.MySQLError as e:
                    messagebox.showerror("Error", f"Failed to delete record: {e}")
        else:
            messagebox.showwarning("No Selection", "Please select a record to delete.")

    def refresh_table(self):
        # Clear current table
        for item in self.my_table.get_children():
            self.my_table.delete(item)
        
        # Re-query and insert new data
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM data")
            rows = cursor.fetchall()
            for row in rows:
                self.my_table.insert("", "end", values=row)


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

class Page3(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = tk.Label(self, text="This is Page 3")
        label.grid(row=0, column=0, pady=10, padx=10, sticky="n")

        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")

        self.button1 = tk.Button(button_frame, text="Go to Page 1", command=lambda: controller.show_page("Page1"))
        self.button1.pack(side="left", padx=5)

        self.button2 = tk.Button(button_frame, text="Go to Page 2", command=lambda: controller.show_page("Page2"))
        self.button2.pack(side="left", padx=5)

        self.button3 = tk.Button(button_frame, text="Page 3", state="disabled")
        self.button3.pack(side="left", padx=5)

    def enable_buttons(self):
        self.button1.config(state="normal")
        self.button2.config(state="normal")
        self.button3.config(state="normal")

    def disable_current_page_button(self):
        self.button3.config(state="disabled")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
