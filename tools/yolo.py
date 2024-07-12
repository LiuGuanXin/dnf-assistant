from ultralytics import YOLO
from tools.image_deal import get_default_img
import torch
import cv2


class YoloPredict:
    """初始化"""

    def __init__(self, model_path):
        print(torch.cuda.is_available())
        torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.data = None
        self.boxes = None
        self.results = None
        self.img = None
        if model_path is not None:
            self.model = YOLO(model_path)
        else:
            self.model = YOLO("../model/best.pt")

    """检测"""

    def predict_img(self, img):
        self.img = img
        self.results = self.model(img)
        self.boxes = self.results[0].boxes
        self.data = self.results[0].boxes.data
        # [505.0202, 169.7504, 651.0491, 249.8571, 0.8848, 1.]
        # 0: self
        # 1: monster
        # 2: closeDoor
        # 3: material
        # 4: xAxisDoor
        # 5: yAxisDoor
        # 左上角  右下角坐标  置信度 类别
        # self.drawing()

    def get_cord(self):
        # 类别里可以加一个小地图的分类以获取小地图的位置
        self.predict_img(get_default_img())
        self_cord = self.get_self_cord()
        monster_cord = self.get_monster_cord()
        material_cord = self.get_material_cord()
        x_door_cord = self.get_x_door_cord()
        y_door_cord = self.get_y_door_cord()
        return self_cord, monster_cord, material_cord, x_door_cord, y_door_cord

    """获取自身坐标"""

    def get_self_cord(self):
        for item in self.data:
            if item[5] == 0 and item[4] > 0.2:
                x, y = (item[0] + item[2]) / 2, item[3]
                return [x, y]
        return []

    """获取怪物坐标"""

    def get_monster_cord(self):
        monster_cord_list = list()
        for item in self.data:
            if item[5] == 1 and item[4] > 0.7:
                x, y = (item[0] + item[2]) / 2, item[3]
                monster_cord_list.append([x, y])
        return monster_cord_list

    def get_left_monster(self):
        monster_cord = self.get_monster_cord()
        if len(monster_cord) > 0:
            left_x_min = monster_cord[0][0]
            left_y_min = monster_cord[0][1]
            for idx, item in enumerate(monster_cord):
                if item[0] < left_x_min:
                    left_x_min = item[0]
                    left_y_min = item[1]
            return left_x_min, left_y_min
        return []

    """获取材料坐标"""

    def get_material_cord(self):
        material_cord_list = list()
        for item in self.data:
            if item[5] == 3 and item[4] > 0.7:
                x, y = (item[0] + item[2]) / 2, item[3]
                material_cord_list.append([x, y])
        return material_cord_list

    """获取打开的x轴门坐标"""

    def get_x_door_cord(self):
        open_door_cord_list = list()
        for item in self.data:
            if item[5] == 4 and item[4] > 0.4:
                x, y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
                open_door_cord_list.append([x, y])
        return open_door_cord_list

    """获取打开的y轴门坐标"""

    def get_y_door_cord(self):
        open_door_cord_list = list()
        for item in self.data:
            if item[5] == 5 and item[4] > 0.4:
                x, y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
                open_door_cord_list.append([x, y])
        return open_door_cord_list

    """获取关闭的门坐标"""

    def get_close_door_cord(self):
        close_door_cord_list = list()
        for item in self.data:
            if item[5] == 2 and item[4] > 0.7:
                x, y = (item[0] + item[2]) / 2, item[3]
                close_door_cord_list.append([x, y])
        return close_door_cord_list

    """获取名称列表"""

    def get_names(self):
        return self.model.names

    """获取检测框列表"""

    def get_boxes(self):
        return self.boxes

    def drawing(self):
        boxes = self.boxes
        names = self.model.names
        img = self.img
        # 绘制检测结果
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # 获取边界框的坐标
            confidence = box.conf[0]  # 获取置信度
            cls = int(box.cls[0])  # 获取类别索引
            label = f'{names[cls]} {confidence:.2f}'

            # 画框和标签
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
