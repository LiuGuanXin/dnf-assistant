from ultralytics import YOLO
from tools.screenshot import get_screenshot
import cv2

# 初始化YOLOv8模型
model = YOLO("model/best.pt")


# 实时捕获屏幕内容并进行检测
while True:
    frame = get_screenshot()

    # 使用 YOLOv8 模型进行实时检测
    results = model(frame)
    # Detection

    # 绘制检测结果
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # 获取边界框的坐标
        confidence = box.conf[0]  # 获取置信度
        cls = int(box.cls[0])  # 获取类别索引
        label = f'{model.names[cls]} {confidence:.2f}'

        # 画框和标签
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 显示结果帧
    cv2.imshow("Screen Capture", frame)

    # 检测是否按下了'Q'键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cv2.destroyAllWindows()
