import pyautogui
import time


def press_key(key, press_time):
    """按下并释放单个按键，并设置按压时间"""
    pyautogui.keyDown(key)
    time.sleep(press_time)
    pyautogui.keyUp(key)


def press_keys(keys, press_time):
    """按下并释放多个按键，并设置按压时间"""
    for key in keys:
        pyautogui.keyDown(key)
    time.sleep(press_time)
    for key in keys:
        pyautogui.keyUp(key)


def single_click(x, y):
    """在指定坐标进行单击"""
    pyautogui.click(x, y)


def click_and_hold(x, y, hold_time):
    """在指定坐标单击并按住指定时间"""
    pyautogui.mouseDown(x, y)
    time.sleep(hold_time)
    pyautogui.mouseUp(x, y)


def click_and_drag(x, y, x_offset, y_offset, drag_time):
    """在指定坐标单击按住并拖动到目标位置"""
    pyautogui.mouseDown(x, y)
    pyautogui.moveTo(x + x_offset, y + y_offset, drag_time)
    pyautogui.mouseUp()


def move(direction, distance):
    # 根据距离计算按压时间
    press_time = distance / 10
    # 八方向
    if direction == 'up':
        press_key('w', press_time)
    elif direction == 'down':
        press_key('s', press_time)
    elif direction == 'left':
        press_key('a', press_time)
    elif direction == 'right':
        press_key('d', press_time)
    elif direction == 'topLeft':
        press_keys(['w', 'a'], press_time)
    elif direction == 'topRight':
        press_keys(['w', 'd'], press_time)
    elif direction == 'downLeft':
        press_keys(['s', 'a'], press_time)
    elif direction == 'downRight':
        press_keys(['s', 'd'], press_time)


def buff(keys):
    for key in keys:
        press_key(key, 0.5)


def skill(key, cast_type, distance=None):
    if cast_type == 'click':
        # 直接点击类型
        press_key(key, 0.5)
    elif cast_type == 'slide_release':
        # 滑动释放类型  鼠标操作
        x, y = 1, 1
        if distance == 'top':
            x_offset, y_offset = 0, -1
        elif distance == 'down':
            x_offset, y_offset = 0, 1
        elif distance == 'left':
            x_offset, y_offset = -1, 0
        elif distance == 'right':
            x_offset, y_offset = 1, 0
        else:
            x_offset, y_offset = 0, 0
        click_and_drag(x, y, x_offset, y_offset, 0.5)


def normal_attack(self, times):
    for _ in range(times):
        press_key('M', 0.5)


def again(self):
    single_click(0, 0)


def opened_reward():
    single_click(0, 0)
