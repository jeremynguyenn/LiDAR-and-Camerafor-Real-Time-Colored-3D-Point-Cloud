#!/bin/bash

# Number of repetitions
# User input, the present prototype only supports 25 moves each, starting from top or bottom
# Make sure to position it at maximum or minimum
NUM_REPETICOES=25

# Loop to repeat the sequence of commands
for ((i=1; i<=NUM_REPETICOES; i++))
do
    echo "Executing iteration $i of $NUM_REPETICOES"

    # Change directory
    cd /home/user/Desktop

    # Takes a photo and saves it as testando.jpg
    libcamera-jpeg -o testando.jpg --shutter 20000

    # Executes a script to obtain LiDAR points
    python3 log.py

    # Executes a script to get the accelerometer angle
    # The angle is saved to angle.txt
    python3 acelerometer.py

    # Executes the main code that overlays the LiDAR points on the image
    # Generates .txt files for each execution, located in the plot folder
    python3 lidar_plot.py

    # Moves the LiDAR upwards or backwards
    # Uncomment the line you are using
    # You can automate the code to run continuously, cycling between servo up and servo down
    # python3 servo_up.py
    # python3 servo_down.py

done

# After the loop, plots all the generated .txt files
python3 final_plot.py
