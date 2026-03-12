import cv2

username = "admin"
password = "ipcam1379"
ip = "192.168.100.64"

rtsp_url = f"rtsp://{username}:{password}@{ip}:554/Streaming/Channels/101"

cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("❌ Cannot open RTSP stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    cv2.imshow("Hikvision Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()