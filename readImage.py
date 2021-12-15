import pyautogui
from PIL import Image
from pytesseract import *
import cv2

pytesseract.tesseract_cmd = r'C:\Users\zpaul\PycharmProjects\BotGU\tesseract\tesseract.exe'
img = cv2.imread('zero.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
string = pytesseract.image_to_string(img)
boxes = pytesseract.image_to_boxes(img)

print(string, boxes)

output = pytesseract.image_to_string(img)
print(output)

# cv2.imshow('result', img)

