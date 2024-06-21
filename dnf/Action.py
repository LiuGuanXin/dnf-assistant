import time
import dnf.Operate as op
import numpy as np
import FrameDeal as fd
import RoomPredict as rp
from YoloPredict import YoloPredict
import math

current_room_number = 1
devi = 10


def move_to_cord(self_cord, dest_cord, model: YoloPredict = None, direction_type=0):
    while True:
        if model is not None:
            x, y, w, h = fd.get_default_region()
            model.predict_img(fd.screenshot(x, y, w, h))
            self_cord = model.get_self_cord()
            line_distance = math.sqrt((dest_cord[0] - self_cord[0]) ** 2 + (dest_cord[1] - self_cord[1]) ** 2)
            if line_distance < devi:
                break
        # 四方向操作
        if direction_type == 0:
            # 分两步移动 分别从 x 轴和 y 轴移动
            # 计算移动的距离
            x_direction = dest_cord[0] - self_cord[0]
            # 判断移动方向
            if x_direction > 0:
                direction = "right"
            else:
                direction = "left"
            op.move(direction, x_direction)
            # 计算移动的距离
            y_direction = dest_cord[1] - self_cord[1]
            # 判断移动方向
            if y_direction > 0:
                direction = "down"
            else:
                y_direction = "up"
            op.move(direction, y_direction)
        # 八方向操作
        elif direction_type == 1:
            # 计算x轴差异
            x_direction = dest_cord[0] - self_cord[0]
            # 计算y轴差异
            y_direction = dest_cord[1] - self_cord[1]
            # 短轴对角线距离
            if abs(x_direction) > abs(y_direction):
                diagonal = abs(y_direction)
            else:
                diagonal = abs(x_direction)
            # 判断移动方向
            if x_direction > 0 and y_direction > 0:
                op.move("downRight", diagonal)
                if abs(x_direction - y_direction) > 0:
                    op.move("right", abs(x_direction - y_direction))
                else:
                    op.move("down", abs(x_direction - y_direction))
            elif x_direction > 0 > y_direction:
                op.move("topLeft", diagonal)
                if abs(x_direction - y_direction) > 0:
                    op.move("left", abs(x_direction - y_direction))
                else:
                    op.move("up", abs(x_direction - y_direction))
            elif x_direction < 0 < y_direction:
                op.move("topRight", diagonal)
                if abs(x_direction - y_direction) > 0:
                    op.move("right", abs(x_direction - y_direction))
                else:
                    op.move("up", abs(x_direction - y_direction))
            elif x_direction < 0 and y_direction < 0:
                op.move("downLeft", diagonal)
                if abs(x_direction - y_direction) > 0:
                    op.move("left", abs(x_direction - y_direction))
                else:
                    op.move("down", abs(x_direction - y_direction))
        if model is not None:
            break


# 捡材料
def pick_material(self_cord, material_cord):
    for material in material_cord:
        move_to_cord(self_cord, material)


def gather_monster(self_cord, monster_cord):
    left_x_min = monster_cord[0][0]
    left_y_min = monster_cord[0][1]
    for idx, item in enumerate(monster_cord):
        if item[0] < left_x_min:
            left_x_min = item[0]
            left_y_min = item[1]
    move_to_cord(self_cord, (left_x_min, left_y_min))


# 攻击
def attack(self_cord, monster_cord):
    # 移动到边缘测稍等 为了让怪物聚集
    # 获取怪物中心的坐标 和 最左侧怪物的坐标
    left_x_min = monster_cord[0][0]
    left_y_min = monster_cord[0][1]
    x_mean = sum(monster_cord[:][0]) / len(monster_cord)
    # 判断是否怪物在攻击范围内
    if (abs(self_cord[0] - left_x_min) < 100
            and abs(self_cord[1] - left_y_min) < 100):
        # 攻击怪物
        # 如何攻击？ 普攻 + 技能的方式
        op.normal_attack(3)
        # 根据怪物数量选择技能
        # 调整面对方向 面朝怪物的方向
        if self_cord[0] >= x_mean:
            op.move("left", 5)
        else:
            op.move("right", 5)
        # 获取可使用技能
        current_skill = fd.get_cd_skill()
        # 释放技能
        serial_list = current_skill.keys()
        random_skill = np.random.choice(list(serial_list))
        op.skill(current_skill[random_skill], "normal")
        time.sleep(1)
        op.normal_attack(3)


def existence_need_door(open_door_cord, direction):
    center_cord = fd.get_default_region()
    door_dict = dict()
    for door in open_door_cord:
        if door[0] - center_cord[0] > 0 and door[1] - center_cord[1] > 0:
            door_dict["up"] = door
        elif door[0] - center_cord[0] < 0 and door[1] - center_cord[1] < 0:
            door_dict["down"] = door
        elif door[0] - center_cord[0] > 0 > door[1] - center_cord[1]:
            door_dict["left"] = door
        else:
            door_dict["right"] = door
    if direction in door_dict.keys():
        return True
    else:
        return False


def path_route(img) -> str:
    # 根据 亮度 通过opencv 识别出来路径 转化为二维数组

    # 获取当前位置  boss 位置
    # 考虑时空怪房间
    return "up"


"""房间对应应该进入的门"""
num_direct = {
    1: "up",
    2: "down",
    3: "left",
    4: "right"
}


# 移动到下一房间
def fixation():
    global current_room_number
    next_door_direction = num_direct[current_room_number]
    current_room_number += 1
    if current_room_number >= len(num_direct):
        current_room_number = 1
    return next_door_direction


def get_next_door_direction(thumbnail_map_cord, path_type):
    x, y = thumbnail_map_cord
    if path_type == 0:
        op.single_click(x, y)
        # 目前已经打开了大地图 获取大地图的截图
        x_m, y_m, w_m, h_m = fd.get_map_region()
        img = fd.screenshot(x_m, y_m, w_m, h_m)
        direction = rp.predict_room(img)
    elif path_type == 1:
        op.single_click(x, y)
        x_m, y_m, w_m, h_m = fd.get_map_region()
        img = fd.screenshot(x_m, y_m, w_m, h_m)
        direction = path_route(img)
    else:
        direction = fixation()
    return direction


def move_next(self_cord, open_door_cord, thumbnail_map_cord, model: YoloPredict):
    direction = get_next_door_direction(thumbnail_map_cord, 0)
    # 寻找下一房间的门的位置
    # 1 检验屏幕是否有需要的门
    if existence_need_door(open_door_cord, direction):
        move_to_cord(self_cord, open_door_cord)
        return
    # 2 没有移动到屏幕中央  检测有没有门
    x, y, w, h = fd.get_default_region()
    x_center, y_center = x + w / 2, y + h / 2
    move_to_cord(self_cord, (x_center, y_center))
    model.predict_img(fd.screenshot(x, y, w, h))
    if existence_need_door(model.get_open_door_cord(), direction):
        move_to_cord(self_cord, open_door_cord)
        return
    # 3 没有接着向门的方向移动  循环检测 直到检测到后移动至门内
    i = 10
    while i:
        model.predict_img(fd.screenshot(x, y, w, h))
        # 判断对应方向的门是否存在于屏幕中
        if existence_need_door(model.get_open_door_cord(), direction):
            move_to_cord(self_cord, open_door_cord)
            break
        else:
            # 朝着预测的方向移动
            op.move(direction, 100)
            i -= 1
