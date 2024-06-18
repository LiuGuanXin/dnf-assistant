import cv2
import pyautogui
import numpy as np
from YoloPredict import YoloPredict
from Action import Action
from Operate import Operate


yolo = YoloPredict()
action = Action()
operate = Operate()


def screenshot():
    # 设置录制区域 (x, y, width, height)
    region = (100, 100, 500, 400)
    # 捕获屏幕指定区域
    frame = np.array(pyautogui.screenshot(region=region))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame


while True:
    frame = screenshot()
    yolo.deal_img(frame)
    self_cord = yolo.get_cord(0)
    monster_cord = yolo.get_cord(1)
    material_cord = yolo.get_cord(2)
    open_door_cord = yolo.get_cord(2)
    if monster_cord is not None:
        action.attack(monster_cord)
    if material_cord is not None:
        action.pick_material()
    if (monster_cord is None
            and material_cord is None
            and open_door_cord is not None):
        action.move_next()

    # 检测是否按下了'Q'键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 释放资源
cv2.destroyAllWindows()
