from rplidar import RPLidar
from collections import defaultdict

PORT_NAME = '/dev/ttyUSB0'
ANGLE_BIN_SIZE = 0.5  # Angle range in degrees for grouping.

def run():
    lidar = RPLidar(PORT_NAME)
    full_scan = []

    try:
        for scan in lidar.iter_scans(scan_type='normal'):
            full_scan.extend(scan)
            if len(full_scan) > 5000:  # Arbitrary limit to ensure full 360-degree coverage.
                break
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        lidar.stop()
        lidar.disconnect()

    # Group the data by angle bins.
    bins = defaultdict(list)
    for meas in full_scan:
        angle = round(meas[1] / ANGLE_BIN_SIZE) * ANGLE_BIN_SIZE
        bins[angle].append(meas)

    # Process the data and calculate the average.
    averaged_data = []
    for angle, measurements in sorted(bins.items()):
        avg_distance = sum(m[2] for m in measurements) / len(measurements)
        avg_quality = sum(m[0] for m in measurements) / len(measurements)
        averaged_data.append((angle, avg_distance, avg_quality))

    # Save the processed data to a file.
    with open('lidar_scan_data.txt', 'w') as f:
        f.write('#RPLIDAR SCAN DATA\n')
        f.write(f'#COUNT={len(averaged_data)}\n')
        f.write('#Angle\tDistance\tQuality\n')
        for meas in averaged_data:
            f.write(f'{meas[0]:.4f}\t{meas[1]:.2f}\t{int(meas[2])}\n')

if __name__ == '__main__':
    run()
