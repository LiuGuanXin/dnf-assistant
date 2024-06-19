import dnf.Operate as op


class Action:
    """ 初始化 """

    def __init__(self, role):
        self.role = role

    """ 攻击 """

    def attack(self, self_cord, monster_cord):

        # 有怪物 - 移动 攻击
        # 没有怪物 - 移动到另一个房间

        # 检测是否存在怪物

        # 存在怪物

        # 离怪物的距离低于一定程度不再检测距离 攻击怪物

        # 离怪物过远不检测距离 移动

        pass

    """ 拾取材料 """

    def pick_material(self, self_cord, material_cord):
        for material in material_cord:
            # 分两步移动 分别从 x 轴和 y 轴移动
            # 计算移动的距离
            x_direction = material[0] - self_cord[0]
            # 判断移动方向
            if x_direction > 0:
                direction = "right"
            else:
                direction = "left"
            op.move(direction, x_direction)
            # 计算移动的距离
            y_direction = material[1] - self_cord[1]
            # 判断移动方向
            if y_direction > 0:
                direction = "down"
            else:
                y_direction = "up"
            op.move(direction, y_direction)

    """ 移动到下一个房间 """

    def move_next(self):
        # 不存在怪物
        # 判断门的位置 控制移动
        pass
