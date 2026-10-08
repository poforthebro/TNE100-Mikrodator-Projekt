import cv2 as cv
import numpy as np
from mp_handpose import MPHandPose
from mp_palmdet import MPPalmDet

class handTracking:

    # Define and initilize each use of the class with these settings
    def __init__(self):
        self.handpose_model_path =  'models/face_detection_yunet.onnx',
        self.palm_detector = None
        self.handpose_detector = None
        

        print("Initilizing hand tracking hardware")

        backend_id = cv.dnn.DNN_BACKEND_OPENCV
        target_id = cv.dnn.DNN_TARGET_CPU
        
        # palm detector
        self.palm_detector = MPPalmDet(
                    modelPath='models/palm_detection_mediapipe_2023feb.onnx',
                    nmsThreshold=0.3,
                    scoreThreshold=0.6,
                    backendId=backend_id,
                    targetId=target_id
                    )
        
        
        # handpose detector
        self.handpose_detector = MPHandPose(
            modelPath='models/handpose_estimation_mediapipe_2023feb.onnx',
                        confThreshold=0.6,
                        backendId=backend_id,
                        targetId=target_id
                        )



    def getHandCoordinates(self, image):
        # Palm detector inference
        palms = self.palm_detector.infer(image)
        hands = np.empty(shape=(0, 132))

        # Estimate the pose of each hand
        for palm in palms:
            # Handpose detector inference
            handpose = self.handpose_detector.infer(image, palm)
            if handpose is not None:
                hands = np.vstack((hands, handpose))
        
        return self.sortHands(hands, palms)



    def sortHands(self, hands, palms):
        # Sort using the quality score function below
        hands = sorted(hands, key=get_quality_score, reverse=True)
        palms = sorted(palms, key=get_quality_score, reverse=True)
        
        # Format the 132-value array into a 21x3 coordinate array for the gesture estimator
        formatted_hands = []
        for hand in hands:
            landmarks = hand[4:67].reshape(21, 3)[:, :2]
            formatted_hands.append(landmarks)
            
        # Returning PALMS first, then HANDS to match your main.py file!
        return palms, formatted_hands



def get_quality_score(hand):
    Q_indicies = 13
    width = hand[2]
    height = hand[3]
    confidence = hand[Q_indicies]

    area = height * width
    q = area * confidence

    return q


'''
    # Get function with more output parameters 

    def get_hand_coordinates(self, image):
        # Palm detector inference
        palms = self.palm_detector.infer(image)
        hands = []

        # Estimate the pose of each hand
        for palm in palms:
            # Handpose detector inference
            handpose = self.handpose_detector.infer(image, palm)
            if handpose is not None:
                landmarks_screen = handpose[4:67].reshape(21, 3).astype(np.int32)
                landmarks_world = handpose[67:130].reshape(21, 3)
                hands.append({
                    'screen': landmarks_screen,
                    'world': landmarks_world
                })

        return palms, hands
    
    '''


    