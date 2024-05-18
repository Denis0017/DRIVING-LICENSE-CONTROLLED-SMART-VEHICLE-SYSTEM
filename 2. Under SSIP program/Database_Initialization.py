import pymysql

try:
    connection = pymysql.connect(
        host='localhost', user='root', password='1223')
    cursor = connection.cursor()
    print("Database connected successfully")
    
    try:
        query = 'create database userdata'
        cursor.execute(query)
        query = 'use userdata'
        cursor.execute(query)
        query = 'create table data(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), date_of_birth DATE, mobile_number VARCHAR(15), license_approval_date DATE, license_expiry_date DATE, license_number VARCHAR(20), rfid_card VARCHAR(50), fingerprint BLOB, photo LONGBLOB)'
        cursor.execute(query)
        print("Database and table created successfully")
    except pymysql.MySQLError as e:
        print(f"Error occurred: {e}")
        try:
            cursor.execute('use userdata')
            print("Using existing database 'userdata'")
        except pymysql.MySQLError as e:
            print(f"Error occurred while switching to 'userdata': {e}")
    
    connection.close()
    print("Database connection closed")
except pymysql.MySQLError as e:
    print(f"Error: database does not connect. {e}")


# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='1223')

# cursor = connection.cursor()
# cursor.execute("""cerate database license_db""")
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS licenses (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(255),
#     dob DATE,
#     mobile_number VARCHAR(15),
#     license_approval_date DATE,
#     license_expiry_date DATE,
#     license_number VARCHAR(20),
#     rfid_card VARCHAR(50),
#     fingerprint BLOB,
#     photo LONGBLOB
# )
# """)
# connection.close()
