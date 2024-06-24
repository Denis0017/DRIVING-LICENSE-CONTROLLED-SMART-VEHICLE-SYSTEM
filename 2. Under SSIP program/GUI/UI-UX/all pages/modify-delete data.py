import pymysql
import getpass
import tkinter as tk
from tkinter import messagebox

def connect_to_db():
    try:
        connection = pymysql.connect(
            host='localhost', 
            user=input("Enter your MySQL username: "), 
            password=getpass.getpass("Enter your MySQL password: "),
            database='userdata'
        )
        print("Database connected successfully")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error: database does not connect. {e}")
        return None

def remove_record(cursor, record_id):
    try:
        cursor.execute("DELETE FROM data WHERE id = %s", (record_id,))
        messagebox.showinfo("Success", "Record removed successfully")
    except pymysql.MySQLError as e:
        messagebox.showerror("Error", f"Failed to remove record: {e}")

def modify_record(cursor, record_id, name, date_of_birth, mobile_number, license_approval_date, license_expiry_date, license_number, rfid_card, fingerprint, photo):
    try:
        updates = []
        params = []
        if name:
            updates.append("name = %s")
            params.append(name)
        if date_of_birth:
            updates.append("date_of_birth = %s")
            params.append(date_of_birth)
        if mobile_number:
            updates.append("mobile_number = %s")
            params.append(mobile_number)
        if license_approval_date:
            updates.append("license_approval_date = %s")
            params.append(license_approval_date)
        if license_expiry_date:
            updates.append("license_expiry_date = %s")
            params.append(license_expiry_date)
        if license_number:
            updates.append("license_number = %s")
            params.append(license_number)
        if rfid_card:
            updates.append("rfid_card = %s")
            params.append(rfid_card)
        if fingerprint:
            updates.append("fingerprint = %s")
            params.append(fingerprint)
        if photo:
            updates.append("photo = %s")
            params.append(photo)

        params.append(record_id)
        cursor.execute(f"UPDATE data SET {', '.join(updates)} WHERE id = %s", params)
        messagebox.showinfo("Success", "Record modified successfully")
    except pymysql.MySQLError as e:
        messagebox.showerror("Error", f"Failed to modify record: {e}")

def main():
    connection = connect_to_db()
    if not connection:
        return
    cursor = connection.cursor()

    def on_remove():
        remove_record(cursor, int(record_id_var.get()))
        connection.commit()

    def on_modify():
        modify_record(cursor, int(record_id_var.get()), name_var.get(), dob_var.get(), mobile_var.get(), approval_var.get(), expiry_var.get(), license_var.get(), rfid_var.get(), fingerprint_var.get(), photo_var.get())
        connection.commit()

    root = tk.Tk()
    root.title("Modify/Delete Data")

    # Labels
    tk.Label(root, text="Name:").grid(row=0, column=0)
    tk.Label(root, text="Date of Birth (YYYY-MM-DD):").grid(row=1, column=0)
    tk.Label(root, text="Mobile Number:").grid(row=2, column=0)
    tk.Label(root, text="License Approval Date (YYYY-MM-DD):").grid(row=3, column=0)
    tk.Label(root, text="License Expiry Date (YYYY-MM-DD):").grid(row=4, column=0)
    tk.Label(root, text="License Number:").grid(row=5, column=0)
    tk.Label(root, text="RFID Card:").grid(row=6, column=0)
    tk.Label(root, text="Fingerprint (as binary data):").grid(row=7, column=0)
    tk.Label(root, text="Photo (as binary data):").grid(row=8, column=0)
    tk.Label(root, text="Record ID to Remove/Modify:").grid(row=9, column=0)

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
    tk.Entry(root, textvariable=fingerprint_var).grid(row=7, column=1)
    photo_var = tk.StringVar()
    tk.Entry(root, textvariable=photo_var).grid(row=8, column=1)
    record_id_var = tk.StringVar()
    tk.Entry(root, textvariable=record_id_var).grid(row=9, column=1)

    # Buttons
    tk.Button(root, text="Remove Record", command=on_remove).grid(row=10, column=0)
    tk.Button(root, text="Modify Record", command=on_modify).grid(row=10, column=1)

    root.mainloop()

    cursor.close()
    connection.close()
    print("Database connection closed")

if __name__ == "__main__":
    main()
