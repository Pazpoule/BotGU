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
    pyautogui.moveTo(x, y)
    pyautogui.click()

def dragNDrop(x, y, xfin, yfin):
    pyautogui.moveTo(x, y)
    time.sleep(0.01)
    pyautogui.dragTo(xfin, yfin, 0.2, button='left')
    time.sleep(0.01)

compteurDePartie = 0
while keyboard.is_pressed('q') == False:
    boutonPlay = pyautogui.locateOnScreen('play.png', grayscale=True, confidence=0.7, region=(925, 563, 925+500, 563+500))
    pouvoirSLAYER = pyautogui.locateOnScreen('pouvoirSLAYER.png', grayscale=True, confidence=0.6)
    boutonConfirmer = pyautogui.locateOnScreen('boutonConfirmer.png', grayscale=True, confidence=0.6)
    boutonKEEPTHESE = pyautogui.locateOnScreen('boutonKEEPTHESE.png', grayscale=True, confidence=0.6)
    boutonKEEPTHESE2 = pyautogui.locateOnScreen('youhave.png', grayscale=True, confidence=0.6)
    boutonTourSuivant = pyautogui.locateOnScreen('boutonTourSuivant.png', grayscale=True, confidence=0.7)
    boutonTourSuivant2 = pyautogui.locateOnScreen('boutonTourSuivant2.png', grayscale=True, confidence=0.6)
    boutonContinuer = pyautogui.locateOnScreen('Continue.png', grayscale=True, confidence=0.6)
    boutonContinuer2 = pyautogui.locateOnScreen('boutonContinueReward.png', grayscale=True, confidence=0.6)
    boutonContinuer3 = pyautogui.locateOnScreen('boutonContinueReward2.png', grayscale=True, confidence=0.6)
    boutonQuit = pyautogui.locateOnScreen('Quit.png', grayscale=True, confidence=0.7)
    boutonArena = pyautogui.locateOnScreen('Arena.png', grayscale=True, confidence=0.7)

    if boutonPlay != None:
        print("Partie lancée")
        pyautogui.click(boutonPlay.left+70, boutonPlay.top+70)

        time.sleep(8)
    if pouvoirSLAYER != None:
        print("Sélectionne SLAYER")
        coordSLAYER = pouvoirSLAYER.left+100, pouvoirSLAYER.top+100
        click(coordSLAYER[0], coordSLAYER[1])
        time.sleep(0.5)
    if boutonKEEPTHESE != None:
        print("Sélectionne KEEP THESE")
        coordKEEPTHESE = boutonKEEPTHESE.left+10, boutonKEEPTHESE.top+10
        click(coordKEEPTHESE[0], coordKEEPTHESE[1])
        compteurDePartie += 1
        time.sleep(1.5)
    if boutonKEEPTHESE2 != None:
        print("Sélectionne KEEP THESE")
        coordKEEPTHESE2 = boutonKEEPTHESE2.left+10, boutonKEEPTHESE2.top+10
        click(coordKEEPTHESE2[0], coordKEEPTHESE2[1])
        time.sleep(0.5)
    if boutonConfirmer != None:
        print("Sélectionne Confirm")
        coordConfirmer = boutonConfirmer.left+20, boutonConfirmer.top+20
        click(coordConfirmer[0], coordConfirmer[1])
        time.sleep(0.5)
    if boutonTourSuivant != None:
        dragNDrop(700, 860, 700, 560)
        dragNDrop(800, 860, 800, 560)
        dragNDrop(900, 860, 900, 560)
        dragNDrop(1000, 860, 1000, 560)
        dragNDrop(1100, 860, 1100, 560)
        dragNDrop(500, 560, 960, 250)
        dragNDrop(600, 560, 960, 250)
        dragNDrop(700, 560, 960, 250)
        dragNDrop(800, 560, 960, 250)
        dragNDrop(900, 560, 960, 250)
        dragNDrop(1000, 560, 960, 250)
        dragNDrop(1100, 560, 960, 250)
        dragNDrop(1200, 560, 960, 250)
        dragNDrop(1300, 560, 960, 250)
        print("Tour passé")
        coordTourSuivant = boutonTourSuivant.left+30, boutonTourSuivant.top+30
        click(coordTourSuivant[0], coordTourSuivant[1])
        time.sleep(0.5)
    if boutonTourSuivant2 != None:
        dragNDrop(700, 860, 700, 560)
        dragNDrop(800, 860, 800, 560)
        dragNDrop(900, 860, 900, 560)
        dragNDrop(1000, 860, 1000, 560)
        dragNDrop(1100, 860, 1100, 560)
        dragNDrop(500, 560, 960, 250)
        dragNDrop(600, 560, 960, 250)
        dragNDrop(700, 560, 960, 250)
        dragNDrop(800, 560, 960, 250)
        dragNDrop(900, 560, 960, 250)
        dragNDrop(1000, 560, 960, 250)
        dragNDrop(1100, 560, 960, 250)
        dragNDrop(1200, 560, 960, 250)
        dragNDrop(1300, 560, 960, 250)

        print("Tour passé")
        coordTourSuivant = boutonTourSuivant2.left+30, boutonTourSuivant2.top+30
        click(coordTourSuivant[0], coordTourSuivant[1])
        time.sleep(0.5)
    if boutonContinuer != None:
        print("Bouton Continuer")
        coordContinuer = boutonContinuer.left+5, boutonContinuer.top+5
        click(coordContinuer[0], coordContinuer[1])
        time.sleep(0.5)
    if boutonContinuer2 != None:
        print("Bouton Continuer2")
        coordContinuer2 = boutonContinuer2.left+20, boutonContinuer2.top+20
        click(coordContinuer2[0], coordContinuer2[1])
        time.sleep(0.5)
    if boutonContinuer3 != None:
        print("Bouton Continuer3")
        coordContinuer3 = boutonContinuer3.left+20, boutonContinuer3.top+20
        click(coordContinuer3[0], coordContinuer3[1])
        time.sleep(0.5)
    if boutonQuit != None:
        print("Bouton Quit")
        coordQuit = boutonQuit.left+5, boutonQuit.top+5
        click(coordQuit[0], coordQuit[1])
        time.sleep(0.5)
    if boutonArena != None:
        print("Bouton Arena")
        coordArena = boutonArena.left+5, boutonArena.top+5
        click(coordArena[0], coordArena[1])
        time.sleep(0.5)
    else:
        print("Waiting")
        time.sleep(0.5)
print("Parties jouées : ", compteurDePartie)






