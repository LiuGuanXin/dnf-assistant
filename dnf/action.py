import time

import dnf.operate as op
import tools.image_deal as fd
from tools.yolo import YoloPredict
import math
import numpy as np
from tools.image_detect import get_cd_skill

current_room_number = 1
devi = 300


class action:
    def __init__(self, model: YoloPredict, skill_max_lighting):
        self.skill_max_lighting = skill_max_lighting
        self.model = model

    def move_next_room(self):
        model = self.model
        global current_room_number
        self_c, _, _, x_door, y_door = model.get_cord()
        if len(self_c) > 0 and (len(x_door) > 0 or len(y_door) > 0):
            while True:
                print("move to next room")
                print("The current room is the " + str(current_room_number) + "st room")
                self_cord, monster_cord, _, x_door, y_door = model.get_cord()
                close_door_cord = model.get_monster_cord()
                if len(close_door_cord) > 0 or len(monster_cord) > 0 or is_black():
                    print("I've moved to the next room")
                    current_room_number += 1
                    print("The current room number：" + str(current_room_number))
                    if current_room_number >= len(num_direct):
                        current_room_number = 1
                    self_cord, monster_cord, _, _, _ = model.get_cord()
                    for _ in range(10):
                        if is_black():
                            time.sleep(0.3)
                    if len(self_cord) > 0:
                        op.move_to_dest(self_cord, fd.get_center_cord(), 0.2)
                    break
                direct, total_number = get_next_door_direction(0)
                print("The number of rooms：" + str(total_number))
                print("next room direction：" + direct)
                next_door_cord = existence_need_door(x_door, y_door, self_cord, direct)
                print("Whether there is a room that can be entered" + str(len(next_door_cord) != 0))
                if len(next_door_cord) == 0 and len(self_cord) > 0:
                    # 移动寻找门
                    print("There is no room to enter, move to find")
                    op.move_to_dest(self_cord, fd.get_center_cord(), 0.1)
                    continue
                if len(self_cord) > 0 and len(next_door_cord) > 0:
                    x_pais = abs(next_door_cord[0] - self_cord[0])
                    y_pais = abs(next_door_cord[1] - self_cord[1])

                    if x_pais < 50 and y_pais < 50:
                        # 已经在附近但是进不去门，需要重新进一下试试
                        pass
                    op.move_to_dest(self_cord, next_door_cord)

    def gather_monster_move(self):
        model = self.model
        while True:
            print("move to monster")
            model.predict_img(fd.get_default_img())
            self_cord = model.get_self_cord()
            dest_cord = model.get_left_monster()
            if len(dest_cord) == 0:
                break
            if len(self_cord) > 0 and len(dest_cord) > 0:
                if break_condition(self_cord, dest_cord):
                    break
                op.move_to_dest(self_cord, dest_cord)

    # 捡材料
    def pick_material(self):
        model = self.model
        times = 0
        while True:
            model.predict_img(fd.get_default_img())
            self_cord = model.get_self_cord()
            material_cord = model.get_material_cord()
            monster_cord = model.get_monster_cord()
            close_door_cord = model.get_close_door_cord()
            # 连续3次没检测到则退出
            if len(material_cord) == 0 or len(monster_cord) > 0 or len(close_door_cord) == 0:
                if times > 3:
                    # 检测不到材料 判断是否进入了结束界面  如何判断？
                    # 点击下一局  弹窗则点击不再提醒 确定
                    # 检测是否进入到了新房间，重置房间编号
                    break
                else:
                    times += 1
            else:
                times = 0
            print("move to material")
            if len(self_cord) > 0 and len(material_cord) > 0:
                op.move_to_dest(self_cord, material_cord[0])

    def use_buff_skill(self):
        # 获取可使用技能
        current_skill_list = get_cd_skill(1, self.skill_max_lighting)
        if "W" in current_skill_list:
            op.skill("W", "click")
        if "E" in current_skill_list:
            op.skill("E", "click")

    def use_random_skill(self):
        # 获取可使用技能
        current_skill_list = get_cd_skill(1, self.skill_max_lighting)
        op.dodge()
        # 释放技能
        if len(current_skill_list) > 0:
            random_skill = np.random.choice(current_skill_list)
            op.skill(random_skill, "click")

    # 攻击
    def attack(self):
        model = self.model
        model.predict_img(fd.get_default_img())
        self_cord = model.get_self_cord()
        monster_cord = model.get_monster_cord()
        if len(self_cord) > 0 and len(monster_cord) > 0:
            num_threshold = 4
            # 判断左侧和右侧的怪物数量
            left_num, right_num = 0, 0
            for monster in monster_cord:
                if monster[0] < self_cord[0]:
                    left_num += 1
                else:
                    right_num += 1
            # 如果数量多于一定的值
            if left_num > num_threshold:
                op.move("left", 0.05)
                self.use_random_skill()
            elif right_num > num_threshold:
                op.move("right", 0.05)
                self.use_random_skill()
            else:
                # 如果数量少于一定的值 获取离自己最近的怪物坐标
                x_min, y_min = get_min_monster(self_cord, monster_cord)
                # 判断是否怪物在普攻范围内
                if (abs(self_cord[0] - x_min) < 300
                        and abs(self_cord[1] - y_min) < 150):
                    if self_cord[0] <= x_min:
                        op.move("right", 0.05)
                    else:
                        op.move("left", 0.05)
                    op.normal_attack(3)


