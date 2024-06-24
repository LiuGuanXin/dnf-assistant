import sys
import subprocess
import threading
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
from PIL import Image

class ScreenMirror(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("手机控制界面")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # 显示手机屏幕的区域
        self.screen_label = QLabel(self)
        self.layout.addWidget(self.screen_label)

        # 点击操作
        self.click_layout = QHBoxLayout()
        self.click_x_input = QLineEdit(self)
        self.click_x_input.setPlaceholderText("点击X坐标")
        self.click_y_input = QLineEdit(self)
        self.click_y_input.setPlaceholderText("点击Y坐标")
        self.click_duration_input = QLineEdit(self)
        self.click_duration_input.setPlaceholderText("点击时长(毫秒)")
        self.click_button = QPushButton("执行点击操作", self)
        self.click_button.clicked.connect(self.perform_click)

        self.click_layout.addWidget(self.click_x_input)
        self.click_layout.addWidget(self.click_y_input)
        self.click_layout.addWidget(self.click_duration_input)
        self.click_layout.addWidget(self.click_button)
        self.layout.addLayout(self.click_layout)

        # 滑动操作
        self.swipe_layout = QHBoxLayout()
        self.swipe_start_x_input = QLineEdit(self)
        self.swipe_start_x_input.setPlaceholderText("起始X坐标")
        self.swipe_start_y_input = QLineEdit(self)
        self.swipe_start_y_input.setPlaceholderText("起始Y坐标")
        self.swipe_end_x_input = QLineEdit(self)
        self.swipe_end_x_input.setPlaceholderText("结束X坐标")
        self.swipe_end_y_input = QLineEdit(self)
        self.swipe_end_duration_input = QLineEdit(self)
        self.swipe_end_duration_input.setPlaceholderText("滑动时长(毫秒)")
        self.swipe_button = QPushButton("执行滑动操作", self)
        self.swipe_button.clicked.connect(self.perform_swipe)

        self.swipe_layout.addWidget(self.swipe_start_x_input)
        self.swipe_layout.addWidget(self.swipe_start_y_input)
        self.swipe_layout.addWidget(self.swipe_end_x_input)
        self.swipe_layout.addWidget(self.swipe_end_y_input)
        self.swipe_layout.addWidget(self.swipe_end_duration_input)
        self.swipe_layout.addWidget(self.swipe_button)
        self.layout.addLayout(self.swipe_layout)

        # 获取点击坐标
        self.get_coords_button = QPushButton("获取点击坐标", self)
        self.get_coords_button.clicked.connect(self.get_click_coords)
        self.layout.addWidget(self.get_coords_button)

        self.setLayout(self.layout)

        # 启动线程来更新屏幕
        self.update_thread = threading.Thread(target=self.update_screen)
        self.update_thread.daemon = True
        self.update_thread.start()

        # 保存点击坐标
        self.click_coords = None

    def update_screen(self):
        while True:
            screenshot = self.get_screenshot()
            if screenshot:
                self.screen_label.setPixmap(QPixmap.fromImage(screenshot))
            time.sleep(1)  # 每秒更新一次

    def get_screenshot(self):
        try:
            subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=open('screen.png', 'wb'))
            image = Image.open('screen.png')
            image = image.resize((400, 800))  # 调整图片大小以适应界面
            image_qt = QImage(image.tobytes(), image.width, image.height, QImage.Format_RGB888)
            return image_qt
        except Exception as e:
            print(f"截图失败: {e}")
            return None

    def perform_click(self):
        x = self.click_x_input.text()
        y = self.click_y_input.text()
        duration = self.click_duration_input.text()
        subprocess.run(['adb', 'shell', 'input', 'tap', x, y])

    def perform_swipe(self):
        start_x = self.swipe_start_x_input.text()
        start_y = self.swipe_start_y_input.text()
        end_x = self.swipe_end_x_input.text()
        end_y = self.swipe_end_y_input.text()
        duration = self.swipe_end_duration_input.text()
        subprocess.run(['adb', 'shell', 'input', 'swipe', start_x, start_y, end_x, end_y, duration])

    def get_click_coords(self):
        self.get_coords_button.setText("点击屏幕获取坐标中...")
        self.screen_label.mousePressEvent = self.capture_click_coords

    def capture_click_coords(self, event):
        self.click_coords = event.pos()
        self.click_x_input.setText(str(self.click_coords.x()))
        self.click_y_input.setText(str(self.click_coords.y()))
        self.get_coords_button.setText("获取点击坐标")
        self.screen_label.mousePressEvent = lambda event: None  # 恢复默认点击事件

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenMirror()
    window.show()
    sys.exit(app.exec_())
