import mediapipe as mp
from keras import models
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

mp_pose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils
pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)


def runWindowPopUp():

    _, img = cap.read()
    img = cv2.resize(img, (640, 480))

    rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb_frame)
    mpDraw.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # pred = predict(data)
    # pred = 'FOCUSED' if pred == 1 else 'UNFOCUSED'
    #
    #
    # img = cv2.putText(img, pred, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
    cv2.imshow('CV2', img)

    cv2.waitKey(33)