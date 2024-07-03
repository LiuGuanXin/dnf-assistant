from tools.keword_tool import single_click
from tools.keword_tool import click_and_drag
import math
import time
from tools.keword_tool import press_key
from tools.keword_tool import press_keys
import tools.adb_tool as at
from tools.image_detect import get_cd_skill

move_wheel_cord = []

skill_cord = {

}

buff_skill_cord = {

}

x_skill_cord = []


def move_to_dest(self_cord, dest_cord, input_time: float = 0):
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


def move(direction, input_time: float = 0, operate_type: int = 0):
    # 根据距离计算按压时间
    press_time = 0.1
    if input_time != 0:
        press_time = input_time
        # adb操作
    if operate_type == 1:
        x, y = move_wheel_cord
        at.move(direction, x, y, press_time)
    else:
        direction_dict = {
            'topLeft': ['up', 'left'],
            'topRight': ['up', 'right'],
            'downLeft': ['down', 'left'],
            'downRight': ['down', 'right']
        }
        # 键盘操作
        if direction == 'up' or direction == 'down' or direction == 'left' or direction == 'right':
            press_key(direction, press_time)
        else:
            press_keys(direction_dict[direction], press_time)


def skill(key, cast_type, direction=None, operate_type: int = 0):
    if operate_type == 0:
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
    else:
        if cast_type == 'click':
            x, y = skill_cord[key]
            at.tap_screen_time(x, y, 1)
        elif cast_type == 'slide_release':
            x, y, x_offset, y_offset = skill_cord[key]
            at.swipe_screen(x, y, x + x_offset, y + y_offset, 0.3)


def buff_skill(skill_max_lighting, operate_type: int = 0):
    if operate_type == 0:
        # 获取可使用技能
        current_skill_list = get_cd_skill(1, skill_max_lighting)
        if len(current_skill_list) > 0:
            for sk in current_skill_list:
                if "W" == sk:
                    press_key(sk, 1)
                elif "E" == sk:
                    press_key(sk, 0.2)
    else:
        for item in buff_skill_cord:
            x_cord, y_cord, t_cord = buff_skill_cord[item]
        at.tap_screen_time(x_cord, y_cord, t_cord)
        time.sleep(0.3)


def dodge(operate_type: int = 0):
    if operate_type == 0:
        press_key('C', 0.2)
    else:
        x, y = [1, 1]
        at.tap_screen_time(x, y, 100)


def normal_attack(times, operate_type: int = 0):
    for _ in range(times):
        if operate_type == 0:
            press_key('X', 0.3)
        else:
            x, y = x_skill_cord
            at.tap_screen_time(x, y, 100)
            time.sleep(0.1)


def again():
    single_click(0, 0)


def opened_reward():
    single_click(0, 0)
