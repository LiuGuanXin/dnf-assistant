import subprocess
import time


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
    Take a screenshot from an Android device and pull it to the local machine.
    """
    screenshot_path_on_device = "/sdcard/screenshot.png"
    screenshot_path_local = "screenshot.png"

    # Construct the adb commands
    adb_command = "adb"
    if device_id:
        adb_command += f" -s {device_id}"

    screencap_command = f"{adb_command} shell screencap -p {screenshot_path_on_device}"
    pull_command = f"{adb_command} pull {screenshot_path_on_device} {screenshot_path_local}"

    # Execute the commands
    print("Taking screenshot...")
    execute_adb_command(screencap_command)
    print("Pulling screenshot to local machine...")
    execute_adb_command(pull_command)
    print(f"Screenshot saved as {screenshot_path_local}")


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
