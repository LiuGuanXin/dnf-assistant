import subprocess
import cv2
import numpy as np

scrcpy_path = "F:/scrcpy/scrcpy.exe"


def capture_screen():
    # 使用 scrcpy 捕获屏幕
    process = subprocess.Popen([scrcpy_path, '-b16M', '--max-size', '800', '--tcpip=192.168.0.100'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return process.stdout


def show_image(stream):
    while True:
        # 读取流中的图像数据
        data = stream.read(921600)
        if not data:
            break
        # 转换为 numpy 数组
        frame = np.frombuffer(data, dtype=np.uint8).reshape((720, 1280, 3))
        # 显示图像
        cv2.imshow('Screen', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    stream = capture_screen()
    show_image(stream)
