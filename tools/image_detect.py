from tools.image_deal import get_default_region, calculate_brightness, get_default_img
from tools.yolo import YoloPredict
from tools.image_deal import operate_type

# 手机屏幕
key_dict_origin = {
    "P": [0.171875, 0.727315, 0.016250, 0.039815],  # 方向盘
    "H": [0.813750, 0.489815, 0.034167, 0.074074],  # 滑动技能
    "C": [0.802500, 0.917130, 0.029167, 0.056481],  # 后跳
    "X": [0.866042, 0.868519, 0.047083, 0.096296],  # 跳跃
    "B": [0.898750, 0.730556, 0.025000, 0.057407],  # 普攻
    "M": [0.898750, 0.300556, 0.000000, 0.000000]  # 普攻
}

adb_skill_dict_origin = {
    "Z": [0.615833, 0.904630, 0.031667, 0.075926],  # 七个大技能
    "A": [0.680417, 0.907870, 0.036667, 0.069444],
    "S": [0.746667, 0.906944, 0.039167, 0.075000],
    "D": [0.762292, 0.749537, 0.037083, 0.080556],
    "F": [0.814792, 0.632870, 0.037917, 0.069444],
    "G": [0.881250, 0.598611, 0.037500, 0.082407],
    "V": [0.884583, 0.451389, 0.035833, 0.082407],
    "Q": [0.771250, 0.318981, 0.030000, 0.054630],  # 四个小技能图标
    "W": [0.816458, 0.318056, 0.029583, 0.058333],
    "E": [0.860208, 0.318981, 0.031250, 0.052778],
    "R": [0.907083, 0.320833, 0.030833, 0.058333]
}

# 虫洞软件映射截屏
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
        # 根据图片检测技能的cd
        # 使用opencv 检测指定区域的图片亮度 亮度低的地方技能未cd
        _, current_total_lighting = detect_skill_lighting(get_default_img())
        for key, lighting in max_lighting.items():
            # 比最高亮度低10点默认是在cd中的技能
            if lighting - 10 < current_total_lighting[key]:
                current_skill.append(key)
        return current_skill

def get_origin_change(origin_dict: dict) -> dict:
    _, _, image_width, image_height = get_default_region()
    skill_dict = dict()
    for key, data in origin_dict.items():
        x_center, y_center, width, height = data
        # 计算真实坐标
        x = x_center * image_width
        y = y_center * image_height
        skill_dict[key] = [x, y]
    return skill_dict

def skill_change_coordinates(origin_dict: dict) -> dict:
    _, _, image_width, image_height = get_default_region()
    skill_dict = dict()
    for key, data in origin_dict.items():
        x_center, y_center, width, height = data

        # 计算左上角坐标
        x_min = (x_center - width / 2) * image_width
        y_min = (y_center - height / 2) * image_height

        # 计算宽度和高度
        w = width * image_width
        h = height * image_height
        skill_dict[key] = [x_min, y_min, w, h]
    return skill_dict

def get_map_cord() -> []:
    skill_dict = get_origin_change(key_dict_origin)
    return skill_dict["M"][0], skill_dict["M"][1]

#   获取轮盘坐标
def get_move_wheel_cord() -> []:
    skill_dict = get_origin_change(key_dict_origin)
    return skill_dict["P"][0], skill_dict["P"][1]


#   获取普攻
def get_x_skill_cord() -> []:
    skill_dict = get_origin_change(key_dict_origin)
    return skill_dict["X"][0], skill_dict["X"][1]


#   获取后跳坐标
def get_c_skill_cord() -> []:
    skill_dict = get_origin_change(key_dict_origin)
    return skill_dict["C"][0], skill_dict["C"][1]


#   获取技能
def get_skill_cord() -> dict:
    skill_dict = get_origin_change(adb_skill_dict_origin)
    center_cord = dict()
    for key, val in skill_dict.items():
        x, y, _, _ = val
        center_cord[key] = [x, y]
    return center_cord


#   获取buff技能
def get_buff_skill_cord() -> []:
    skill_dict = get_origin_change(adb_skill_dict_origin)
    return skill_dict["W"][0], skill_dict["W"][1]


def get_skill_max_lighting(model: YoloPredict):
    while True:
        self, _, _, _ = model.get_cord()
        if len(self) != 0:
            _, total_lighting = detect_skill_lighting(get_default_img())
            break
    return total_lighting


def detect_skill_lighting(img):
    if operate_type == 0:
        origin_cord = skill_dict_origin
    else:
        origin_cord = adb_skill_dict_origin
    skill_dict = skill_change_coordinates(origin_cord)
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
