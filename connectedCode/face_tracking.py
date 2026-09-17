import cv2
from picamera2 import Picamera2


# Variable for width and height in pixels that is used for video stream
streamResWidth = 1080
streamResHeight = 1920

# Variable for width and height in pixels that is used by the ML algorithms
MLresWidth = 640
MLresHeight = 480

# Scale coordinates
scale_x = streamResWidth / MLresWidth
scale_y = streamResHeight / MLresHeight



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
    deltaX = (MLresWidth // 2) - x
    deltaY = (MLresHeight // 2) - y
    return (deltaX, deltaY)

# draw a rectangle around a face
def draw_rectangle(frame, face):
    box = list(map(int, face[:4]))

    small_x, small_y, small_w, small_h = box[0], box[1], box[2], box[3]

    big_x = int(small_x * scale_x)
    big_y = int(small_y * scale_y)
    big_w = int(small_w * scale_x)
    big_h = int(small_h * scale_y)

    cv2.rectangle(frame, (big_x, big_y), (big_w + big_x, big_h + big_y), (0, 255, 0), 2)
    
    landmarks = list(map(int, face[4:14]))

    # Uncomment both lines to draw circles in eyes, nose and mouth
    #for i in range(5):

    # Uncomment line to draw circles in eyes, nose and mouth
    # cv2.circle(frame, (landmarks[2*i], landmarks[2*i+1]), 2, (0, 0, 255), -1)


# Draw Circle in middle of best face
def draw_circle_face(frame, x, y):
    big_x = int(x * scale_x)
    big_y = int(y * scale_y)

    centerOfCircle = (big_x, big_y) 
    image = cv2.circle(frame, centerOfCircle, radius = 10, color = (0, 0, 255), thickness = -1)

# Function that continously maps face coordinates
def run_tracker(on_target_update):

    # 1. Initialize the modern Raspberry Pi camera module
    picam2 = Picamera2()

    # Configure camera to create both a high res and a lores stream
    config = picam2.create_video_configuration(
        main={"format": 'BGR888', "size": (streamResWidth, streamResHeight)},
        lores={"format": 'BGR888', "size": (MLresWidth, MLresHeight)}
        )
        
    picam2.configure(config)
    picam2.start()

    # Load OpenCV's built-in deep learning face detector (YuNet)
    # Ensure 'face_detection_yunet.onnx' is in the same folder
    detector = cv2.FaceDetectorYN.create(
        model='face_detection_yunet.onnx',
        config='',
        input_size=(MLresWidth, MLresHeight),
        score_threshold=0.6
    )


    while True:
    # Grab both frames from the hardware
        request = picam2.capture_request()
        high_res_frame = request.make_array("main")
        ml_frame = request.make_array("lores")

    # Flip both
        high_res_frame = cv2.flip(high_res_frame, 1)
        ml_frame = cv2.flip(ml_frame, 1)

        # 3. Detect faces
        status, faces = detector.detect(ml_frame)

        # 4. Draw bounding boxes and landmarks
        if faces is not None: # Check that there is a face available
            faces = sorted(faces, key=get_quality_score, reverse=True)
            

            best_face = faces[0]
            best_face_coord = list(map(int, best_face[:4]))
            small_x = best_face_coord[0] + ( best_face_coord[2] // 2 ) # Center of face
            small_y = best_face_coord[1] + ( best_face_coord[3] // 2 ) # Center of face
        
            delta = get_delta_xy(small_x, small_y)
            cv2.putText(high_res_frame, f"Delta X: {delta[0]}, Delta Y: {delta[1]}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # This line sends the delta values to the action.py file
            on_target_update(delta[0], delta[1])

            score = int(get_quality_score(best_face))
            cv2.putText(high_res_frame, f"Score: {score}", (int(best_face_coord[0] * scale_x), int( (best_face_coord[1] - 10) * scale_y) ), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            draw_circle_face(high_res_frame, small_x, small_y)

            # Square around all faces
            for face in faces: # Loop through alla faces
                draw_rectangle(high_res_frame, face)

                
        # Display the frame
        cv2.imshow('Modern Pi Camera Face Tracking', high_res_frame)

        # ESC to exit
        if cv2.waitKey(5) & 0xFF == 27:
            break

    # Clean up resources safely
    picam2.stop()
    cv2.destroyAllWindows()