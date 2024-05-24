import time
import numpy as np
from matplotlib import pyplot as plt
import serial
import adafruit_fingerprint

# Setup serial communication with the fingerprint sensor
uart = serial.Serial("COM11", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# Function to capture and save a new fingerprint image
def capture_fingerprint_image(file_path):
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Got image...Transferring image data...")
    imgList = finger.get_fpdata("image", 2)
    imgArray = np.zeros(73728, np.uint8)
    for i, val in enumerate(imgList):
        imgArray[(i * 2)] = val & 240
        imgArray[(i * 2) + 1] = (val & 15) * 16
    imgArray = np.reshape(imgArray, (288, 256))
    plt.imsave(file_path, imgArray, cmap='gray')
    print(f"New fingerprint image saved as {file_path}")

# Function to load and process a fingerprint image
def load_fingerprint_image(file_path):
    img = plt.imread(file_path)
    return img

# Function to compare two fingerprint images
def compare_fingerprints(img1, img2):
    if np.array_equal(img1, img2):
        return True
    return False

# Main function
def main():
    # File paths
    old_fingerprint_file = "fingerprint_image.png"
    new_fingerprint_file = "new_fingerprint_image.png"

    # Capture a new fingerprint image
    capture_fingerprint_image(new_fingerprint_file)

    # Load the old and new fingerprint images
    old_fingerprint = load_fingerprint_image(old_fingerprint_file)
    new_fingerprint = load_fingerprint_image(new_fingerprint_file)

    # Compare the fingerprints
    if compare_fingerprints(old_fingerprint, new_fingerprint):
        print("Fingerprints match!")
    else:
        print("Fingerprints do not match.")

if __name__ == "__main__":
    main()
