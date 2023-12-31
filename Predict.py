
from keras import models
import ctypes
import SFXPlayer
import PopupManager
from LandmarkLogger import testVideo
from time import time
from flet import *
import flet as ft
import cv2
from tkinter import messagebox

num = 0
with open(r'slouchCounter.txt', 'r') as slouchFile:
    numberCount = int(slouchFile.read())

model = models.load_model('model.h5')

running = True

def goHome(e):
    global running
    running = False
def toggleMute(e):
    SFXPlayer.isMuted = not SFXPlayer.isMuted
def togglePopup(e):
    PopupManager.isShowPopup = not PopupManager.isShowPopup

def predict(data):
    prediction = model.predict(data)[0][0]
    return 'FOCUSED' if prediction < 0.5 else 'UNFOCUSED', prediction

def runModel(page, functs):
    global numberCount, num, running


    lastConf = 0

    startTime = time()

    while running:
        num += 1
        points = testVideo(10, page, lastConf) #run the live video thingy

        img = ft.Image(
            src=f'picture{num}.png',
            width=300,
            height=300,
            fit=ft.ImageFit.CONTAIN,
        )

        page.clean()
        page.title = 'Run'
        if SFXPlayer.isMuted and PopupManager.isShowPopup:
            buttonMute: ElevatedButton = ElevatedButton(text='Turn On Sound', width=150, height=50)
            buttonPop: ElevatedButton = ElevatedButton(text='Disable Popup', width=150, height=50)
        elif SFXPlayer.isMuted and not PopupManager.isShowPopup:
            buttonMute: ElevatedButton = ElevatedButton(text='Turn On Sound', width=150, height=50)
            buttonPop: ElevatedButton = ElevatedButton(text='Enable Popup', width=150, height=50)
        elif not SFXPlayer.isMuted and PopupManager.isShowPopup:
            buttonMute: ElevatedButton = ElevatedButton(text='Turn Off Sound', width=150, height=50)
            buttonPop: ElevatedButton = ElevatedButton(text='Disable Popup', width=150, height=50)
        elif not SFXPlayer.isMuted and not PopupManager.isShowPopup:
            buttonMute: ElevatedButton = ElevatedButton(text='Turn Off Sound', width=150, height=50)
            buttonPop: ElevatedButton = ElevatedButton(text='Enable Popup', width=150, height=50)

        buttonBack: ElevatedButton = ElevatedButton(text='Back', width=150, height=50)
        page.add(img, buttonMute, buttonPop, buttonBack)
        buttonMute.on_click = toggleMute
        buttonPop.on_click = togglePopup
        buttonBack.on_click = goHome

        if len(points) > 0 and len(points[0]) > 0:
            pred, value = predict(points)
            print(f'Prediction: {value}')
            lastConf = value

            if pred == 'FOCUSED':
                startTime = time()
            print(startTime)

            print(pred)

            if (time() - startTime) > 15:
                SFXPlayer.playBeepSFX()

                numberCount += 1
                with open('slouchCounter.txt', 'w') as overWrite:
                    overWrite.write(str(numberCount))
                if PopupManager.isShowPopup:
                    functs[2](numberCount)
                startTime = time()

        else:
            print('NO POINTS FOUND')

    cv2.destroyAllWindows()
    functs[0](functs[1])
    running = True


