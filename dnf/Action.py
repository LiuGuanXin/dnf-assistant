import time
import dnf.Operate as op
from collections import deque
import dnf.FrameDeal as fd
import dnf.RoomPredict as rp
from dnf.YoloPredict import YoloPredict
import math
import numpy as np

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


def eight_move(self_cord, dest_cord):
    # 计算x轴差异
    x_direction = dest_cord[0] - self_cord[0]
    # 计算y轴差异
    y_direction = dest_cord[1] - self_cord[1]
    # 计算角度
    angle = math.atan(y_direction / x_direction)
    # 判断移动方向
    if x_direction > 0 and y_direction > 0:
        if 0 <= angle < 30:
            op.move("right")
        elif 30 <= angle <= 60:
            op.move("downRight")
        elif 60 < angle <= 90:
            op.move("down")
    elif x_direction > 0 > y_direction:
        if 0 <= angle < 30:
            op.move("right")
        elif 30 <= angle <= 60:
            op.move("topRight")
        elif 60 < angle <= 90:
            op.move("up")
    elif x_direction < 0 < y_direction:
        if 0 <= angle < 30:
            op.move("left")
        elif 30 <= angle <= 60:
            op.move("downLeft")
        elif 60 < angle <= 90:
            op.move("down")
    elif x_direction < 0 and y_direction < 0:
        if 0 <= angle < 30:
            op.move("left")
        elif 30 <= angle <= 60:
            op.move("topLeft")
        elif 60 < angle <= 90:
            op.move("up")


def break_condition(self_cord, dest_cord):
    x_pais = abs(dest_cord[0] - self_cord[0])
    y_pais = abs(dest_cord[1] - self_cord[1])
    if x_pais < 300 and y_pais < 200:
        print("拉怪完成")
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
        if len(self_cord) > 0 and len(dest_cord) > 0:
            if break_condition(self_cord, dest_cord):
                break
            # 四方向操作
            if direction_type == 0:
                four_move(self_cord, dest_cord)
            # 八方向操作
            elif direction_type == 1:
                eight_move(self_cord, dest_cord)



def move_to_cord(dest_cord, model: YoloPredict = None, direction_type=0):
    while True:
        if model is not None:
            x, y, w, h = fd.get_default_region()
            model.predict_img(fd.screenshot(x, y, w, h))
            self_cord = model.get_self_cord()
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
def pick_material(material_cord):
    for material in material_cord:
        move_to_cord(material)


flag = 0


# 攻击
def attack(model: YoloPredict):
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
            # 攻击怪物
            # 如何攻击？ 普攻 + 技能的方式
            op.normal_attack(3)
            # 根据怪物数量选择技能
            # 调整面对方向 面朝怪物的方向
            if self_cord[0] >= x_mean:
                op.move("left")
            else:
                op.move("right")
            # 获取可使用技能
            current_skill = fd.get_cd_skill()
            # 释放技能
            serial_list = current_skill.keys()
            random_skill = np.random.choice(list(serial_list))
            op.skill(current_skill[random_skill], "normal")
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


def calculate_brightness(image):
    # 图像是 RGB 颜色空间
    r_brightness = np.mean(image[:, :, 0])
    g_brightness = np.mean(image[:, :, 1])
    b_brightness = np.mean(image[:, :, 2])
    t_brightness = np.mean(image)
    return t_brightness, r_brightness, g_brightness, b_brightness


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


def split_image_and_calculate_brightness(screenshot, num_splits_x, num_splits_y):
    screenshot = np.array(screenshot)  # 转换为 NumPy 数组

    height, width, _ = screenshot.shape

    # 计算每个小正方形的大小
    step_x = width // num_splits_x
    step_y = height // num_splits_y

    # 初始化结果数组
    brightness_array = np.zeros((num_splits_y, num_splits_x, 3))

    # 遍历图像，切分成小正方形并计算亮度
    for i in range(num_splits_y):
        for j in range(num_splits_x):
            # 计算当前小正方形的坐标范围
            x_start = j * step_x
            y_start = i * step_y
            x_end = x_start + step_x
            y_end = y_start + step_y

            # 提取当前小正方形区域
            square = screenshot[y_start:y_end, x_start:x_end]

            # 计算亮度
            t_brightness, r_brightness, g_brightness = calculate_brightness(square)

            brightness_array[i, j] = [t_brightness, r_brightness, g_brightness]

        max_t = np.max(brightness_array[:, :, 0])
        t_x, t_y = np.argmax(max_t)
        max_r = np.max(brightness_array[:, :, 1])
        r_x, r_y = np.argmax(max_r)
        max_b = np.max(brightness_array[:, :, 2])
        b_x, b_y = np.argmax(max_b)
        min_t = np.min(brightness_array[:, :, 0])
        # 0 无效  1 有效房间  2 开始位置  3 结束位置  4 精英怪位置 5 时空怪位置（需要根据不同地图手动处理）
        # 亮度的高低根据最高亮度和最低亮度定义

        room_class_array = np.zeros((num_splits_y, num_splits_x))

        room_class_array[t_x, t_y] = 2
        room_class_array[r_x, r_y] = 3
        room_class_array[b_x, b_y] = 4
        data = brightness_array[:, :, 0]
        with np.nditer(data, flags=['multi_index']) as it:
            for x in it:
                idx = it.multi_index
                if data[idx] > min_t + (max_t - min_t) * 0.1:
                    x[...] = 1
            return brightness_array


