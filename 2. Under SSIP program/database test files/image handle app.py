import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pymysql
import io

def connect_to_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1223',
        database='image_database'
    )

def create_database_and_table():
    connection = connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS image_database;")
        cursor.execute("USE image_database;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_name VARCHAR(255) NOT NULL,
                image_data LONGBLOB NOT NULL
            );
        """)
    connection.commit()
    connection.close()

def fetch_image_list():
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT image_name FROM images")
            images = cursor.fetchall()
            return [image[0] for image in images]
    finally:
        connection.close()

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if file_path:
        image_name = file_path.split('/')[-1]
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        connection = connect_to_db()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO images (image_name, image_data) VALUES (%s, %s)"
                cursor.execute(sql, (image_name, binary_data))
            connection.commit()
            messagebox.showinfo("Success", "Image uploaded successfully!")
            update_image_list()
        finally:
            connection.close()

def view_images():
    images = fetch_image_list()
    if images:
        messagebox.showinfo("Images in Database", "\n".join(images))
    else:
        messagebox.showinfo("Info", "No images found in the database.")

def download_image():
    image_list = fetch_image_list()
    if image_list:
        image_to_download = filedialog.askstring("Select Image", "Enter the image name to download:", initialvalue=image_list[0])
        if image_to_download:
            connection = connect_to_db()
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT image_data FROM images WHERE image_name=%s", (image_to_download,))
                    image_data = cursor.fetchone()[0]
                image = Image.open(io.BytesIO(image_data))
                save_path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=image_to_download)
                if save_path:
                    image.save(save_path)
                    messagebox.showinfo("Success", "Image downloaded successfully!")
            finally:
                connection.close()
    else:
        messagebox.showinfo("Info", "No images found in the database.")

def update_image_list():
    image_list = fetch_image_list()
    listbox.delete(0, tk.END)
    for image_name in image_list:
        listbox.insert(tk.END, image_name)

# Initialize the Tkinter application
root = tk.Tk()
root.title("Image Upload and Download")

# Create the database and table if not already created
create_database_and_table()

# Create a listbox to display the list of images
listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)

# Update the image list initially
update_image_list()

# Create buttons for the actions
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

view_button = tk.Button(root, text="View Images", command=view_images)
view_button.pack(pady=10)

download_button = tk.Button(root, text="Download Image", command=download_image)
download_button.pack(pady=10)

root.mainloop()
