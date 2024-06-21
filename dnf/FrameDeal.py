# 主要用于处理录屏的帧
import cv2
import pyautogui
import numpy as np


def get_default_region():
    return 1410, 875, 1153, 500


def get_map_region():
    x, y, w, h = get_default_region()
    return x + w / 2, y + w / 2, w / 2, h / 2


# 定义多个指定区域（使用左上角和右下角的坐标）
regions = [
    ((50, 50), (150, 150)),
    ((200, 200), (300, 300))
]
# 与上面的区域定义对应，定义技能级别
skill_class = {
    1: "h",
    2: 'j'
}


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


def get_cd_skill() -> dict:
    x, y, w, h = get_default_region()
    img = screenshot(x, y, w, h)
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
    return current_skill
