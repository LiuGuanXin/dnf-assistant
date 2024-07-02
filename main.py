from tools.image_deal import screenshot
from tools.image_deal import get_default_region
from tools.image_detect import get_skill_max_lighting
from tools.yolo import YoloPredict
from dnf.action import action

yolo = YoloPredict("../model/best.pt")
act = action(yolo)


def main():
    skill_max_lighting = get_skill_max_lighting(yolo)
    x, y, w, h = get_default_region()
    # buff_skill(skill_max_lighting)
    while True:
        frame = screenshot(x, y, w, h)
        self, monster, material, open_door = yolo.get_cord(frame)
        for _ in range(5):
            if len(monster) == 0 and len(material) > 0:
                # 捡材料
                act.pick_material()
        # 判断是否有开着的门
        if len(open_door) > 0 and len(monster) == 0 and len(material) == 0:
            print("移动到下一个房间")
            act.move_next_room()
        if len(self) != 0 and len(monster) != 0:
            act.gather_monster_move()
            frame = screenshot(x, y, w, h)
            self, monster, material, open_door = yolo.get_cord(frame)
            print("开始攻击")
            if len(monster) != 0 and len(self) != 0:
                act.attack(skill_max_lighting)


if __name__ == '__main__':
    main()