def break_condition(self_cord, dest_cord):
    x_pais = abs(dest_cord[0] - self_cord[0])
    y_pais = abs(dest_cord[1] - self_cord[1])
    if x_pais < 200 and y_pais < 150:
        return True
    else:
        return False


# 获取离自己最近的对象坐标
def get_min_monster(self_cord, monster_list):
    min_monster = monster_list[0]
    min_distance = math.sqrt((abs(self_cord[0]) - abs(min_monster[0])) ** 2
                             + (abs(self_cord[1]) - abs(min_monster[1])) ** 2)
    for monster in monster_list:
        dis = math.sqrt((abs(self_cord[0]) - abs(monster[0])) ** 2
                        + (abs(self_cord[1]) - abs(monster[1])) ** 2)
        if dis < min_distance:
            min_distance = dis
            min_monster = monster
    return min_monster


# 根据顶点对角线来划分上下左右
def get_direction_by_diagonal(x, y) -> str:
    _, _, w, h = fd.get_default_region()
    # 计算点到对角线1的y值
    y1 = (h / w) * x
    # 计算点到对角线2的y值
    y2 = (-h / w) * x + h

    if y < y1 and y < y2:
        return "up"
    elif y > y1 and y > y2:
        return "down"
    elif y1 < y < y2:
        return "left"
    else:
        return "right"


# 根据中心点十字划分上下左右
def get_direction(x, y) -> str:
    x_, y_, _, _ = fd.get_default_region()
    if y < y_:
        return "up"
    elif y > y_:
        return "down"
    elif x < x_:
        return "left"
    elif x > x_:
        return "right"


def existence_need_door(x_door, y_door, self_cord, direction) -> []:
    door_dict = dict()
    if (direction == "left" or direction == "right") and len(x_door) > 0:
        for door in x_door:
            if self_cord[0] > door[0]:
                door_dict["left"] = door
            else:
                door_dict["right"] = door
    elif (direction == "up" or direction == "down") and len(y_door) > 0:
        for door in y_door:
            if self_cord[0] > door[0]:
                door_dict["up"] = door
            else:
                door_dict["down"] = door
    return door_dict[direction]


room_class_array = []


def ana_brightness(image):
    r_brightness = image[:, :, 0]
    g_brightness = image[:, :, 1]
    b_brightness = image[:, :, 2]
    t_brightness = (image[:, :, 0] + image[:, :, 1] + image[:, :, 2]) / 3
    return t_brightness, r_brightness, g_brightness, b_brightness


def path_route(img) -> tuple[str, int]:
    global room_class_array
    # if img is None:
    #     return room_class_array[current_room_number]
    # 根据 亮度 通过opencv 识别出来路径 转化为二维数组
    if len(room_class_array) == 0:
        # 示例使用
        num_splits_x = 5  # x轴方向切分数
        num_splits_y = 4  # y轴方向切分数
        room_class_array = fd.split_image_and_calculate_brightness(img, num_splits_x, num_splits_y)
    # 路线规划
    direct_list = fd.shortest_path_directions(room_class_array)
    global current_room_number
    direction = direct_list[current_room_number]
    current_room_number += 1
    if current_room_number > len(num_direct) + 1:
        current_room_number = 1
        room_class_array = []
    return direction, len(direct_list)


"""房间对应应该进入的门"""
num_direct = {
    1: "up",
    2: "right",
    3: "right",
    4: "down",
    5: "right",
    6: "right",
    7: "left",
    8: "up",
    9: "right"
}


# 移动到下一个房间
def fixation():
    global current_room_number
    next_door_direction = num_direct[current_room_number]
    return next_door_direction, len(num_direct)


def get_next_door_direction(path_type):
    if path_type == 1:
        direction, total_number = path_route(fd.get_thumbnail_map())
    else:
        direction, total_number = fixation()
    return direction, total_number


def is_black():
    x_center, y_center = fd.get_center_cord()
    frame = fd.screenshot(x_center - 100, y_center - 100, 200, 200)
    total = np.mean(np.array(frame))
    print("当前的亮度为：" + str(total))
    if total < 20:
        return True
    else:
        return False


def rechallenge(cord):
    global current_room_number
    op.single_click(cord[0], cord[1])
    current_room_number = 1


def confirm_challenge(select_cord, confirm_cord):
    global current_room_number
    op.single_click(select_cord[0], select_cord[1])
    time.sleep(1)
    op.single_click(confirm_cord[0], confirm_cord[1])
    current_room_number = 1
