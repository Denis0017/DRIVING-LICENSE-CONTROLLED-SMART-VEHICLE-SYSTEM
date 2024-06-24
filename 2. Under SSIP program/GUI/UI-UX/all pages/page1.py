import tkinter as tk
from tkinter import ttk
from database import execute_query

class Page1(tk.Frame):
    def __init__(self, parent, controller, bg="white"):
        super().__init__(parent, bg=bg)
        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        label = tk.Label(self, text="This is Page 1", bg=bg)
        label.grid(row=0, column=0, pady=10, padx=10, sticky="n")

        # Create a frame for the table
        table_frame = ttk.Frame(self)
        table_frame.grid(row=2, column=0, pady=10, sticky="nsew")

        self.grid_rowconfigure(2, weight=1)

        # Get column names and data
        column_names = self.get_column_names()

        # Create the Treeview widget
        self.my_table = ttk.Treeview(table_frame, columns=column_names, show='headings')

        # Set column headings
        for col in column_names:
            self.my_table.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
            self.my_table.column(col, width=100)  # Adjust the column width as needed

        # Insert data rows
        self.refresh_table()

        # Pack the Treeview
        self.my_table.pack(fill="both", expand=True)

    def get_column_names(self):
        query = "SELECT * FROM data LIMIT 1"
        _, description = execute_query(query)
        column_names = [desc[0] for desc in description]
        return column_names

    def refresh_table(self):
        # Clear current table
        for item in self.my_table.get_children():
            self.my_table.delete(item)

        # Re-query and insert new data
        query = "SELECT * FROM data"
        rows, _ = execute_query(query)
        for row in rows:
            self.my_table.insert("", "end", values=row)

    def sort_column(self, col, reverse):
        data = [(self.my_table.set(child, col), child) for child in self.my_table.get_children("")]
        data.sort(reverse=reverse)
        for index, item in enumerate(data):
            self.my_table.move(item[1], "", index)
        self.my_table.heading(col, command=lambda: self.sort_column(col, not reverse))


