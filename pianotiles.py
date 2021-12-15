from pyautogui import *
import pyautogui, sys
import time
import keyboard
import random
import win32api, win32con

x, y = pyautogui.position()
print(x, y)
# im = pyautogui.screenshot()
# print(im.getpixel(pyautogui.position()))


# Tile 1 Position: X:  603 Y:  690 RGB: ( 77,  80, 115)
# Tile 2 Position: X:  688 Y:  690 RGB: (  0,   0,   0)
# Tile 3 Position: X:  777 Y:  690 RGB: ( 79,  82, 116)
# Tile 4 Position: X:  861 Y:  690 RGB: ( 80,  83, 116)

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)  # This pauses the script for 0.1 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


while keyboard.is_pressed('q') == False:

    if pyautogui.pixel(603, 600)[0] == 0:
        click(603, 600)
    if pyautogui.pixel(688, 600)[0] == 0:
        click(688, 600)
    if pyautogui.pixel(777, 600)[0] == 0:
        click(777, 600)
    if pyautogui.pixel(862, 600)[0] == 0:
        click(862, 600)