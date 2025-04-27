import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize
import matplotlib.image as mpimg
import re
import os

# Define the offset variables.
add_coord_x = 0
add_coord_y = 280

def carregar_dados(arquivo):
    with open(arquivo, 'r') as f:
        for _ in range(3):
            next(f)  # Skip the header.
        dados = np.loadtxt(f)
    return dados[:, 0], dados[:, 1]

def plotar_dados():
    angulos, distancias = carregar_dados('/home/edu/Desktop/lidar_scan_data.txt')
    angulo_de_rotacao = 92
    angulos_radianos = np.radians(angulos + angulo_de_rotacao)

    x = distancias * np.cos(angulos_radianos)
    y = distancias * np.sin(angulos_radianos)
    x = -x  # Mirror the data on the X-axis.

    fov = 54  # Field of View in degrees. Adjust according to your camera.
    central_angle_deg = 90 + angulo_de_rotacao

    angles_points = (np.degrees(np.arctan2(y, -x)) % 360)  # Normalize angles
    angle_left_boundary = (central_angle_deg - fov / 2) % 360
    angle_right_boundary = (central_angle_deg + fov / 2) % 360

    if angle_left_boundary < angle_right_boundary:
        within_fov = (angles_points >= angle_left_boundary) & (angles_points <= angle_right_boundary)
    else:
        within_fov = (angles_points >= angle_left_boundary) | (angles_points <= angle_right_boundary)

    return np.column_stack((x[within_fov], y[within_fov])), angles_points[within_fov]

def rotacionar_pontos(points):
    def rotate(points, angles):
        angle_x, angle_y, angle_z = np.radians(angles)
       
        # Rotation matrix around the X-axis.
        rot_x = np.array([[1, 0, 0],
                          [0, np.cos(angle_x), -np.sin(angle_x)],
                          [0, np.sin(angle_x), np.cos(angle_x)]])
       
        # Rotation matrix around the Y-axis.
        rot_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                          [0, 1, 0],
                          [-np.sin(angle_y), 0, np.cos(angle_y)]])
       
        # Rotation matrix around the Z-axis.
        rot_z = np.array([[np.cos(angle_z), -np.sin(angle_z), 0],
                          [np.sin(angle_z), np.cos(angle_z), 0],
                          [0, 0, 1]])
       
        # Rotate the points
        rotated_points = points @ rot_x.T @ rot_y.T @ rot_z.T
        return rotated_points

    # Add the Z dimension to the points.
    points_3d = np.hstack((points, np.zeros((len(points), 1))))
   
    # Set the rotation angles: 0 degrees for X, 0 degrees for Y, and 0 degrees for Z.
    rotated_points = rotate(points_3d, [0, 0, 0])
   
    return rotated_points[:, :2]  # Return only the x and y coordinates.

# Load and process the data.
points_within_fov, angles_red_points = plotar_dados()

# Remap the normalized angles to X coordinates (0 to 2592). Change according to the resolution of your camera.
x_min = 0
x_max = 2592
y_line = 972  # Adjustable value for the line height.
min_angle = np.min(angles_red_points)
max_angle = np.max(angles_red_points)
shift = -(min_angle + (max_angle - min_angle) / 2)
normalized_angles = angles_red_points + shift

x_coords = np.interp(normalized_angles, (min(normalized_angles), max(normalized_angles)), (x_min, x_max))
new_xy_coordinates = np.column_stack((x_coords, [y_line] * len(x_coords)))

# Load and resize the image.
image_path = '/home/edu/Desktop/testando.jpg'
image = np.rot90(mpimg.imread(image_path), k=0)
resized_image = resize(image, (1944, 2592))

# Filter the points that are within the x range from 0 to 2592.
filtered_xy_coordinates = []
for point in new_xy_coordinates:
    shifted_x = point[0] + add_coord_x
    if 0 <= shifted_x <= 2592:
        shifted_point = (shifted_x, point[1] + add_coord_y)
        filtered_xy_coordinates.append(shifted_point)

# Get RGB values from the pixels.
pixel_values = []
for point in new_xy_coordinates:
    rounded_x = int(round(point[0] + add_coord_x))
    rounded_y = int(round(point[1] + add_coord_y))
    adjusted_y = resized_image.shape[0] - 1 - rounded_y
    if 0 <= rounded_x < resized_image.shape[1] and 0 <= adjusted_y < resized_image.shape[0]:
        pixel_value = resized_image[adjusted_y, rounded_x] * 255
        pixel_values.append(pixel_value)

# Fix the size mismatch between arrays.
points_within_fov_with_z = np.column_stack((points_within_fov, np.zeros(points_within_fov.shape[0])))
pixel_values = np.array(pixel_values)  # Converta para array numpy

# Make sure the number of points and RGB values match.
min_len = min(len(points_within_fov_with_z), len(pixel_values))
points_within_fov_with_z = points_within_fov_with_z[:min_len]
pixel_values = pixel_values[:min_len]

# Convert pixel_values to 2D, if necessary.
pixel_values = pixel_values[:, np.newaxis] if pixel_values.ndim == 1 else pixel_values

# Combine the data
combined_result = np.hstack((points_within_fov_with_z, pixel_values))

# Function to get the next file name.
def get_next_filename(folder_path, base_name='plot_', extension='.txt'):
    # List all the files in the directory.
    files = os.listdir(folder_path)
    
    # Filter files that match the pattern 'plot_x.txt'.
    plot_files = [f for f in files if f.startswith(base_name) and f.endswith(extension)]
    
    #If no files exist, start with plot_1.txt.
    if not plot_files:
        return os.path.join(folder_path, f"{base_name}1{extension}")
    
    # Extract the number from the highest existing file.
    numbers = [int(f[len(base_name):-len(extension)]) for f in plot_files]
    max_number = max(numbers)
    
    # Return the next file name.
    return os.path.join(folder_path, f"{base_name}{max_number + 1}{extension}")

# The name of the next file.
file_path = get_next_filename('/home/user/plot/')

# Path to the text file containing the tilt angle value.
file_path_angle = '/home/user/angle.txt'

# Read the content of the file.
with open(file_path_angle, 'r') as file:
    content = file.read()

# Use a regular expression to extract the numerical tilt value, including negative numbers.
angle_match = re.search(r'Average Inclination:\s*([-?\d.]+)°', content)
if angle_match:
    angle_degrees = float(angle_match.group(1))
else:
    raise ValueError("Could not find the angle in the text file.")

# Convert the angle to radians.
angle_radians = np.deg2rad(angle_degrees)

# Define the rotation matrix for a rotation around the Y-axis.
rotation_matrix_y = np.array([
    [np.cos(angle_radians), 0, np.sin(angle_radians)],
    [0, 1, 0],
    [-np.sin(angle_radians), 0, np.cos(angle_radians)]
])

# Define xyz
xyz = combined_result[:, :3]

# Rotate each point
rotated_xyz = np.dot(xyz, rotation_matrix_y.T)

# Save the rotated data in a .txt file.
header = 'X Y Z R'
np.savetxt(file_path, np.hstack((rotated_xyz, combined_result[:, 3:])), header=header, fmt='%10.5f')

print(f"Arquivo salvo em: {file_path}")
