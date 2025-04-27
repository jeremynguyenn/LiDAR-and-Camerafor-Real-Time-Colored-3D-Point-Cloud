import time
import board
import busio
import adafruit_adxl34x
import math

# Initiate I2C communication
i2c = busio.I2C(board.SCL, board.SDA)

# Initiate ADXL345 sensor
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Function to calculate the tilt relative to the XZ plane.
def calculate_inclination(x, z, calibration_offset):
    inclination = -(math.degrees(math.atan2(x, z)) - calibration_offset)
    return inclination

# Define the calibration offset manually.
calibration_offset = 86.39

# Number of samples to calculate the average.
num_samples = 100

# Interval between readings in seconds (can be adjusted or removed).
sample_interval = 0.01

# Path to the text file, change to your own directory.
file_path = "/home/user/angle.txt"

inclinations = []

# Collect num_samples samples.
for _ in range(num_samples):
    # Read accelerometer values
    x, y, z = accelerometer.acceleration
    
    # Calculate the tilt relative to the XZ plane.
    inclination = calculate_inclination(x, z, calibration_offset)
    
    # Add the tilt to the list.
    inclinations.append(inclination)
    
    if sample_interval > 0:
        time.sleep(sample_interval)

# Calculate the average of the tilts.
average_inclination = sum(inclinations) / num_samples

# Write the average to the text file.
with open(file_path, "w") as file:
    file.write(f"Average Inclination: {average_inclination:.2f}°\n")

# The code now ends execution after saving the value to the file.
