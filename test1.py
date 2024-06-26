import cv2
import subprocess
import numpy as np

# 设置设备屏幕分辨率为 600x800
subprocess.run(["adb", "shell", "wm", "size", "600x800"])

# 启动 scrcpy 并输出原始帧数据
scrcpy_command = ["scrcpy", "--raw"]
scrcpy_process = subprocess.Popen(scrcpy_command, stdout=subprocess.PIPE)


# 函数用于读取并展示帧数据
def display_frames():
    # 读取帧头（12字节）：4字节时间戳 + 4字节长度 + 4字节类型
    header_size = 12
    while True:
        # 从 scrcpy 进程的 stdout 读取帧头
        header = scrcpy_process.stdout.read(header_size)
        if len(header) < header_size:
            break

        # 解析帧头信息
        frame_size = int.from_bytes(header[4:8], byteorder='little')

        # 从 scrcpy 进程的 stdout 读取一帧数据
        frame_data = scrcpy_process.stdout.read(frame_size)

        # 解码为图像
        frame = np.frombuffer(frame_data, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # 检查图像是否解码成功
        if frame is not None:
            # 使用 OpenCV 显示图像
            cv2.imshow("Android Screen", frame)

            # 按 'q' 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


# 显示帧数据
display_frames()


# 点击屏幕
def tap(x, y):
    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)])


# 滑动屏幕
def swipe(x1, y1, x2, y2, duration):
    subprocess.run(["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])


# 示例点击和滑动操作
tap(300, 400)
swipe(100, 200, 300, 400, 500)

# 释放资源
scrcpy_process.terminate()
cv2.destroyAllWindows()

# 恢复设备原始分辨率
subprocess.run(["adb", "shell", "wm", "size", "reset"])
