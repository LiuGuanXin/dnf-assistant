import dnf.keword_operate as op
from collections import deque
import tools.image_deal as fd
from tools.yolo import YoloPredict
import math
import numpy as np

from tools.image_detect import get_cd_skill

current_room_number = 1
devi = 300


def four_move(self_cord, dest_cord):
    # 移动 分别从 x 轴和 y 轴移动
    # 计算移动的距离
    x_direction = dest_cord[0] - self_cord[0]
    # 判断移动方向
    if x_direction > 0:
        direction = "right"
    else:
        direction = "left"
    op.move(direction)
    # 计算移动的距离
    y_direction = dest_cord[1] - self_cord[1]
    # 判断移动方向
    if y_direction > 0:
        direction = "down"
    else:
        direction = "up"
    op.move(direction)


def eight_move(self_cord, dest_cord, input_time=0):
    # 计算x轴差异
    x_direction = dest_cord[0] - self_cord[0]
    # 计算y轴差异
    y_direction = dest_cord[1] - self_cord[1]
    # 计算角度
    angle = math.degrees(math.atan(abs(y_direction / x_direction)))
    # 判断移动方向
    if x_direction > 0 and y_direction > 0:
        if 0 <= angle < 30:
            op.move("right", input_time)
            print("向右移动")
        elif 30 <= angle <= 60:
            op.move("downRight", input_time)
            print("向右下移动")
        elif 60 < angle <= 90:
            op.move("down", input_time)
            print("向下移动")
    elif x_direction > 0 > y_direction:
        if 0 <= angle < 30:
            op.move("right", input_time)
            print("向右移动")
        elif 30 <= angle <= 60:
            op.move("topRight", input_time)
            print("向右上移动")
        elif 60 < angle <= 90:
            op.move("up", input_time)
            print("向右上移动")
    elif x_direction < 0 < y_direction:
        if 0 <= angle < 30:
            op.move("left", input_time)
            print("向左移动")
        elif 30 <= angle <= 60:
            op.move("downLeft", input_time)
            print("向左下移动")
        elif 60 < angle <= 90:
            op.move("down", input_time)
            print("向下移动")
    elif x_direction < 0 and y_direction < 0:
        if 0 <= angle < 30:
            op.move("left", input_time)
            print("向左移动")
        elif 30 <= angle <= 60:
            op.move("topLeft", input_time)
            print("向左上移动")
        elif 60 < angle <= 90:
            op.move("up", input_time)
            print("向上移动")


def break_condition(self_cord, dest_cord):
    x_pais = abs(dest_cord[0] - self_cord[0])
    y_pais = abs(dest_cord[1] - self_cord[1])
    if x_pais < 200 and y_pais < 150:
        return True
    else:
        return False


def gather_monster_move(model, direction_type=1):
    while True:
        print("走位拉怪")
        x, y, w, h = fd.get_default_region()
        img = fd.screenshot(x, y, w, h)
        model.predict_img(img)
        self_cord = model.get_self_cord()
        dest_cord = model.get_left_monster()
        if len(dest_cord) == 0:
            break
        if len(self_cord) > 0 and len(dest_cord) > 0:
            if break_condition(self_cord, dest_cord):
                break
            # 四方向操作
            if direction_type == 0:
                four_move(self_cord, dest_cord)
            # 八方向操作
            elif direction_type == 1:
                eight_move(self_cord, dest_cord)


# 捡材料
def pick_material(model: YoloPredict):
    times = 0
    while True:
        x, y, w, h = fd.get_default_region()
        model.predict_img(fd.screenshot(x, y, w, h))
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
            eight_move(self_cord, material_cord[0])


def buff_skill(skill_max_lighting):
    # 获取可使用技能
    current_skill_list = get_cd_skill(1, skill_max_lighting)
    if len(current_skill_list) > 0:
        for skill in current_skill_list:
            if "W" == skill:
                op.press_key(skill, 4)
            elif "E" == skill:
                op.press_key(skill, 0.2)


flag = 0


# 攻击
def attack(model: YoloPredict, skill_max_lighting):
    x, y, w, h = fd.get_default_region()
    model.predict_img(fd.screenshot(x, y, w, h))
    self_cord = model.get_self_cord()
    monster_cord = model.get_monster_cord()
    if len(self_cord) > 0 and len(monster_cord) > 0:
        # 获取怪物中心的坐标 和 最左侧怪物的坐标
        left_x_min, left_y_min = model.get_left_monster()
        x_mean = sum(monster_cord[:][0]) / len(monster_cord)
        # 判断是否怪物在攻击范围内
        if (abs(self_cord[0] - left_x_min) < 200
                and abs(self_cord[1] - left_y_min) < 200):
            # 调整
            # 攻击怪物
            # 如何攻击？ 普攻 + 技能的方式
            op.normal_attack(3)
            # 根据怪物数量选择技能
            # 调整面对方向 面朝怪物的方向
            if self_cord[0] >= x_mean:
                op.press_key("right", 0.05)
            else:
                op.press_key("left", 0.05)
            # 获取可使用技能
            current_skill_list = get_cd_skill(1, skill_max_lighting)
            # 释放技能
            if len(current_skill_list) > 0:
                random_skill = np.random.choice(current_skill_list)
                op.skill(random_skill, "click")


