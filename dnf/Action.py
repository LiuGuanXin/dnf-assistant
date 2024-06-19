import time

import dnf.Operate as op
import numpy as np


# 定义多个指定区域（使用左上角和右下角的坐标）
regions = [
    ((50, 50), (150, 150)),
    ((200, 200), (300, 300))
]
# 与上面的区域定义对应，定义技能级别
skill_class = {
    1 : "h",
    2 : 'j'
}

def calculate_average_brightness(image, top_left, bottom_right):
    # 提取指定区域
    region = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    # 计算平均亮度
    average_brightness = np.mean(region)
    return average_brightness

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

# 攻击
def attack(self_cord, monster_cord, img):
    # 移动到边缘测稍等 为了让怪物聚集
    # 获取怪物中心的坐标 和 最左侧怪物的坐标
    left_x_min = monster_cord[0][0]
    left_y_min = monster_cord[0][1]
    x_mean = 0
    for idx, item in enumerate(monster_cord):
        if item[0] < left_x_min:
            left_x_min = item[0]
            left_y_min = item[1]
        x_mean += item[0]
    x_mean = x_mean / len(monster_cord)
    move_to_cord(self_cord, (left_x_min, left_y_min))

    # 判断是否怪物在攻击范围内
    if (abs(self_cord[0] - left_x_min) < 100
            and abs(self_cord[1] - left_y_min) < 100):
        # 攻击怪物
        # 如何攻击？ 普攻 + 技能的方式
        # 根据图片检测技能的cd
        # 根据当前输入图片的的坐标判断各个技能的位置
        # 使用opencv 检测指定区域的图片亮度 亮度低的地方技能未cd
        # 存储的可以释放的技能
        current_skill = dict()
        # 计算每个指定区域的平均亮度
        idx: int
        for idx, ((x1, y1), (x2, y2)) in enumerate(regions):
            avg_brightness = calculate_average_brightness(img, (x1, y1), (x2, y2))
            # 判断技能是否cd
            if avg_brightness > 100:
                current_skill.setdefault(idx, skill_class.get(idx))
        op.normal_attack(3)
        # 根据怪物数量选择技能

        # 调整面对方向 面朝怪物的方向
        if self_cord[0] >= x_mean:
            op.move("left",5)
        else:
            op.move("right",5)

        # 释放技能
        serial_list = current_skill.keys()
        random_skill = np.random.choice(list(serial_list))
        op.skill(current_skill[random_skill], "normal")
        time.sleep(1)
        op.normal_attack(3)

# 移动到下一房间
def move_next(self_cord, open_door_cord):
    # open_door_cord 是个列表 如何判断走哪个门？
    # 如果是固定某个地图可以记录房间，直接写死
    # 判断门的位置 控制移动
    x_direction = open_door_cord[0][0] - self_cord[0]
    # 判断移动方向
    if x_direction > 0:
        direction = "right"
    else:
        direction = "left"
    op.move(direction, x_direction)
    # 计算移动的距离
    y_direction = open_door_cord[0][0] - self_cord[1]
    # 判断移动方向
    if y_direction > 0:
        direction = "down"
    else:
        y_direction = "up"
    op.move(direction, y_direction)

