### Project Overview: SafeDrive-Advanced-Driver-Authentication-System

In response to the significant issue of underage driving in India, which greatly increases the risk of accidents, we are developing an innovative solution. This project, designed to assist the government in addressing this problem, involves a central system containing a license database and a remote device installed in vehicles to authenticate a driver’s license before allowing the vehicle to start.

The system comprises two primary components:

1. **Central Device (Database Server)**
2. **Remote Device (Car Music Player)**

### Central Device Operations: Managing and Creating Licenses

The central device functions as the data management hub and is responsible for creating new driving licenses. Here’s how the process works:

1. **New License Creation**:
   - **Input Personal Details**: Collect information such as name, date of birth (DOB), mobile number, license approval date, license expiry date, and license number.
   - **RFID Card Integration**: Use a button to read the unique RFID card number.
   - **Biometric Data Collection**: Capture the right-hand index fingerprint using a fingerprint sensor.
   - **Photograph**: Take a high-quality image of the individual’s face.

   After entering all the details, clicking the 'Continue' button will:
   - Insert all data into the central database.
   - Write essential data (name, DOB, mobile number, license approval date, license expiry date) onto the RFID card with encryption for security.

### Remote Device Operations: Ensuring Driver Authentication

The remote device, which typically functions as a media player in vehicles, has additional features to ensure driver authentication. Here’s a detailed look at its operation:

1. **Vehicle Unlock and Initialization**:
   - When the vehicle is unlocked, the system starts and prompts for a valid driver’s license linked to the device.

2. **Authentication Process**:
   - The system requires the driver to scan their RFID card or provide a valid fingerprint. Only upon successful authentication can the vehicle be started, and the system then switches to the media player interface.

3. **Continuous Driver Monitoring**:
   - Throughout the drive, the system continuously monitors the driver’s face, matching it with the stored profile photograph to ensure the authenticated driver remains behind the wheel.

4. **Profile Management**:
   - An icon in the upper-right corner of the interface provides access to the driver’s profile details stored in the database. The profile menu offers three key options:
     - **Logout**: Logs the driver out and turns off the vehicle engine.
     - **Delete Profile**: Unlinks and removes the profile data from the device, enhancing security.
     - **Add New Profile**: Requires an internet connection to fetch data from the central server. The process involves:
       - Scanning the driving license using the RFID scanner to decode the encrypted card and retrieve the license number.
       - Verifying the license number against the central database. If valid, the system fetches all relevant data.
       - Confirming the addition of the new profile. The new driver can only start the vehicle if their fingerprint and facial recognition match the stored data.

### Technical Implementation

This system will be developed using Python programming language and will utilize PyMySQL for database management. 

### Vision: Enhancing Road Safety and Reducing Accidents

By integrating this Smart License Authentication System, we aim to create a safer driving environment in India. This technology ensures that vehicles are operated only by licensed and authorized drivers, thereby significantly reducing the likelihood of accidents caused by underage drivers. Through the use of advanced biometrics and continuous monitoring, our system offers an unprecedented level of security, promoting peace of mind for both drivers and regulatory authorities.

Join us in revolutionizing road safety with smart technology that safeguards lives and strengthens community protection.
