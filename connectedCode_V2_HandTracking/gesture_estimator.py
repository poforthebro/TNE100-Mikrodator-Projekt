import numpy as np

# CLass to guestimate the gesture of the hand
class get_Gesture():

    # Define and initilize each use of the class with these settings
    def __init__(self):
        print("Initilizing Gesture Guesser")


    def _vector_2_angle(self, v1, v2):
        uv1 = v1 / np.linalg.norm(v1)
        uv2 = v2 / np.linalg.norm(v2)
        angle = np.degrees(np.arccos(np.dot(uv1, uv2)))
        return angle

    def _hand_angle(self, hand):
        angle_list = []
        # thumb
        angle_ = self._vector_2_angle(
            np.array([hand[0][0] - hand[2][0], hand[0][1] - hand[2][1]]),
            np.array([hand[3][0] - hand[4][0], hand[3][1] - hand[4][1]])
        )
        angle_list.append(angle_)
        # index
        angle_ = self._vector_2_angle(
            np.array([hand[0][0] - hand[6][0], hand[0][1] - hand[6][1]]),
            np.array([hand[7][0] - hand[8][0], hand[7][1] - hand[8][1]])
        )
        angle_list.append(angle_)
        # middle
        angle_ = self._vector_2_angle(
            np.array([hand[0][0] - hand[10][0], hand[0][1] - hand[10][1]]),
            np.array([hand[11][0] - hand[12][0], hand[11][1] - hand[12][1]])
        )
        angle_list.append(angle_)
        # ring
        angle_ = self._vector_2_angle(
            np.array([hand[0][0] - hand[14][0], hand[0][1] - hand[14][1]]),
            np.array([hand[15][0] - hand[16][0], hand[15][1] - hand[16][1]])
        )
        angle_list.append(angle_)
        # pink
        angle_ = self._vector_2_angle(
            np.array([hand[0][0] - hand[18][0], hand[0][1] - hand[18][1]]),
            np.array([hand[19][0] - hand[20][0], hand[19][1] - hand[20][1]])
        )
        angle_list.append(angle_)
        return angle_list

    def _finger_status(self, lmList):
        fingerList = []
        originx, originy = lmList[0]
        keypoint_list = [[5, 4], [6, 8], [10, 12], [14, 16], [18, 20]]
        for point in keypoint_list:
            x1, y1 = lmList[point[0]]
            x2, y2 = lmList[point[1]]
            if np.hypot(x2 - originx, y2 - originy) > np.hypot(x1 - originx, y1 - originy):
                fingerList.append(True)
            else:
                fingerList.append(False)

        return fingerList



    def _classify(self, hand):
        thr_angle = 65.
        thr_angle_thumb = 30.
        thr_angle_s = 49.
        gesture_str = "Undefined"

        angle_list = self._hand_angle(hand)

        thumbOpen, firstOpen, secondOpen, thirdOpen, fourthOpen = self._finger_status(hand)
        # Number
        if (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle) and \
                not firstOpen and not secondOpen and not thirdOpen and not fourthOpen:
            gesture_str = "Zero"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle) and \
                firstOpen and not secondOpen and not thirdOpen and not fourthOpen:
            gesture_str = "One"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle) and \
                not thumbOpen and firstOpen and secondOpen and not thirdOpen and not fourthOpen:
            gesture_str = "Two"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] > thr_angle) and \
                not thumbOpen and firstOpen and secondOpen and thirdOpen and not fourthOpen:
            gesture_str = "Three"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle) and \
                firstOpen and secondOpen and thirdOpen and fourthOpen:
            gesture_str = "Four"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s) and \
                thumbOpen and firstOpen and secondOpen and thirdOpen and fourthOpen:
            gesture_str = "Five"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s) and \
                thumbOpen and not firstOpen and not secondOpen and not thirdOpen and fourthOpen:
            gesture_str = "Six"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle_s) and \
                thumbOpen and firstOpen and not secondOpen and not thirdOpen and not fourthOpen:
            gesture_str = "Seven"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle) and (angle_list[2] < thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle_s) and \
                thumbOpen and firstOpen and secondOpen and not thirdOpen and not fourthOpen:
            gesture_str = "Eight"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle) and (angle_list[2] < thr_angle) and (
                angle_list[3] < thr_angle) and (angle_list[4] > thr_angle_s) and \
                thumbOpen and firstOpen and secondOpen and thirdOpen and not fourthOpen:
            gesture_str = "Nine"

        return gesture_str

    

    def getGesture(self, hand):
        gesture = self._classify(hand)
        return gesture