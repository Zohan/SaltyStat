__author__ = 'root'
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time
import SaltyIRC
import subprocess

mouse = PyMouse();
keyboard = PyKeyboard();

# Enter your login details below
username=''
email=''
password=''

def logIn():
    global betOn
    mouse.click(754,135)
    time.sleep(10)
    mouse.click(352,485)
    keyboard.type_string(email)
    time.sleep(2)
    mouse.click(340,575)
    keyboard.type_string(password)
    time.sleep(1)
    mouse.click(355,675)
    return 1

def loadBrowser():
    browser = subprocess.Popen(['epiphany', 'www.saltybet.com/'], stdout=0, stdin=subprocess.PIPE)
    return browser


loadBrowser()
time.sleep(10)
logIn()
time.sleep(20)
print("Logged in?")
while(1):
    SaltyIRC.setup()
    SaltyIRC.mainLoop()



