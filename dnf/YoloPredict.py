from ultralytics import YOLO


class YoloPredict:
    """初始化"""

    def __init__(self, model_path):
        self.data = None
        self.box = None
        self.results = None
        if model_path is not None:
            self.model = YOLO(model_path)
        else:
            self.model = YOLO("../model/best.pt")

    """检测"""

    def deal_img(self, img):
        self.results = self.model(img)
        self.data = self.results[0].boxes.data
        # [505.0202, 169.7504, 651.0491, 249.8571, 0.8848, 1.]
        # 0: self
        # 1: monster
        # 2: closeDoor
        # 3: material
        # 4: openDoor
        # 左上角  右下角坐标  置信度 类别

    """获取自身坐标"""

    def get_self_cord(self):
        x, y = 0, 0
        for item in self.data:
            if item[5] == 0 and item[4] > 0.7:
                x, y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
        return x, y

    """获取怪物坐标"""

    def get_monster_cord(self):
        monster_cord_list = list()
        for item in self.data:
            if item[5] == 1 and item[4] > 0.7:
                x, y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
                monster_cord_list.append([x, y])
        return monster_cord_list

    """获取材料坐标"""

    def get_material_cord(self):
        material_cord_list = list()
        for item in self.data:
            if item[5] == 3 and item[4] > 0.7:
                x, y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
                material_cord_list.append([x, y])
        return material_cord_list

    """获取打开的门坐标"""

    def get_open_door_cord(self):
        open_door_cord_list = list()
        for item in self.data:
            if item[5] == 4 and item[4] > 0.7:
                x, y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
                open_door_cord_list.append([x, y])
        return open_door_cord_list

    """获取关闭的门坐标"""

    def get_close_door_cord(self):
        close_door_cord_list = list()
        for item in self.data:
            if item[5] == 2 and item[4] > 0.7:
                x, y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
            close_door_cord_list.append([x, y])
        return close_door_cord_list
