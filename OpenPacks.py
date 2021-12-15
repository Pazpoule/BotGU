from pyautogui import *
import pyautogui, sys
import time
import keyboard
import random
import win32api, win32con

x, y = pyautogui.position()
print(x, y)

time.sleep(1)

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
def dragNDrop(x, y, xfin, yfin):
    win32api.SetCursorPos((x, y))
    time.sleep(0.01)
    pyautogui.dragTo(xfin, yfin, 0.2, button='left')

compteurPack =0
while keyboard.is_pressed('q') == False:
    pack = pyautogui.locateOnScreen('Pack.png', grayscale=True, confidence=0.6)
    emplacementPack = pyautogui.locateOnScreen('emplacementPack.png', grayscale=True, confidence=0.6)
    carteGagnee = pyautogui.locateOnScreen('CarteGagnee.png', grayscale=True, confidence=0.6)
    nextPack = pyautogui.locateOnScreen('nextPack.png', grayscale=True, confidence=0.6)

    if pack != None:
        print("Click Pack")
        coordPack = pack.left+70, pack.top+70
        try:
            dragNDrop(coordPack[0], coordPack[1], emplacementPack.left+70, emplacementPack.top+20)
        except:
            print("wait")
        time.sleep(0.1)
    if carteGagnee != None:
        print("Click Carte")
        coordCart = carteGagnee.left+70, carteGagnee.top+70
        click(coordCart[0], coordCart[1])
    if nextPack != None:
        print("Click Next Pack")
        coordNext = nextPack.left+5, nextPack.top+5
        click(coordNext[0], coordNext[1])
        compteurPack += 1
        time.sleep(0.5)
print("Nombre de pack : ", compteurPack)

































