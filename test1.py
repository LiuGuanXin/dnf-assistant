import cv2
import subprocess
import threading
import time

scrcpy_path = "G:/scrcpy-win64-v2.4/scrcpy.exe"


def start_scrcpy():
    subprocess.Popen([
        "scrcpy", "--no-playback", "--record=tmp.mp4"
    ])


def capture_video_stream():
    cap = cv2.VideoCapture("tmp.mp4")
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Android Screen', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    scrcpy_thread = threading.Thread(target=start_scrcpy)
    scrcpy_thread.start()

    # 给 scrcpy 一些时间来启动和开始录制
    time.sleep(5)

    capture_video_stream()


if __name__ == "__main__":
    main()
