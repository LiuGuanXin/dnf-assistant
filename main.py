from dnf.FrameDeal import screenshot
from dnf.FrameDeal import get_default_region
from dnf.YoloPredict import YoloPredict
import dnf.Action as act

yolo = YoloPredict("../model/best.pt")


def main():
    x, y, w, h = get_default_region()
    while True:
        frame = screenshot(x, y, w, h)
        self, monster, material, open_door = yolo.get_cord(frame)
        # 判断是否有开着的门
        if len(open_door) > 0:
            print("移动到下一个房间")
            act.move_next_room(yolo)
        # 判断当前屏幕是否存在怪物
        # 判断是否存在材料
        # 如果不存在判断是否有关闭的门
        # 如果有移动角色寻找怪物
        # 如果没有判断是否有打开的们
        if len(self) != 0:
            act.gather_monster_move(yolo, 1)
            frame = screenshot(x, y, w, h)
            self, monster, material, open_door = yolo.get_cord(frame)
            print("开始攻击")
            if len(monster) != 0 and len(self) != 0:
                act.attack(yolo)


if __name__ == '__main__':
    main()
