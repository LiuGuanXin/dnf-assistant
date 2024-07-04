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
        self_c, _, _, open_door = model.get_cord()
        if len(self_c) > 0 and len(open_door) > 0:
            while True:
                print("移动到下一个房间")
                print("当前是第" + str(current_room_number) + "个房间")
                self_cord, monster_cord, _, open_door = model.get_cord()
                close_door_cord = model.get_monster_cord()
                if len(close_door_cord) > 0 or len(monster_cord) > 0 or is_black():
                    print("已经移动到下一个房间了")
                    current_room_number += 1
                    print("当前房间序号：" + str(current_room_number))
                    if current_room_number >= len(num_direct):
                        current_room_number = 1
                    self_cord, monster_cord, _, open_door = model.get_cord()
                    if len(self_cord) > 0:
                        op.move_to_dest(self_cord, fd.get_center_cord())
                    break
                # fd.get_thumbnail_map()
                direct = get_next_door_direction(None, 0)
                print("下一个房间门的方向：" + direct)
                next_door_cord = existence_need_door(open_door, direct)
                print("是否存在可以进入的房间" + str(len(next_door_cord) != 0))
                if len(next_door_cord) == 0 and len(self_cord) > 0:
                    # 移动寻找门
                    print("不存在可以进入的房间，移动寻找")
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
            print("走位拉怪")
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
            # 连续五次没检测到则退出
            if (len(material_cord) == 0 or len(monster_cord) > 0
                    or len(close_door_cord) == 0):
                if times > 3:
                    break
                else:
                    times += 1
            else:
                times = 0
            print("捡材料")
            if len(self_cord) > 0 and len(material_cord) > 0:
                op.move_to_dest(self_cord, material_cord[0])

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
                op.move("right", 0.05)
                self.use_random_skill()
            elif right_num > num_threshold:
                op.move("left", 0.05)
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
                    # 如何攻击？ 普攻 + 技能的方式
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


def get_direction(x, y) -> str:
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


def existence_need_door(open_door_cord, direction) -> []:
    door_dict = dict()
    for door in open_door_cord:
        direct = get_direction(door[0], door[1])
        door_dict[direct] = door
    if direction in door_dict.keys():
        return door_dict[direction]
    else:
        return []


room_class_array = []


def ana_brightness(image):
    r_brightness = image[:, :, 0]
    g_brightness = image[:, :, 1]
    b_brightness = image[:, :, 2]
    t_brightness = (image[:, :, 0] + image[:, :, 1] + image[:, :, 2]) / 3
    return t_brightness, r_brightness, g_brightness, b_brightness


def path_route(img) -> str:
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
    return direction


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
    return next_door_direction


def get_next_door_direction(mag_img, path_type):
    if path_type == 1:
        direction = path_route(mag_img)
    else:
        direction = fixation()
    return direction


def is_black():
    x_center, y_center = fd.get_center_cord()
    frame = fd.screenshot(x_center - 100, y_center - 100, 200, 200)
    total = np.mean(np.array(frame))
    if total < 20:
        return True
    else:
        return False
