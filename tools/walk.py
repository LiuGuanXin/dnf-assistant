import subprocess
import time


# adb操作手机
# 1. 实时录屏并展示
# 2. 操作点击、操作滑动实现
# 3. 操作位置坐标获取，实现通过点击操作记录位置坐标
# 4. 八方向移动实现
# 需要记录的操作坐标
# 1. 移动轮盘位置。 2. 技能位置。 3. 地图位置  4. 再来一次位置。 5.修理位置。
def execute_adb_command(command):
    """
    Execute an adb command and return the output.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        print(result.stderr)
    return result.stdout


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
    execute_adb_command(swipe_command)


def move(direction, start_x=500, start_y=1000, distance=300, duration=300, device_id=None):
    """
    Move in one of the eight directions from the (start_x, start_y) coordinates.
    """
    directions = {
        "up": (0, -distance),
        "down": (0, distance),
        "left": (-distance, 0),
        "right": (distance, 0),
        "left_up": (-distance, -distance),
        "right_up": (distance, -distance),
        "left_down": (-distance, distance),
        "right_down": (distance, distance),
    }

    if direction in directions:
        delta_x, delta_y = directions[direction]
        end_x = start_x + delta_x
        end_y = start_y + delta_y
        swipe_screen(start_x, start_y, end_x, end_y, duration, device_id)
    else:
        print(f"Invalid direction: {direction}")


# Example usage
# if __name__ == "__main__":
#     device_id = None  # Replace with your device ID if you have multiple devices connected
#     start_x = 500  # Starting x coordinate
#     start_y = 1000  # Starting y coordinate
#     distance = 300  # Distance to move in pixels
#     duration = 300  # Duration of the swipe in milliseconds
#
#     directions = ["up", "down", "left", "right", "left_up", "right_up", "left_down", "right_down"]
#     for direction in directions:
#         print(f"Moving {direction}")
#         move(direction, start_x, start_y, distance, duration, device_id)
#         time.sleep(1)  # Add a delay between movements for demonstration purposes
