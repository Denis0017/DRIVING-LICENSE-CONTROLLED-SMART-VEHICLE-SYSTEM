import pymysql
import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
from PIL import Image, ImageTk

def connect_to_db():
    try:
        connection = pymysql.connect(
            host='localhost', 
            user="root", 
            password="1223",
            database='userdata'
        )
        print("Database connected successfully")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error: database does not connect. {e}")
        return None

def add_record(cursor, name, date_of_birth, mobile_number, license_approval_date, license_expiry_date, license_number, rfid_card, fingerprint, photo):
    try:
        cursor.execute("""
            INSERT INTO data (name, date_of_birth, mobile_number, license_approval_date, 
                              license_expiry_date, license_number, rfid_card, fingerprint, photo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, date_of_birth, mobile_number, license_approval_date, 
              license_expiry_date, license_number, rfid_card, fingerprint, photo))
        messagebox.showinfo("Success", "Record added successfully")
    except pymysql.MySQLError as e:
        messagebox.showerror("Error", f"Failed to add record: {e}")

def main():
    connection = connect_to_db()
    if not connection:
        return
    cursor = connection.cursor()

    def on_add():
        add_record(cursor, name_var.get(), dob_var.get(), mobile_var.get(), approval_var.get(), expiry_var.get(), license_var.get(), rfid_var.get(), fingerprint_var.get(), photo_var.get())
        connection.commit()

    def select_file(var):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                var.set(file.read())

    def capture_photo(var):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Captured Photo', frame)
            cv2.waitKey(0)
            cap.release()
            cv2.destroyAllWindows()
            _, buffer = cv2.imencode('.jpg', frame)
            var.set(buffer.tobytes())
        else:
            messagebox.showerror("Error", "Failed to capture photo")

    def capture_fingerprint(var):
        # Placeholder function to simulate fingerprint data retrieval
        # Replace this with actual sensor data retrieval logic
        fingerprint_data = b'\x00\x01\x02\x03\x04'  # Dummy binary data
        var.set(fingerprint_data)

    root = tk.Tk()
    root.title("Add Data to Database")

    # Labels
    tk.Label(root, text="Name:").grid(row=0, column=0)
    tk.Label(root, text="Date of Birth (YYYY-MM-DD):").grid(row=1, column=0)
    tk.Label(root, text="Mobile Number:").grid(row=2, column=0)
    tk.Label(root, text="License Approval Date (YYYY-MM-DD):").grid(row=3, column=0)
    tk.Label(root, text="License Expiry Date (YYYY-MM-DD):").grid(row=4, column=0)
    tk.Label(root, text="License Number:").grid(row=5, column=0)
    tk.Label(root, text="RFID Card:").grid(row=6, column=0)
    tk.Label(root, text="Fingerprint:").grid(row=7, column=0)
    tk.Label(root, text="Photo:").grid(row=8, column=0)

    # Entry fields
    name_var = tk.StringVar()
    tk.Entry(root, textvariable=name_var).grid(row=0, column=1)
    dob_var = tk.StringVar()
    tk.Entry(root, textvariable=dob_var).grid(row=1, column=1)
    mobile_var = tk.StringVar()
    tk.Entry(root, textvariable=mobile_var).grid(row=2, column=1)
    approval_var = tk.StringVar()
    tk.Entry(root, textvariable=approval_var).grid(row=3, column=1)
    expiry_var = tk.StringVar()
    tk.Entry(root, textvariable=expiry_var).grid(row=4, column=1)
    license_var = tk.StringVar()
    tk.Entry(root, textvariable=license_var).grid(row=5, column=1)
    rfid_var = tk.StringVar()
    tk.Entry(root, textvariable=rfid_var).grid(row=6, column=1)
    
    fingerprint_var = tk.StringVar()
    tk.Button(root, text="Capture Fingerprint", command=lambda: capture_fingerprint(fingerprint_var)).grid(row=7, column=1)
    
    photo_var = tk.StringVar()
    tk.Button(root, text="Capture Photo", command=lambda: capture_photo(photo_var)).grid(row=8, column=1)

    # Button
    tk.Button(root, text="Add Record", command=on_add).grid(row=9, column=0)

    root.mainloop()

    cursor.close()
    connection.close()
    print("Database connection closed")

if __name__ == "__main__":
    main()
