import tools.adb_tool as at
import time

skill_cord = {

}

buff_skill_cord = {

}

x_skill_cord = []

move_wheel_cord = []


class Operate:
    def __init__(self, device_id):
        self.device_id = device_id

    def move(self, direction, duration=0, distance=300):
        start_x, start_y = move_wheel_cord
        at.move(direction, start_x, start_y, distance, duration, self.device_id)

    def skill(self, number, cast_type, duration=1000):
        if cast_type == 'click':
            x, y = skill_cord[number]
            at.tap_screen_time(x, y, duration, self.device_id)
        elif cast_type == 'slide_release':
            x, y, x_offset, y_offset = skill_cord[number]
            at.swipe_screen(x, y, x + x_offset, y + y_offset, duration, self.device_id)

    def buff(self):
        for item in buff_skill_cord:
            x, y, t = buff_skill_cord[item]
            at.tap_screen_time(x, y, t, self.device_id)
            time.sleep(0.3)

    def normal_attack(self, times):
        for _ in range(times):
            x, y = x_skill_cord
            at.tap_screen_time(x, y, 100, self.device_id)
            time.sleep(0.1)
