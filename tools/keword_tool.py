import pyautogui
import time


def press_key(key, press_time):
    """按下并释放单个按键，并设置按压时间"""
    pyautogui.keyDown(key)
    time.sleep(float(abs(press_time)))
    pyautogui.keyUp(key)


def press_keys(keys, press_time):
    """按下并释放多个按键，并设置按压时间"""
    for key in keys:
        pyautogui.keyDown(key)
    time.sleep(float(press_time))
    for key in keys:
        pyautogui.keyUp(key)


def single_click(x, y):
    """在指定坐标进行单击"""
    pyautogui.click(x, y)
    time.sleep(0.2)


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
