import tkinter as tk
from tkinter import filedialog, messagebox
import pymysql

def connect_to_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1223',
        database='file_database'
    )

def create_database_and_table():
    connection = connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS file_database;")
        cursor.execute("USE file_database;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                file_data LONGBLOB NOT NULL
            );
        """)
    connection.commit()
    connection.close()

def fetch_file_list():
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT file_name FROM files")
            files = cursor.fetchall()
            return [file[0] for file in files]
    finally:
        connection.close()

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("DAT files", "*.dat")])
    if file_path:
        file_name = file_path.split('/')[-1]
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO files (file_name, file_data) VALUES (%s, %s)"
                cursor.execute(sql, (file_name, binary_data))
            connection.commit()
            messagebox.showinfo("Success", "File uploaded successfully!")
            update_file_list()
        finally:
            connection.close()

def view_files():
    files = fetch_file_list()
    if files:
        messagebox.showinfo("Files in Database", "\n".join(files))
    else:
        messagebox.showinfo("Info", "No files found in the database.")

def download_file():
    file_list = fetch_file_list()
    if file_list:
        file_to_download = filedialog.askstring("Select File", "Enter the filename to download:", initialvalue=file_list[0])
        if file_to_download:
            connection = connect_to_db()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT file_data FROM files WHERE file_name=%s", (file_to_download,))
                    file_data = cursor.fetchone()[0]
                save_path = filedialog.asksaveasfilename(defaultextension=".dat", initialfile=file_to_download)
                if save_path:
                    with open(save_path, 'wb') as file:
                        file.write(file_data)
                    messagebox.showinfo("Success", "File downloaded successfully!")
            finally:
                connection.close()
    else:
        messagebox.showinfo("Info", "No files found in the database.")

def update_file_list():
    file_list = fetch_file_list()
    listbox.delete(0, tk.END)
    for file_name in file_list:
        listbox.insert(tk.END, file_name)

# Initialize the Tkinter application
root = tk.Tk()
root.title("File Upload and Download")

# Create the database and table if not already created
create_database_and_table()

# Create a listbox to display the list of files
listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)

# Update the file list initially
update_file_list()

# Create buttons for the actions
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=10)

view_button = tk.Button(root, text="View Files", command=view_files)
view_button.pack(pady=10)

download_button = tk.Button(root, text="Download File", command=download_file)
download_button.pack(pady=10)

root.mainloop()
