import subprocess
import time
import numpy as np
import cv2


def execute_adb_command(command):
    """
    Execute an adb command and return the output.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        print(result.stderr)
    return result.stdout


def take_screenshot(device_id=None):
    """
     Take a screenshot from an Android device and process it using OpenCV.
     """
    adb_command = "adb"
    if device_id:
        adb_command += f" -s {device_id}"
    screencap_command = f"{adb_command} shell screencap -p"
    # Execute the command and get the raw image data
    print("Taking screenshot...")
    raw_image = execute_adb_command(screencap_command)
    # Convert the raw image data to a numpy array
    image_array = np.frombuffer(raw_image, dtype=np.uint8)
    # Decode the image array to an OpenCV image
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image is None:
        print("Failed to decode image")
        return
    # Process the image using OpenCV
    print("Processing the screenshot with OpenCV...")
    # Example processing: Convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Display the image
    cv2.imshow('Screenshot', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return image


def tap_screen(x, y, device_id=None):
    """
    Simulate a tap on the Android device at the specified (x, y) coordinates.
    """
    adb_command = "adb"
    if device_id:
        adb_command += f" -s {device_id}"

    tap_command = f"{adb_command} shell input tap {x} {y}"

    # Execute the command
    print(f"Tapping on screen at ({x}, {y})...")
    execute_adb_command(tap_command)


def tap_screen_time(x, y, duration_ms=100, device_id=None):
    """
    Simulate a tap on the Android device at the specified (x, y) coordinates with a specified duration.
    """
    adb_command = "adb"
    if device_id:
        adb_command += f" -s {device_id}"

    # The swipe command with the same start and end points can be used to control the tap duration
    tap_command = f"{adb_command} shell input swipe {x} {y} {x} {y} {duration_ms}"

    # Execute the command
    print(f"Tapping on screen at ({x}, {y}) for {duration_ms} milliseconds...")
    execute_adb_command(tap_command)


def swipe_screen(start_x, start_y, end_x, end_y, duration=300, device_id=None):
    """
    Simulate a swipe on the Android device from the specified (start_x, start_y) coordinates
    to the (end_x, end_y) coordinates.
    """
    adb_command = "adb"
    if device_id:
        adb_command += f" -s {device_id}"

    swipe_command = f"{adb_command} shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}"

    # Execute the command
    print(f"Swiping on screen from ({start_x}, {start_y}) to ({end_x}, {end_y}) with duration {duration}ms...")
    execute_adb_command(swipe_command)


def move(direction, start_x=500, start_y=1000, distance=300, duration=300, device_id=None):
    """
    Move in one of the eight directions from the (start_x, start_y) coordinates.
    """
    direction_dict = {
        "up": (0, -distance),
        "down": (0, distance),
        "left": (-distance, 0),
        "right": (distance, 0),
        "left_up": (-distance, -distance),
        "right_up": (distance, -distance),
        "left_down": (-distance, distance),
        "right_down": (distance, distance),
    }

    if direction in direction_dict:
        delta_x, delta_y = direction_dict[direction]
        end_x = start_x + delta_x
        end_y = start_y + delta_y
        swipe_screen(start_x, start_y, end_x, end_y, duration, device_id)
    else:
        print(f"Invalid direction: {direction}")


# Example usage
if __name__ == "__main__":
    device_id_input = None  # Replace with your device ID if you have multiple devices connected
    take_screenshot(device_id_input)
    x_input = 500  # Replace with your desired x coordinate
    y_input = 1000  # Replace with your desired y coordinate
    device_id_input = None  # Replace with your device ID if you have multiple devices connected
    tap_screen(x_input, y_input, device_id_input)
    start_x_input = 100  # Replace with your desired start x coordinate
    start_y_input = 100  # Replace with your desired start y coordinate
    end_x_input = 500  # Replace with your desired end x coordinate
    end_y_input = 1000  # Replace with your desired end y coordinate
    duration_input = 500  # Duration of the swipe in milliseconds
    device_id_input = None  # Replace with your device ID if you have multiple devices connected
    swipe_screen(start_x_input, start_y_input, end_x_input, end_y_input, duration_input, device_id_input)
    directions = ["up", "down", "left", "right", "left_up", "right_up", "left_down", "right_down"]
    for direct in directions:
        print(f"Moving {direct}")
        move(start_x_input, start_y_input, end_x_input, end_y_input, duration_input, device_id_input)
        time.sleep(1)  # Add a delay between movements for demonstration purposes
