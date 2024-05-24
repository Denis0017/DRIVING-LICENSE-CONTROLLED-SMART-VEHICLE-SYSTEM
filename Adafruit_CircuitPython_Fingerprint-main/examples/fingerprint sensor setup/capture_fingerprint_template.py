import serial
import adafruit_fingerprint
import pymysql

# Setup serial communication with the fingerprint sensor
uart = serial.Serial("COM11", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# Connect to MySQL
conn = pymysql.connect(host='localhost', user='root', password='1223', database='fingerprint_db')
cursor = conn.cursor()

def capture_fingerprint_template():
    print("Waiting for finger...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Image taken")

    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to template")

    print("Creating model...")
    if finger.create_model() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to create model")

    print("Saving model...")
    template = finger.get_fpdata("char", 1)
    
    # Save the template to MySQL
    cursor.execute("INSERT INTO fingerprint_templates (template) VALUES (%s)", (template,))
    conn.commit()
    print("Template saved to database")

if __name__ == "__main__":
    capture_fingerprint_template()
    cursor.close()
    conn.close()
