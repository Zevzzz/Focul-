from playsound import playsound

isMuted = False

def playBeepSFX():
    if not isMuted:
        playsound('beep.mp3')

