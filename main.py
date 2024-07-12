import time

from tools.image_detect import get_skill_max_lighting
from tools.yolo import YoloPredict
from dnf.action import action
from dnf.action import current_room_number
from dnf.action import get_next_door_direction
from dnf.action import rechallenge, confirm_challenge
from tools.pd_ocr import pd_ocr

ocr = pd_ocr()
yolo = YoloPredict("../model/best.pt")

skill_max_lighting = get_skill_max_lighting(yolo)
act = action(yolo, skill_max_lighting)


def main():
    while True:
        self, monster, material, open_door = yolo.get_cord()
        for _ in range(5):
            if len(monster) == 0 and len(material) > 0:
                # 捡材料
                act.pick_material()
            # 如果当前房间是最终的房间，检测是否出现了重新挑战
            _, total_rooms = get_next_door_direction(0)
            if current_room_number == total_rooms:
                # 如果出现了重新挑战且检测不到存在材料
                rechallenge_cord = ocr.detect_rechallenge()
                if len(rechallenge_cord) > 0 and len(material) == 0:
                    # 点击重新挑战
                    print("re-challenge")
                    rechallenge(rechallenge_cord)
                    time.sleep(2)
                    select_cord, confirm_cord = ocr.confirm_challenge()
                    if len(select_cord) > 0 and len(confirm_cord) > 0:
                        confirm_challenge(select_cord, confirm_cord)
        # 判断是否有开着的门
        if len(open_door) > 0 and len(monster) == 0 and len(material) == 0:
            print("move to next room")
            act.move_next_room()
        if len(self) != 0 and len(monster) != 0:
            act.use_buff_skill()
            act.gather_monster_move()
            self, monster, material, open_door = yolo.get_cord()
            print("prepare for the attack")
            if len(monster) != 0 and len(self) != 0:
                act.attack()


if __name__ == '__main__':
    main()
