import cv2
import pyautogui
import numpy as np
from dnf.YoloPredict import YoloPredict
import dnf.Action as act


yolo = YoloPredict("../model/best.pt")


def screenshot(x, y, width, height):
    # 设置录制区域 (x, y, width, height)
    region = (x, y, width, height)
    # 捕获屏幕指定区域
    return cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_BGR2RGB)


while True:
    frame = screenshot(1410, 875, 1153, 500)
    yolo.deal_img(frame)
    self_cord = yolo.get_self_cord()
    monster_cord = yolo.get_monster_cord()
    material_cord = yolo.get_material_cord()
    open_door_cord = yolo.get_open_door_cord()
    if len(monster_cord) != 0 and len(self_cord) != 0:
        act.attack(self_cord, monster_cord, frame)
    if  len(material_cord) != 0 and len(self_cord) != 0:
        act.pick_material(self_cord, material_cord)
    if (len(monster_cord) != 0
            and len(material_cord) != 0
            and len(open_door_cord) != 0):
        act.move_next(self_cord, open_door_cord)

    # 检测是否按下了'Q'键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 释放资源
cv2.destroyAllWindows()
