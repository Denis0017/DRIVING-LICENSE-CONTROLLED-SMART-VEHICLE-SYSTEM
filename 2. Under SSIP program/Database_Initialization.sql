create database licence_userdata
use licence_userdata
create table data(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), date_of_birth DATE, mobile_number VARCHAR(15), license_approval_date DATE, license_expiry_date DATE, license_number VARCHAR(20), rfid_card VARCHAR(50), fingerprint BLOB, photo LONGBLOB)
use licence_userdata