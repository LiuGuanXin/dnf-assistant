import cv2
import pyautogui
import numpy as np
from dnf.YoloPredict import YoloPredict
from dnf.Action import Action


yolo = YoloPredict("../model/best.pt")
action = Action()


def screenshot(x, y, width, height):
    # 设置录制区域 (x, y, width, height)
    region = (x, y, width, height)
    # 捕获屏幕指定区域
    return cv2.cvtColor(np.array(pyautogui.screenshot(region=region)), cv2.COLOR_BGR2RGB)


while True:
    frame = screenshot(1410, 875, 1153, 500)
    yolo.deal_img(frame)
    self_cord = yolo.get_self_cord()
    monster_cord = yolo.get_monster_cord()
    material_cord = yolo.get_material_cord()
    open_door_cord = yolo.get_open_door_cord()
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