def get_direction(px, py, x, y) -> str:
    dx = x - px
    dy = y - py
    if abs(dx) > abs(dy):
        if dx > 0:
            return 'right'
        else:
            return 'left'
    else:
        if dy > 0:
            return 'up'
        else:
            return 'down'


def existence_need_door(open_door_cord, direction) -> []:
    _, _, w, h = fd.get_default_region()
    door_dict = dict()
    for door in open_door_cord:
        direction = get_direction(door[0], door[1], int(w / 2), int(h / 2))
        door_dict[direction] = door
    if direction in door_dict.keys():
        return door_dict[direction]
    else:
        return []


def shortest_path_directions(grid, must_pass=None):
    if grid.size == 0:
        return []

    rows, cols = grid.shape
    directions = [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]  # 上下左右四个方向

    # 找到起点和终点的位置
    start = tuple(np.argwhere(grid == 2)[0])
    end = tuple(np.argwhere(grid == 3)[0])

    if not start or not end:
        return []

    queue = deque([(start[0], start[1], [])])  # 队列中存储 (row, col, path)
    visited = set()
    visited.add(start)

    # 如果有必经点，将其添加到访问集合中
    if must_pass:
        for point in must_pass:
            visited.add(tuple(point))

    while queue:
        r, c, path = queue.popleft()

        # 如果到达终点，返回当前路径
        if (r, c) == end:
            return path

        # 否则，继续向四个方向扩展
        for dr, dc, dir_name in directions:
            nr, nc = r + dr, c + dc

            # 检查边界和是否访问过
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if grid[nr, nc] != 0 and grid[nr, nc] != 4:
                    visited.add((nr, nc))
                    new_path = path + [dir_name]
                    queue.append((nr, nc, new_path))

    # 如果无法到达终点，返回空列表
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
    direct_list = shortest_path_directions(room_class_array)
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


def get_min_door(self_cord, open_door_list: list) -> []:
    min_door = open_door_list[0]
    min_distance = math.sqrt((self_cord[0] - min_door[0]) ** 2 + (self_cord[1] - min_door[1]) ** 2)
    for door in open_door_list:
        dis = math.sqrt((self_cord[0] - min_door[0]) ** 2 + (door[1] - door[1]) ** 2)
        if dis < min_distance:
            min_distance = dis
            min_door = door
    return min_door


def reversal_direct(direct: str) -> str:
    if direct == "up":
        return "down"
    elif direct == "down":
        return "up"
    elif direct == "left":
        return "right"
    elif direct == "right":
        return "left"


def move_next_room(model: YoloPredict):
    global current_room_number
    x, y, w, h = fd.get_default_region()
    frame = fd.screenshot(x, y, w, h)
    self, _, _, open_door = model.get_cord(frame)
    if len(self) > 0 and len(open_door) > 0:
        while True:
            print("移动到下一个房间")
            print("当前是第" + str(current_room_number) + "个房间")
            x, y, w, h = fd.get_default_region()
            self_cord, monster_cord, _, open_door = model.get_cord(fd.screenshot(x, y, w, h))
            close_door_cord = model.get_monster_cord()
            if len(close_door_cord) > 0 or len(monster_cord) > 0:
                print("已经移动到下一个房间了")
                current_room_number += 1
                print("当前房间序号：" + str(current_room_number))
                if current_room_number >= len(num_direct):
                    current_room_number = 1
                break
            # fd.get_thumbnail_map()
            direct = get_next_door_direction(None, 0)
            next_door_cord = existence_need_door(open_door, direct)
            print("是否存在可以进入的房间" + str(len(next_door_cord) != 0))
            if len(next_door_cord) == 0 and len(self_cord) > 0:
                # 移动寻找门
                print("不存在可以进入的房间，移动寻找")
                # x, y, w, h = fd.get_default_region()
                # x_center, y_center = x + w / 2, y + h / 2
                # eight_move(self_cord, (x_center, y_center), 1)
                continue
            if len(self_cord) > 0 and len(next_door_cord) > 0:
                x_pais = abs(next_door_cord[0] - self_cord[0])
                y_pais = abs(next_door_cord[1] - self_cord[1])
                # 寻找到可以进入的房间后记录与可以进入房间的距离
                # 如果距离小于一定值 开始检测当前距离最近的门的方向是否发生了改变
                # 如果发生了改变则跳出循环进入下一个房间
                if x_pais < 300 and y_pais < 300:
                    x, y, w, h = fd.get_default_region()
                    model.predict_img(fd.screenshot(x, y, w, h))
                    self_cord_ = model.get_self_cord()
                    open_door_list = model.get_open_door_cord()
                    if len(open_door_list) > 0 and len(self_cord_) > 0:
                        min_door = get_min_door(self_cord_, open_door_list)
                        reversal = reversal_direct(direct)
                        _, _, w, h = fd.get_default_region()
                        if get_direction(min_door[0], min_door[1], int(w / 2), int(h / 2)) == reversal:
                            print("已经移动到下一个房间了")
                            current_room_number += 1
                            print("当前房间序号：" + str(current_room_number))
                            if current_room_number >= len(num_direct):
                                current_room_number = 1
                            break

                if x_pais < 50 and y_pais < 50:
                    # 已经在附近但是进不去门，需要重新进一下试试
                    pass
                eight_move(self_cord, next_door_cord)
