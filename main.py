from tools.image_detect import get_skill_max_lighting
from tools.yolo import YoloPredict
from dnf.action import action

yolo = YoloPredict("../model/best.pt")
skill_max_lighting = get_skill_max_lighting(yolo)
act = action(yolo, skill_max_lighting)


def main():
    # buff_skill(skill_max_lighting)
    while True:
        self, monster, material, open_door = yolo.get_cord()
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
            self, monster, material, open_door = yolo.get_cord()
            print("开始攻击")
            if len(monster) != 0 and len(self) != 0:
                act.attack()


if __name__ == '__main__':
    main()