room_class_array = []


def ana_brightness(image):
    r_brightness = image[:, :, 0]
    g_brightness = image[:, :, 1]
    b_brightness = image[:, :, 2]
    t_brightness = (image[:, :, 0] + image[:, :, 1] + image[:, :, 2]) / 3
    return t_brightness, r_brightness, g_brightness, b_brightness


def path_route(img) -> str:
    global room_class_array

    # 获取亮度
    t_brightness, r_brightness, g_brightness, b_brightness = ana_brightness(img)
    print(t_brightness)
    print(r_brightness)
    print(g_brightness)
    print(b_brightness)
    # 根据 亮度 通过opencv 识别出来路径 转化为二维数组
    # 只有刚进入的时候才会规划路径
    # if len(room_class_array) == 0:
    #     # 示例使用
    #     num_splits_x = 10  # x轴方向切分数
    #     num_splits_y = 10  # y轴方向切分数
    #     room_class_array = split_image_and_calculate_brightness(img, num_splits_x, num_splits_y)
    # # 路线规划
    # direct_list = shortest_path_directions(room_class_array)
    # global current_room_number
    # direction = direct_list[current_room_number]
    # current_room_number += 1
    # if current_room_number > len(num_direct) + 1:
    #     current_room_number = 1
    #     room_class_array = []
    # return direction


"""房间对应应该进入的门"""
num_direct = {
    1: "up",
    2: "down",
    3: "left",
    4: "right"
}


# 移动到下一个房间
def fixation():
    global current_room_number
    next_door_direction = num_direct[current_room_number]
    current_room_number += 1
    if current_room_number >= len(num_direct):
        current_room_number = 1
    return next_door_direction


def get_next_door_direction(mag_img, path_type):
    if path_type == 0:
        direction = rp.predict_room(mag_img)
    elif path_type == 1:
        direction = path_route(mag_img)
    else:
        direction = fixation()
    return direction


def move_next(model: YoloPredict):
    # thumbnail_map = fd.get_thumbnail_map()
    # direction = get_next_door_direction(thumbnail_map, 0)
    #
    # x, y, w, h = fd.get_default_region()
    # frame = fd.screenshot(x, y, w, h)
    # self, monster, material, open_door = model.get_cord(frame)
    #
    # # 寻找下一个房间的门的位置
    # # 1 检验屏幕是否有需要的门
    # if existence_need_door(open_door_cord, direction):
    #     move_to_cord(self_cord, open_door_cord)
    #     return
    # # 2 没有移动到屏幕中央  检测有没有门
    # x, y, w, h = fd.get_default_region()
    # x_center, y_center = x + w / 2, y + h / 2
    # move_to_cord(self_cord, (x_center, y_center))
    # model.predict_img(fd.screenshot(x, y, w, h))
    # if existence_need_door(model.get_open_door_cord(), direction):
    #     move_to_cord(self_cord, open_door_cord)
    #     return
    # # 3 没有接着向门的方向移动  循环检测 直到检测到后移动至门内
    # i = 10
    # while i:
    #     model.predict_img(fd.screenshot(x, y, w, h))
    #     # 判断对应方向的门是否存在于屏幕中
    #     if existence_need_door(model.get_open_door_cord(), direction):
    #         move_to_cord(self_cord, open_door_cord)
    #         break
    #     else:
    #         # 朝着预测的方向移动
    #         op.move(direction, 100)
    #         i -= 1
    pass


def move_next_room(model: YoloPredict):
    while True:
        x, y, w, h = fd.get_default_region()
        frame = fd.screenshot(x, y, w, h)
        self, monster, material, open_door = model.get_cord(frame)
        if len(self) > 0 and len(open_door) > 0:
            move_to_cord(open_door[0], model, 0)
        x, y, w, h = fd.get_default_region()
        frame = fd.screenshot(x, y, w, h)
        model.predict_img(frame)
        close_door_cord = model.get_close_door_cord()
        monster_cord = model.get_monster_cord()
        if len(close_door_cord) > 0 or len(monster_cord) > 0:
            break
