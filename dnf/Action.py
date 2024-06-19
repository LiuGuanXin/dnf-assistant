import dnf.Operate as op


# 捡材料
def pick_material(self_cord, material_cord):
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

# 攻击
def attack(self_cord, monster_cord, img):
    # 移动到边缘测稍等 为了让怪物聚集
    # 获取怪物中心的坐标 和 最左侧怪物的坐标

    # 攻击怪物
    # 如何攻击？ 普攻 + 技能的方式
    # 根据图片检测技能的cd
    # 根据当前输入图片的的坐标判断各个技能的位置
    # 使用opencv 检测指定区域的图片亮度 亮度低的地方技能未cd
    op.normal_attack(3)
    op.skill("q", "normal")


# 移动到下一房间
def move_next(self_cord, open_door_cord):
    # open_door_cord 是个列表 如何判断走哪个门？
    # 如果是固定某个地图可以记录房间，直接写死
    # 判断门的位置 控制移动
    x_direction = open_door_cord[0][0] - self_cord[0]
    # 判断移动方向
    if x_direction > 0:
        direction = "right"
    else:
        direction = "left"
    op.move(direction, x_direction)
    # 计算移动的距离
    y_direction = open_door_cord[0][0] - self_cord[1]
    # 判断移动方向
    if y_direction > 0:
        direction = "down"
    else:
        y_direction = "up"
    op.move(direction, y_direction)

