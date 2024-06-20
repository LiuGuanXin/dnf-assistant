import time
import dnf.Operate as op
import numpy as np
import FrameDeal as fd
import RoomPredict as rp

current_room_number = 1


def move_to_cord(self_cord, dest_cord):
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


def existence_need_door(self_cord, open_door_cord, direction):
    return False


def path_route(img) -> str:
    # 根据 亮度 通过opencv 识别出来路径 转化为二维数组
    # 获取当前位置  boss 位置
    # 考虑时空怪房间
    return "up"


# 移动到下一房间
def fixation():
    num_direct = {
        1: "up",
        2: "down",
        3: "left",
        4: "right"
    }
    return num_direct[current_room_number]


def get_next_door_direction(thumbnail_map_cord, path_type):
    x, y = thumbnail_map_cord

    if path_type == 0:
        op.single_click(x, y)
        # 目前已经打开了大地图 获取大地图的截图
        img = fd.screenshot(0, 0, 1920, 1080)
        direction = rp.predict_room(img)
    elif path_type == 1:
        op.single_click(x, y)
        # 目前已经打开了大地图 获取大地图的截图
        img = fd.screenshot(0, 0, 1920, 1080)
        direction = path_route(img)
    else:
        direction = fixation()
    return direction


def move_next(self_cord, open_door_cord, thumbnail_map_cord):
    direction = get_next_door_direction(thumbnail_map_cord, 0)
    # 寻找下一房间的门的位置
    i = 10
    while i:
        # 判断对应方向的门是否存在于屏幕中
        if existence_need_door(self_cord, open_door_cord, direction):
            move_to_cord(self_cord, open_door_cord)
            break
        else:
            # 首先移动到屏幕中央移动，再朝着预测的方向移动
            x, y, w, h = fd.get_default_region()
            x_center, y_center = x + w / 2, y + h / 2
            move_to_cord(self_cord, (x_center, y_center))
            op.move(direction, 100)
            i -= 1
