from Operate import Operate

class Action:
    def __init__(self):
        self.operate = Operate()
        pass


    def attack(self, self_cord, monster_cord):
        # 计算怪物坐标
        self.operate.move(self_cord)



        # 检测是否存在怪物

        # 存在怪物

        # 离怪物的距离低于一定程度不再检测距离 攻击怪物

        # 离怪物过远不检测距离 移动

        pass

    def pick_material(self, self_cord, material_cord):

        pass

    def move_next(self):
        # 不存在怪物
        # 判断门的位置 控制移动
        pass
