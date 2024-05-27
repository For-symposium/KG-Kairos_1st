import time
from rplidar import RPLidar

# Specify the serial port where the RPLidar is connected
PORT_NAME = '/dev/tty.usbserial-0001'  # Update this port according to your system

def run_lidar():
    # Create a RPLidar object
    lidar = RPLidar(PORT_NAME)
    
    try:
        # Start scanning
        print("Starting RPLIDAR...")
        for scan in lidar.iter_scans():
            for (_, angle, distance) in scan:
                if 177 < angle < 183:
                    print(f"Angle: {angle:.2f}°, Distance: {distance/10:.2f} cm")
                
            # Adding a small sleep to avoid overwhelming the output
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("Stopping...")
    
    finally:
        # Stop the lidar and disconnect
        lidar.stop()
        lidar.disconnect()

if __name__ == '__main__':
    run_lidar()
