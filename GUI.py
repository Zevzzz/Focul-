import flet as ft
from flet import *

import SFXPlayer
import PopupManager
import ctypes

onMute = True

def runGUI():
    import Train
    from LandmarkLogger import setWantedPoints
    from Predict import runModel, predict
    from Train import getData, trainNN
    import tkinter
    from tkinter import messagebox
    from tkinter import ttk
    # from tkinter import *
    from PIL import Image, ImageTk
    import cv2
    from tkinter import Tk
    from tkinter import messagebox

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    infoString = '''Dear User,
    
    Hello! Please select "Record", then “Record Proper” on the homepage to start. You will be scanned for one minute, and during the process, please sit up as straight as possible. Next, please select "Record Improper" and sit in positions that you deem unsuitable, such as leaning to the side and slouching in your seat. These will be used to train the program to understand correct and incorrect positions catered towards you. Finally, click “Run” to let the program do its magic!
    
    We hope you have a wonderful experience and a successful use!
    
    Best regards,
    Developers of Focul
    '''

    titleVisibility = True

    slouchWindow = Tk()
    slouchWindow.geometry('0x0')
    slouchWindow.withdraw()


    def main(page: ft.Page) -> None:
        page.fonts = {
            "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
            "Open Sans": "/fonts/OpenSans-Regular.ttf",
            "Aleo Bold Italic": "https://raw.githubusercontent.com/google/fonts/master/ofl/aleo/Aleo-BoldItalic.ttf"
        }
        page.title = 'Home'
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.theme_mode = ft.ThemeMode.DARK
        page.theme = Theme(font_family="Kanit")
        page.window_width = 450
        page.window_height = 650
        page.window_resizable = False
        textTitle: Text = Text("    Focul", width=110, size=25)
        buttonRun: ElevatedButton = ElevatedButton(text='Run', width=150, height=50)
        buttonRecord: ElevatedButton = ElevatedButton(text='Record', width=150, height=50)
        buttonInfo: ElevatedButton = ElevatedButton(text='Info', width=150, height=50)

        def home(e: ControlEvent) -> None:
            page.clean()
            page.title = 'Home'
            textTitle: Text = Text("    Focul", width=110, size=25)
            buttonRun: ElevatedButton = ElevatedButton(text='Run', width=150, height=50)
            buttonRecord: ElevatedButton = ElevatedButton(text='Record', width=150, height=50)
            buttonInfo: ElevatedButton = ElevatedButton(text='Info', width=150, height=50)
            page.add(textTitle,
                     buttonRun,
                     buttonRecord,
                     buttonInfo)
            buttonRun.on_click = run
            buttonRecord.on_click = record
            buttonInfo.on_click = info

        def soundToggle(e: ControlEvent) -> None:
            SFXPlayer.isMuted = not SFXPlayer.isMuted
            page.clean()
            page.title = 'Run'
            buttonLiveVideo: ElevatedButton = ElevatedButton(text="Start Live Video", width=150, height=50)

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
            page.add(buttonLiveVideo, buttonMute, buttonPop, buttonBack)
            buttonMute.on_click = soundToggle
            buttonPop.on_click = visualToggle
            buttonBack.on_click = home
            buttonLiveVideo.on_click = runCVLiveVideo

        def visualToggle(e: ControlEvent) -> None:
            PopupManager.isShowPopup = not PopupManager.isShowPopup
            page.clean()
            page.title = 'Run'
            buttonLiveVideo: ElevatedButton = ElevatedButton(text="Start Live Video", width=150, height=50)

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
            page.add(buttonLiveVideo, buttonMute, buttonPop, buttonBack)
            buttonMute.on_click = soundToggle
            buttonPop.on_click = visualToggle
            buttonBack.on_click = home
            buttonLiveVideo.on_click = runCVLiveVideo

        def info(e: ControlEvent) -> None:
            page.clean()
            page.title = 'Info'
            infoText: Text = Text(infoString, width=300, size=15)

            buttonBack: ElevatedButton = ElevatedButton(text='Back', width=150, height=50)
            page.add(infoText, buttonBack)
            buttonBack.on_click = home

        def record(e: ControlEvent) -> None:
            page.clean()
            page.title = 'Record'
            buttonRecordProper: ElevatedButton = ElevatedButton(text='Record Proper', width=150, height=50)
            buttonRecordImproper: ElevatedButton = ElevatedButton(text='Record Improper', width=150, height=50)
            buttonQuit: ElevatedButton = ElevatedButton(text='Quit', width=150, height=50)
            page.add(buttonRecordProper, buttonRecordImproper, buttonQuit)
            buttonRecordProper.on_click = runCVF
            buttonRecordImproper.on_click = runCVNF
            buttonQuit.on_click = trainModel
            # page.update()
            # setState()

        def runCVF(e: ControlEvent) -> None:
            setWantedPoints(True, 30/60, 30, page)
            record(e)

        def runCVNF(e: ControlEvent) -> None:
            setWantedPoints(False, 30/60, 30, page)
            record(e)

        def trainModel(e: ControlEvent):
            home(e)
            tags, points = Train.getData('points.txt')
            Train.trainNN(tags, points, 'model.h5', 40)

        def run(e: ControlEvent) -> None:
            page.clean()
            page.title = 'Run'
            buttonLiveVideo: ElevatedButton = ElevatedButton(text="Start Live Video", width=150, height=50)

            buttonMute: ElevatedButton = ElevatedButton(text='Turn Off Sound', width=150, height=50)
            buttonPop: ElevatedButton = ElevatedButton(text='Disable Popup', width=150, height=50)
            buttonBack: ElevatedButton = ElevatedButton(text='Back', width=150, height=50)

            page.add(buttonLiveVideo, buttonMute, buttonPop, buttonBack)
            buttonMute.on_click = soundToggle
            buttonPop.on_click = visualToggle
            buttonBack.on_click = home
            buttonLiveVideo.on_click = runCVLiveVideo

        def showPopup(num):
            MessageBox = ctypes.windll.user32.MessageBoxW
            MessageBox(None, f'Warning #{num}\nPlease sit up!', 'Warning!', 0)

        def runCVLiveVideo(e: ControlEvent) -> None:
            global numberCount, slouchFile, showVisualslouch
            runModel(page, [home, e, showPopup])

        home
        page.add(textTitle,
                 buttonRun,
                 buttonRecord,
                 buttonInfo)
        buttonRun.on_click = run
        buttonRecord.on_click = record
        buttonInfo.on_click = info


    ft.app(target=main)
