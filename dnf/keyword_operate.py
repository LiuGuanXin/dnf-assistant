import pyautogui
import time
import math
from tools.image_detect import get_cd_skill


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


def move(direction, input_time: float = 0):
    # 根据距离计算按压时间
    press_time = 0.1
    if input_time != 0:
        press_time = input_time
    # 八方向a
    if direction == 'up':
        press_key('up', press_time)
    elif direction == 'down':
        press_key('down', press_time)
    elif direction == 'left':
        press_key('left', press_time)
    elif direction == 'right':
        press_key('right', press_time)
    elif direction == 'topLeft':
        press_keys(['up', 'left'], press_time)
    elif direction == 'topRight':
        press_keys(['up', 'right'], press_time)
    elif direction == 'downLeft':
        press_keys(['down', 'left'], press_time)
    elif direction == 'downRight':
        press_keys(['down', 'right'], press_time)


def four_move(self_cord, dest_cord):
    # 移动 分别从 x 轴和 y 轴移动
    # 计算移动的距离
    x_direction = dest_cord[0] - self_cord[0]
    # 判断移动方向
    if x_direction > 0:
        direction = "right"
    else:
        direction = "left"
    move(direction)
    # 计算移动的距离
    y_direction = dest_cord[1] - self_cord[1]
    # 判断移动方向
    if y_direction > 0:
        direction = "down"
    else:
        direction = "up"
    move(direction)


def eight_move(self_cord, dest_cord, input_time: float = 0):
    # 计算x轴差异
    x_direction = dest_cord[0] - self_cord[0]
    # 计算y轴差异
    y_direction = dest_cord[1] - self_cord[1]
    # 计算角度
    angle = math.degrees(math.atan(abs(y_direction / x_direction)))
    # 判断移动方向
    if x_direction > 0 and y_direction > 0:
        if 0 <= angle < 30:
            move("right", input_time)
            print("向右移动")
        elif 30 <= angle <= 60:
            move("downRight", input_time)
            print("向右下移动")
        elif 60 < angle <= 90:
            move("down", input_time)
            print("向下移动")
    elif x_direction > 0 > y_direction:
        if 0 <= angle < 30:
            move("right", input_time)
            print("向右移动")
        elif 30 <= angle <= 60:
            move("topRight", input_time)
            print("向右上移动")
        elif 60 < angle <= 90:
            move("up", input_time)
            print("向右上移动")
    elif x_direction < 0 < y_direction:
        if 0 <= angle < 30:
            move("left", input_time)
            print("向左移动")
        elif 30 <= angle <= 60:
            move("downLeft", input_time)
            print("向左下移动")
        elif 60 < angle <= 90:
            move("down", input_time)
            print("向下移动")
    elif x_direction < 0 and y_direction < 0:
        if 0 <= angle < 30:
            move("left", input_time)
            print("向左移动")
        elif 30 <= angle <= 60:
            move("topLeft", input_time)
            print("向左上移动")
        elif 60 < angle <= 90:
            move("up", input_time)
            print("向上移动")


def buff_skill(skill_max_lighting):
    # 获取可使用技能
    current_skill_list = get_cd_skill(1, skill_max_lighting)
    if len(current_skill_list) > 0:
        for sk in current_skill_list:
            if "W" == sk:
                press_key(sk, 1)
            elif "E" == sk:
                press_key(sk, 0.2)


def skill(key, cast_type, direction=None):
    if cast_type == 'click':
        # 直接点击类型
        press_key(key, 1)
    elif cast_type == 'slide_release':
        # 滑动释放类型  鼠标操作
        x, y = 1, 1
        if direction == 'top':
            x_offset, y_offset = 0, -1
        elif direction == 'down':
            x_offset, y_offset = 0, 1
        elif direction == 'left':
            x_offset, y_offset = -1, 0
        elif direction == 'right':
            x_offset, y_offset = 1, 0
        else:
            x_offset, y_offset = 0, 0
        click_and_drag(x, y, x_offset, y_offset, 0.5)


def dodge():
    press_key('C', 0.2)


def normal_attack(times):
    for _ in range(times):
        press_key('X', 0.3)


def again():
    single_click(0, 0)


def opened_reward():
    single_click(0, 0)
