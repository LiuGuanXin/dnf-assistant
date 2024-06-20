from dnf.FrameDeal import screenshot
from dnf.FrameDeal import get_default_region
from dnf.YoloPredict import YoloPredict
import dnf.Action as act

yolo = YoloPredict("../model/best.pt")


def main():
    x, y, w, h = get_default_region()
    while True:
        frame = screenshot(x, y, w, h)
        self, monster, material, open_door, thumbnail_map = yolo.get_cord(frame)
        if len(monster) != 0 and len(self) != 0:
            act.attack(self, monster)
        if len(material) != 0 and len(self) != 0:
            act.pick_material(self, material)
        if (len(monster) != 0
                and len(material) != 0
                and len(open_door) != 0):
            room_number = 1
            act.move_next(self, thumbnail_map, room_number, yolo)


if __name__ == '__main__':
    main()
