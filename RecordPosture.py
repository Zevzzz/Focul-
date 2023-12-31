import mediapipe as mp
import cv2
import time
import flet as ft
from flet import *
import os

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
num = 0

def recordPostureAll(duration, fps, page): #use during recording data for the NN, duration is in the form of min when being inputted
    global num


    mp_pose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils

    pose = mp_pose.Pose(
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)
    points = []
    tempP = []
    startT = time.time()

    success, frame = cap.read()

    num = 0
    while len(points)/fps <= duration * 60:
        num += 1
        success, frame = cap.read()

        if not success:
            break
        frame = cv2.resize(frame, (640, 480))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb_frame)

        mpDraw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        if not result.pose_landmarks:
            pass
        elif time.time() - startT > 1 / int(fps):
            startT = time.time()
            for id, lm in enumerate(result.pose_landmarks.landmark):
                tempP.append({"x": lm.x, "y": lm.y, "z": lm.z, "Visibility": lm.visibility})
                x = int(lm.x * 640)
                y = int(lm.y * 480)
                cv2.circle(frame, (x, y), 1, (255, 0, 255), -1)
            points.append(tempP)
            tempP = []

        conf = round(100*len(points)/fps/(duration*60), 2)
        conf = 100.00 if conf > 100 else conf
        cv2.putText(frame, f"[{conf}%]", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        key = cv2.waitKey(33)

        if page:
            cv2.imwrite(f'pic{num}.png', frame)
            img = ft.Image(
                src=f'pic{num}.png',
                width=300,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            )
            page.clean()
            page.title = 'Record'
            page.add(img)
            page.update()

        else:
            cv2.imshow('Preview', frame)
    for i in range(1, num+1):
        os.remove(f'pic{i}.png')

    cv2.destroyAllWindows()
    return points

def recordPostureSelected(fps, page, finalConf = None): #use during the live video, infinite kinda useless rn can delete if want
    global num
    num+=1

    mp_pose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils

    pose = mp_pose.Pose(
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)
    points = []
    tempP = []
    startT = time.time()


    wanted = list(open("points.txt", "r").readline().split(" ")[:-1])
    wanted = list(map(int, wanted))

    success, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb_frame)

    mpDraw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    points = []
    if not result.pose_landmarks:

        pass

    elif time.time() - startT > 1/int(fps):

        startT = time.time()
        for id, lm in enumerate(result.pose_landmarks.landmark):
            if id not in wanted: #checks if point is a significant point
                continue
            tempP.append(lm.x)
            tempP.append(lm.y)
            tempP.append(lm.z)
            x = int(lm.x * 640)
            y = int(lm.y * 480)
            cv2.circle(frame, (x, y), 1, (255, 0, 255), -1)
        points.append(tempP)
        tempP = []

    if finalConf:
        if finalConf > 0.5:
            conf = round((finalConf * 100), 2)
            conf = conf * 1.1 + 10
            conf = conf if conf < 100 else 100.0
            cv2.putText(frame, f"UNFOCUSED [{round(conf, 2)}% conf]", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        else:
            conf = round(((1-finalConf) * 100), 2)
            conf = conf * 1.1 + 10
            conf = conf if conf < 100 else 100.0
            cv2.putText(frame, f"FOCUSED [{round(conf, 2)}% conf]", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imwrite(f"picture{num}.png", frame)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(33)
    page.update()
    os.remove(f'picture{num}.png')

    return points
