import threading # Make sure we can divide code into different threads
import queue # For handling queues
import numpy as np
import cv2
from action import run_motor_worker
from face_tracking import face_tracking
from visual import display
from delta import delta
from camera import camera
from queue_handler import queue_handler
from hand_tracking import handTracking
from gesture_estimator import get_Gesture


########    Variables used      ########### 

# Variable for width and height in pixels that is used for video stream
streamResWidth = 1280
streamResHeight = 720

# Variable for width and height in pixels that is used by the ML algorithms
MLresWidth = 320
MLresHeight = 240

# Scale coordinates
scale_x = streamResWidth / MLresWidth
scale_y = streamResHeight / MLresHeight

# Machine Learning Quality factor for face tracking
ML_Q = 0.4
Q_factor_threshold = 1200


########    Classes used      ########### 

# We need to create instances of each class here:
cam = camera(streamResWidth, streamResHeight, MLresWidth, MLresHeight)
face_tracker = face_tracking(MLresWidth, MLresHeight, ML_Q)
Delta = delta(MLresWidth, MLresHeight)
data_queue = queue_handler()
hand_tracker = handTracking()
gestureTracker = get_Gesture()


display1 = display(scale_x, scale_y)

frame_count = 0
faces = []
quality = []
hands = []
palms = []


while True:
    frames = cam.get_frames()
    active_quality = [0]
    deltaArray = (0, 0)

    faces, quality = face_tracker.get_faces(frames[0])

    if frame_count % 3 == 0:
        # Run hand tracker
        palms, hands = hand_tracker.getHandCoordinates(frames[0])
        


    frame_count += 1 # Increase frame count


    if faces is not None:
        best_face = faces[0] # The face vector is sorted based on quality already, The first one is the best
        deltaArray = Delta.get_delta(best_face)
        active_quality = quality


        # LEo added this to not track any bad faces
        if quality[0] >= Q_factor_threshold:
            data_queue.send_to_queue(deltaArray)


# ________________ Hand Tracking __________________ #
    # Hand tracking code:
    # If hands is not none or 0
    if hands:
        best_hand = hands[0] # Hands is sorted and the best hand will be the first one
        gesture = gestureTracker.getGesture(best_hand) # Find the gesture the first hand is doing
        
        print("Current Gesture: ") 
        print(gesture)


    # Format and display frame
    display1.display_frame(frames[1], faces, active_quality[0], deltaArray, gesture, (streamResWidth, streamResHeight))

    if cv2.waitKey(5) & 0xFF == 27:
            break
