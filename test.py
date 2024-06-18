import cv2
import pyautogui
import numpy as np
from YoloPredict import YoloPredict
from Action import Action
from Operate import Operate


yolo = YoloPredict()
action = Action()
operate = Operate()


def screenshot(x, y, width, height):
    # 设置录制区域 (x, y, width, height)
    region = (x, y, width, height)
    # 捕获屏幕指定区域
    img = np.array(pyautogui.screenshot(region=region))
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


while True:
    frame = screenshot(100, 100, 1000, 1000)
    yolo.deal_img(frame)
    self_cord = yolo.get_cord(0)
    monster_cord = yolo.get_cord(1)
    material_cord = yolo.get_cord(2)
    open_door_cord = yolo.get_cord(2)
    if monster_cord is not None and self_cord is not None:
        action.attack(self_cord, monster_cord)
    if material_cord is not None and self_cord is not None:
        action.pick_material(self_cord, material_cord)
    if (monster_cord is None
            and material_cord is None
            and open_door_cord is not None):
        action.move_next()

    # 检测是否按下了'Q'键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 释放资源
cv2.destroyAllWindows()
