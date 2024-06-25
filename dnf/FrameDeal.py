# 主要用于处理录屏的帧
import time
from dnf.Operate import press_key
import cv2
import pyautogui
import numpy as np
from dnf.YoloPredict import YoloPredict

""" 截取指定区域的屏幕 """


def screenshot(x: int, y: int, width: int, height: int) -> object:
    # 设置录制区域 (x, y, width, height)
    region = (x, y, width, height)
    # 捕获屏幕指定区域
    return cv2.cvtColor(np.array(pyautogui.screenshot(region=region)), cv2.COLOR_BGR2RGB)


def get_default_region():
    return 1410, 875, 1153, 500


def get_map_region():
    x, y, image_width, image_height = get_default_region()
    x_center, y_center, width, height = [0.496097, 0.511000, 0.220295, 0.406000]
    # 计算左上角坐标
    x_min = x + (x_center - width / 2) * image_width
    y_min = y + (y_center - height / 2) * image_height
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


def get_thumbnail_map_v2() -> []:
    press_key("M", 0.5)
    time.sleep(2)
    x, y, w, h = get_default_region()
    img = screenshot(x, y, w, h)
    x_center, y_center, width, height = [0.496097, 0.511000, 0.220295, 0.406000]
    x_m = (x_center - width / 2) * w
    y_m = (y_center - height / 2) * h
    # 计算宽度和高度
    w_m = width * w
    h_m = height * h
    # 获取亮度
    return img[int(y_m):int(y_m + h_m), int(x_m):int(x_m + w_m)]


def calculate_average_brightness(image, top_left, bottom_right):
    # 提取指定区域
    region = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    # 计算平均亮度
    average_brightness = np.mean(region)
    return average_brightness


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

            brightness_array[i, j] = [t_brightness, r_brightness, g_brightness, b_brightness]

        max_t = np.max(brightness_array[:, :, 0])
        t_x, t_y = np.argmax(max_t)
        max_r = np.max(brightness_array[:, :, 1])
        r_x, r_y = np.argmax(max_r)
        max_g = np.max(brightness_array[:, :, 2])
        g_x, g_y = np.argmax(max_g)
        max_b = np.min(brightness_array[:, :, 3])
        b_x, b_y = np.argmax(max_b)
        min_t = np.min(brightness_array[:, :, 0])
        # 0 无效  1 有效房间  2 开始位置  3 结束位置  4 精英怪位置 5 补给位置 6 时空怪位置（需要根据不同地图手动处理）
        # 亮度的高低根据最高亮度和最低亮度定义

        room_class_array = np.zeros((num_splits_y, num_splits_x))

        room_class_array[t_x, t_y] = 2
        room_class_array[r_x, r_y] = 3
        room_class_array[b_x, b_y] = 4
        room_class_array[g_x, g_y] = 5
        data = brightness_array[:, :, 0]
        # 使用enumerate获取索引
        for i, row in enumerate(data):
            for j, element in enumerate(row):
                if data[i, j] < min_t + (max_t - min_t) * 0.1:
                    room_class_array[i, j] = 1
        return room_class_array

