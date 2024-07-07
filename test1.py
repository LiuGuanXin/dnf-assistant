import time

from tools.image_detect import get_skill_max_lighting
from tools.yolo import YoloPredict
from dnf.action import action

yolo = YoloPredict("../model/best.pt")
skill_max_lighting = get_skill_max_lighting(yolo)
act = action(yolo, skill_max_lighting)
while True:
    act.use_random_skill()
    time.sleep(1)
