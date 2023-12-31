import mediapipe as mp
import cv2
import time
import numpy as np
from RecordPosture import recordPostureAll, recordPostureSelected
cv2.PAUSE = 0
mp.PAUSE = 0
np.PAUSE = 0

def setWantedPoints(isFocused, durationMin, fps, page): #use during the set up data for the NN
    focusType = 0 if isFocused else 1
    points = recordPostureAll(durationMin, fps, page)
    wanted = []

    for i in range(33):
        count = 0
        for data in points:
            point = data[i]
            vis = point.get("Visibility")
            if vis >= 0.5:
                count += 1
        if count/(len(points)) > 0.9:
            wanted.append(i)
    pointStr = ''
    for i in range(len(points)):
        pointStr += str(focusType) + ' '
        for num in wanted:
            if points[i][num].get("Visibility") > 0.5:
                 pointStr += str(points[i][num].get('x')) + ' ' + str(points[i][num].get('y')) + ' ' + str(points[i][num].get('z')) + ' '
            else:
                break
        pointStr += '\n'

    with open('points.txt', 'a') as file:
        if isFocused:
            for num in wanted:
                file.write(str(num) + " ")
        file.write("\n")
        file.write(str(pointStr) + '\n')

    file.close()



def testVideo(fps, page, finalConf = None): #use during the live video
    return recordPostureSelected(fps, page, finalConf)
