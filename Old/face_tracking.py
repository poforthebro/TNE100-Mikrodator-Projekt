import cv2
from picamera2 import Picamera2

# Variable for width and height in pixels
resolutionWidth = 640
resolutionHeight = 480

# 1. Initialize the modern Raspberry Pi camera module
picam2 = Picamera2()

# Configure it for OpenCV's preferred format (BGR) and the specified size
picam2.configure(picam2.create_video_configuration(main={"format": 'BGR888', "size": (resolutionWidth, resolutionHeight)}))
picam2.start()

# Load OpenCV's built-in deep learning face detector (YuNet)
# Ensure 'face_detection_yunet.onnx' is in the same folder
detector = cv2.FaceDetectorYN.create(
    model='face_detection_yunet.onnx',
    config='',
    input_size=(resolutionWidth, resolutionHeight),
    score_threshold=0.6
)

# Function to calculate quality of each face
def get_quality_score(face):
    width = face[2]
    height = face[3]
    confidence = face[14]
    
    area = width * height
    
    # Multiply size by clarity (e.g., 40,000 px area * 0.95 confidence)
    return area * confidence

# Calculate face distance from center of screen in x and y
def get_delta_xy(x, y):
    deltaX = (resolutionWidth // 2) - x
    deltaY = (resolutionHeight // 2) - y
    return (deltaX, deltaY)

# draw a rectangle around a face
def draw_rectangle(frame, face):
    box = list(map(int, face[:4]))
    cv2.rectangle(frame, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0, 255, 0), 2)
    
    landmarks = list(map(int, face[4:14]))

    # Uncomment both lines to draw circles in eyes, nose and mouth
    #for i in range(5):

    # Uncomment line to draw circles in eyes, nose and mouth
    # cv2.circle(frame, (landmarks[2*i], landmarks[2*i+1]), 2, (0, 0, 255), -1)


# Draw Circle in middle of best face
def draw_circle_face(frame, x, y):

    centerOfCircle = (x, y) 
    image = cv2.circle(frame, centerOfCircle, radius = 10, color = (0, 0, 255), thickness = -1)

while True:
    # 2. Capture a frame directly from Picamera2
    frame = picam2.capture_array()

    # Mirror flip the frame for a more natural view
    frame = cv2.flip(frame, 1)

    # 3. Detect faces
    status, faces = detector.detect(frame)

    # 4. Draw bounding boxes and landmarks
    if faces is not None: # Check that there is a face available
        faces = sorted(faces, key=get_quality_score, reverse=True)
        

        best_face = faces[0]
        best_face_coord = list(map(int, best_face[:4]))
        x = best_face_coord[0] + ( best_face_coord[2] // 2 ) # Center of face
        y = best_face_coord[1] + ( best_face_coord[3] // 2 ) # Center of face
    
        delta = get_delta_xy(x, y)
        cv2.putText(frame, f"Delta X: {delta[0]}, Delta Y: {delta[1]}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


        score = int(get_quality_score(best_face))
        cv2.putText(frame, f"Score: {score}", (best_face_coord[0], best_face_coord[1] - 10), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        draw_circle_face(frame, x, y)

        # Square around all faces
        for face in faces: # Loop through alla faces
            draw_rectangle(frame, face)

            
    # Display the frame
    cv2.imshow('Modern Pi Camera Face Tracking', frame)

    # ESC to exit
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Clean up resources safely
picam2.stop()
cv2.destroyAllWindows()