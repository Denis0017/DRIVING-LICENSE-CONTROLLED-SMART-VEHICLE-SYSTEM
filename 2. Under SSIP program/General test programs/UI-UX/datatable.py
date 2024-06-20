import tkinter as tk
from tkinter import ttk
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

# Create the main window
window = tk.Tk()
window.title("Sortable Table")

# Create a frame for the table
table_frame = ttk.Frame(window)
table_frame.pack()

# Create the Treeview widget
my_table = ttk.Treeview(table_frame, columns=column_names, show='headings')

# Set column headings
for col in column_names:
    my_table.heading(col, text=col, command=lambda c=col: sort_column(my_table, c))
    my_table.column(col, width=100)  # Adjust the column width as needed

# Insert data rows
for row in cursor.fetchall():
    my_table.insert("", "end", values=row)

# Function to sort columns
def sort_column(tree, col, reverse=False):
    data = [(tree.set(child, col), child) for child in tree.get_children("")]
    data.sort(reverse=reverse)
    for index, item in enumerate(data):
        tree.move(item[1], "", index)
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

# Pack the Treeview
my_table.pack()

# Run the Tkinter application
window.mainloop()
