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
from gesture_estimator import getGesture


########    Variables used      ########### 

# Variable for width and height in pixels that is used for video stream
streamResWidth = 1920
streamResHeight = 1080

# Variable for width and height in pixels that is used by the ML algorithms
MLresWidth = 320
MLresHeight = 240

# Scale coordinates
scale_x = streamResWidth / MLresWidth
scale_y = streamResHeight / MLresHeight

# Machine Learning Quality factor for face tracking
ML_Q = 0.3


########    Classes used      ########### 

# We need to create instances of each class here:
cam = camera(streamResWidth, streamResHeight, MLresWidth, MLresHeight)
face_tracker = face_tracking(MLresWidth, MLresHeight, ML_Q)
Delta = delta(MLresWidth, MLresHeight)
data_queue = queue_handler()
hand_tracker = handTracking()


display1 = display(scale_x, scale_y)




while True:
    frames = cam.get_frames()
    active_quality = [0]
    deltaArray = (0, 0)

    faces, quality = face_tracker.get_faces(frames[0])
    
    # Run hand tracker
    palms, hands = hand_tracker.getHandCoordinates(frames[0])
    print("Hands: ")
    
    for hand in hands:
        for entry in hand:
            print(entry)

    print("palms: ")
    for palm in palms:
            for entry in palm:
                print(entry)
    
        

    # Figure out hand sign / whatever, not finished
   # gestuer = getGesture(palms, hands)

    if faces is not None:
        best_face = faces[0] # The face vector is sorted based on quality already, The first one is the best
        deltaArray = Delta.get_delta(best_face)
        active_quality = quality

        data_queue.send_to_queue(deltaArray)

    display1.display_frame(frames[1], faces, active_quality[0], deltaArray)

    if cv2.waitKey(5) & 0xFF == 27:
            break

# Do we need to add this line somewhere? Maybe in delta function
            # This line sends the delta values to the action.py file
#            on_target_update(delta[0], delta[1])