from tools.image_deal import screenshot, get_default_region, calculate_brightness
from tools.yolo import YoloPredict

# YOLO标签数据
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
# 技能按键
skill_class = ["A", "S", "D", "F", "G", "Q", "W", "E", "R", "V", "Z"]

skill_max_lighting = {}


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
        _, current_total_lighting = detect_skill_lighting(img)
        for key, lighting in max_lighting.items():
            # 比最高亮度低10点默认是在cd中的技能
            if lighting - 10 < current_total_lighting[key]:
                current_skill.append(key)
        return current_skill


def skill_change_coordinates() -> dict:
    _, _, image_width, image_height = get_default_region()

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


def get_skill_max_lighting(model: YoloPredict):
    while True:
        x, y, w, h = get_default_region()
        img = screenshot(x, y, w, h)
        self, _, _, _ = model.get_cord(img)
        if len(self) != 0:
            _, total_lighting = detect_skill_lighting(img)
            break
    return total_lighting


def detect_skill_lighting(img):
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
