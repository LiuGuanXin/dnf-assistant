# 主要用于处理录屏的帧
import time
from dnf.Operate import press_key
import cv2
import pyautogui
import numpy as np
from dnf.YoloPredict import YoloPredict


def get_default_region():
    return 1410, 875, 1153, 500


def get_map_region():
    x, y, image_width, image_height = get_default_region()
    x_center, y_center, width, height = data = [0.496097, 0.511000, 0.220295, 0.406000]
    # 计算左上角坐标
    x_min = (x_center - width / 2) * image_width
    y_min = (y_center - height / 2) * image_height
    # 计算宽度和高度
    w = width * image_width
    h = height * image_height
    return x_min, y_min, w, h


def get_thumbnail_map() -> []:
    press_key("M", 0.5)
    time.sleep(2)
    x, y, w, h = get_map_region()
    img = screenshot(x, y, w, h)
    # 获取亮度
    return img


# 技能按键
skill_class = ["A", "S", "D", "F", "G", "Q", "W", "E", "R", "V", "Z"]


def calculate_average_brightness(image, top_left, bottom_right):
    # 提取指定区域
    region = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    # 计算平均亮度
    average_brightness = np.mean(region)
    return average_brightness


""" 截取指定区域的屏幕 """


def screenshot(x: int, y: int, width: int, height: int) -> object:
    # 设置录制区域 (x, y, width, height)
    region = (x, y, width, height)
    # 捕获屏幕指定区域
    return cv2.cvtColor(np.array(pyautogui.screenshot(region=region)), cv2.COLOR_BGR2RGB)


def calculate_brightness(image):
    # 图像是 RGB 颜色空间
    r_brightness = np.mean(image[:, :, 0])
    g_brightness = np.mean(image[:, :, 1])
    b_brightness = np.mean(image[:, :, 2])
    t_brightness = np.mean(image)
    return t_brightness, r_brightness, g_brightness, b_brightness


def split_image_and_calculate_brightness(img, num_splits_x, num_splits_y):
    img = np.array(img)  # 转换为 NumPy 数组

    height, width, _ = img.shape

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
            square = img[y_start:y_end, x_start:x_end]

            # 计算亮度
            t_brightness, r_brightness, g_brightness, b_brightness = calculate_brightness(square)

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


# 示例YOLO标签数据
skill_dict_origin = {
    "Z": [0.612316, 0.938000, 0.036427, 0.076000],
    "A": [0.677797, 0.935000, 0.033825, 0.078000],
    "S": [0.743712, 0.934000, 0.035559, 0.076000],
    "D": [0.761492, 0.774000, 0.034692, 0.084000],
    "F": [0.813096, 0.652000, 0.033825, 0.076000],
    "G": [0.881613, 0.617000, 0.033825, 0.082000],
    "V": [0.881613, 0.465000, 0.035559, 0.082000],
    "Q": [0.768864, 0.326000, 0.026886, 0.064000],
    "W": [0.813964, 0.326000, 0.028621, 0.064000],
    "E": [0.858630, 0.328000, 0.027754, 0.068000],
    "R": [0.904163, 0.329000, 0.028621, 0.066000]
}
slide_region = [0.812229, 0.505000]


def skill_change_coordinates() -> dict:
    x, y, image_width, image_height = get_default_region()

    skill_dict = dict()
    for key, data in skill_dict_origin.items():
        x_center, y_center, width, height = data

        # 计算左上角坐标
        x_min = (x_center - width / 2) * image_width
        y_min = (y_center - height / 2) * image_height

        # 计算宽度和高度
        w = width * image_width
        h = height * image_height
        skill_dict[key] = [x_min, y_min, w, h]
    return skill_dict


def detect_lighting(img):
    skill_dict = skill_change_coordinates()
    lighting_dict = dict()
    total_lighting_dict = dict()
    for key, data in skill_dict.items():
        x, y, w, h = data
        region = img[int(y):int(y + h), int(x):int(x + w)]
        # 计算亮度
        t_avg, r_avg, g_avg, b_avg = calculate_brightness(region)
        lighting_dict[key] = [t_avg, r_avg, g_avg, b_avg]
        total_lighting_dict[key] = t_avg
    return lighting_dict, total_lighting_dict


skill_max_lighting = {}


def get_skill_max_lighting(model: YoloPredict):
    while True:
        x, y, w, h = get_default_region()
        img = screenshot(x, y, w, h)
        self, monster, material, open_door = model.get_cord(img)
        if len(self) != 0:
            skill_dict, total_lighting = detect_lighting(img)
            break
    return total_lighting


def get_cd_skill(choice_type, max_lighting: dict) -> list:
    # 存储的可以释放的技能
    current_skill = list()
    # 返回所有技能列表
    if choice_type == 0:
        return skill_class
    else:
        x, y, w, h = get_default_region()
        img = screenshot(x, y, w, h)
        # 根据图片检测技能的cd
        # 使用opencv 检测指定区域的图片亮度 亮度低的地方技能未cd
        lighting_dict, current_total_lighting = detect_lighting(img)
        for key, lighting in max_lighting.items():
            # 比最高亮度低10点默认是在cd中的技能
            if lighting - 10 < current_total_lighting[key]:
                current_skill.append(key)
        return current_skill
