__author__ = 'root'
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time

mouse = PyMouse()
keyboard = PyKeyboard()

while 1:
    print(mouse.position())
    time.sleep(0.5)