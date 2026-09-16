import cv2
from picamera2 import Picamera2

# 1. Initialize the modern Raspberry Pi camera module
picam2 = Picamera2()

# Configure it for OpenCV's preferred format (BGR) and a 640x480 resolution
picam2.configure(picam2.create_video_configuration(main={"format": 'BGR888', "size": (640, 480)}))
picam2.start()

# Load OpenCV's built-in deep learning face detector (YuNet)
# Ensure 'face_detection_yunet.onnx' is in the same folder
detector = cv2.FaceDetectorYN.create(
    model='face_detection_yunet.onnx',
    config='',
    input_size=(640, 480),
    score_threshold=0.6
)

while True:
    # 2. Capture a frame directly from Picamera2
    frame = picam2.capture_array()

    # Mirror flip the frame for a more natural view
    frame = cv2.flip(frame, 1)

    # 3. Detect faces
    status, faces = detector.detect(frame)

    # 4. Draw bounding boxes and landmarks
    if faces is not None:
        for face in faces:
            box = list(map(int, face[:4]))
            cv2.rectangle(frame, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0, 255, 0), 2)
            
            landmarks = list(map(int, face[4:14]))
            for i in range(5):
                cv2.circle(frame, (landmarks[2*i], landmarks[2*i+1]), 2, (0, 0, 255), -1)

    # Display the frame
    cv2.imshow('Modern Pi Camera Face Tracking', frame)

    # ESC to exit
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Clean up resources safely
picam2.stop()
cv2.destroyAllWindows()
