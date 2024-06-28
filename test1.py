import cv2
import subprocess


def start_scrcpy():
    subprocess.Popen([
        "scrcpy", "--no-display", "--tcpip=localhost", "--port=8080", "--output-format=h264"
    ])


def capture_video_stream():
    cap = cv2.VideoCapture("tcp://localhost:8080")
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
    start_scrcpy()
    capture_video_stream()


if __name__ == "__main__":
    main()
