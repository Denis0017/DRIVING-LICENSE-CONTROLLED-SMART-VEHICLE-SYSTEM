import pymysql

try:
    connection = pymysql.connect(
        host='localhost', user='root', password='1223')
    cursor = connection.cursor()
except:
    print("error: database dose not connect")

try:
    query = 'create database userdata'
    cursor.execute(query)
    query = 'use userdata'
    cursor.execute(query)
    query = 'create table data(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), date_of_birth DATE, mobile_number VARCHAR(15), license_approval_date DATE, license_expiry_date DATE, license_number VARCHAR(20), rfid_card VARCHAR(50), fingerprint BLOB, photo LONGBLOB)'
    cursor.execute(query)
except:
    cursor.execute('use userdata')
connection.close()


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
