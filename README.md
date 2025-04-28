## Features  
- **Real-Time 3D Point Cloud Generation**: Combines LiDAR data and images for colored 3D point clouds.  
- **Edge Device Optimization**: Designed to work efficiently on single-board computers.  
- **Simplified Workflow**: All processing is consolidated in a single pipeline for ease of use.

## Prerequisites  
- **Hardware**:  
  - 2D LiDAR sensor (recommend Slamtec RPLIDAR A1)
  - Camera module compatible with `libcamera` (recommend rev 1.3 camera module)
  - Servo motors (for LiDAR adjustment, recommend Mg996r)
  - Accelerometer (recommend ADXL345)
  - Single Board Computer (recommend Raspberry Pi 4)
- **Software**:  
  - Python (>=3.6)
  - Pi OS (recommended)

## Prototype Assembly Instructions
The STL files for the prototype can be found in the prototype folder of this repository. Simply download the files and use a 3D printer for printing.
The material used for printing is PLA 1.75mm filament, with a layer height of 0.2mm for optimal results.
There is also a video of the mounting process. Feel free to download, if necessary.
| ![LiDAR System](https://github.com/jeremynguyenn/LiDAR-and-Camerafor-Real-Time-Colored-3D-Point-Cloud/blob/main/LiDAR-and-Camera-for-Real-Time-3D-Point-Cloud/Prototype/prototipo_final.png) | 

## Video demo model
![Prototype Demo](https://github.com/jeremynguyenn/LiDAR-and-Camerafor-Real-Time-Colored-3D-Point-Cloud/blob/main/LiDAR-and-Camera-for-Real-Time-3D-Point-Cloud/Prototype/prototype_final.gif)

## Running the Code  

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/jeremynguyenn/LiDAR-and-Camerafor-Real-Time-Colored-3D-Point-Cloud.git  
   cd Edge-Based-Fusion-of-LiDAR-and-Camera-Data  
   ./main.sh


## Code Tutorial

Running the `main.sh` script will execute the following functions in sequence. Descriptions of each function are provided below

        libcamera-jpeg -o testando.jpg --shutter 20000
- libcamera-jpeg: This is the command-line tool used to capture JPEG images with the libcamera library.
- -o testando.jpg: This option specifies the output file where the captured image will be saved.
- --shutter 20000: This option controls the shutter speed of the camera. The value 20000 refers to the exposure time in microseconds (µs). So, in this case, the camera's shutter is open for 20 milliseconds (20000 µs). A longer shutter speed allows more light to reach the camera sensor, which can be useful in low-light environments but might also cause motion blur if the camera or subject moves. Adapt it according to the ambient light.
  
      python3 log.py
- Imports RPLidar to interact with the lidar sensor and defaultdict to handle data grouped by angle bins.
- Defines the sensor port (/dev/ttyUSB0) and sets the angle bin size (0.5°).
- Initializes the lidar sensor.
- Collects scan data in "normal" mode, appending it to a list until 5000 points are captured.
- Handles any errors during scanning.
- Stops and disconnects from the lidar after scanning.
- Groups scan data into angle bins (e.g., 0.5° increments) using a dictionary.
- For each angle bin, calculates the average distance and quality.
- Stores the averaged data.
- Writes the averaged data (angle, distance, quality) to a file (lidar_scan_data.txt).
- This script captures lidar data, processes it into averaged values by angle, and saves it for further use.

      python3 acelerometer.py
- Imports libraries for time management, I2C communication, and accelerometer interaction (using the ADXL345 sensor).
- Initializes I2C communication using busio.I2C with the SCL and SDA pins from the board library. Check the pinout of your SBC.
- Initializes the ADXL345 accelerometer sensor using the I2C bus.
- Defines a function (calculate_inclination) to calculate the tilt (inclination) based on the X and Z accelerometer values, with an optional calibration offset.
- The inclination is computed as the arctangent of the X and Z values, adjusted by the calibration offset.
- Sets a calibration_offset for accurate tilt calculation.
- Defines num_samples as 100 (number of samples to average) and sample_interval as 0.01 seconds (time between readings).
- Collects accelerometer data for num_samples iterations.
- Reads X, Y, and Z acceleration values from the sensor.
- Calculates the inclination for each reading and appends it to a list.
- After collecting the data, calculates the average inclination from the list of collected values.
- Writes the calculated average inclination to a text file (/home/user/angle.txt).
- The script finishes after saving the average inclination to the file.

      python3 lidar_plot.py
- numpy and matplotlib are used for mathematical operations and plotting.
- skimage.transform.resize is used to resize images.
- re is used for regular expressions, and os handles file system operations.
- add_coord_x and add_coord_y are set to shift the coordinates of the points.
- Loads lidar scan data from a specified text file, skipping the header and extracting angle and distance values.
- Calculates and transforms lidar scan data into Cartesian coordinates (x, y).
- Filters the data based on the camera’s field of view (FOV).
- Returns the points within the FOV, adjusting angles for plotting.
- Rotates the points in 3D space based on specified rotation angles around the X, Y, and Z axes.
- Converts lidar data into 2D (x, y) coordinates, adjusting them based on the camera’s field of view and resolution.
- Resizes an image to match the lidar data's x-coordinate range.
- Filters points based on the x-coordinate range.
- Extracts RGB pixel values from the resized image based on the lidar data coordinates.
- Combines the lidar points and corresponding RGB values into a single dataset.
- A function (get_next_filename) determines the next available filename for saving the processed data.
- Reads the tilt angle from a text file (angle.txt).
- Extracts the angle using a regular expression and converts it to radians.
- Defines a rotation matrix to rotate the 3D points around the Y-axis using the tilt angle.
- Applies the rotation matrix to the lidar points.
- Saves the rotated data along with the RGB values to a text file, with a header indicating the data format.
- Prints the file path where the processed data is saved.
- This script processes lidar data, adjusts it for camera FOV and resolution, combines it with pixel color values from an image, rotates the data based on a tilt angle, and saves the result to a file for further analysis.

      python3 servo_up.py
      python3 servo_down.py
- Configures Raspberry Pi GPIO to control a servo motor via PWM on pin 11.
- set_servo_angle(angle): Moves the servo to the specified angle (0-180 degrees).
- get_current_angle(): Reads and returns the servo's current angle from a file.
- save_current_angle(angle): Saves the current angle to a file.
- eads the current angle, increments or decrements it, moves the servo, and updates the angle file.
- Stops PWM and cleans up GPIO on script termination.

      python3 final_plot.py
- numpy is used for numerical operations and array handling.
- matplotlib.pyplot is used for plotting the data in 3D.
- os and glob are used for handling file operations and accessing files in a folder.
- Uses glob to search for files matching the pattern plot_*.txt in a specified directory (pasta).
- Loads the data from each file using np.loadtxt and appends them to a list.
- Combines all loaded data into a single 2D numpy array using np.vstack.
- Creates a 3D scatter plot using matplotlib.
- Extracts the XYZ coordinates (first 3 columns) and RGB values (last 3 columns) from the data.
- Normalizes the RGB values to the range [0, 1].
- Plots the points using ax.scatter, with a red point at the origin and the rest colored according to their RGB values.
- Sets the limits for the X, Y, and Z axes.
- Configures the 3D view's elevation and azimuth for better visualization.
- Defines pasta_dados as the folder path where the .txt files are stored.
- Loads all the data from the .txt files in the specified folder using carregar_dados_arquivos.
- Plots the loaded data using plotar_dados.
