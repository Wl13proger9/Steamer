#python -m eel steamer.py web --onefile --icon=icon.ico
import eel
import os
from commands import *
import re
import winreg
import webbrowser


import ctypes

def hideConsole():
  whnd = ctypes.windll.kernel32.GetConsoleWindow()
  if whnd != 0:
     ctypes.windll.user32.ShowWindow(whnd, 0)

hideConsole()


import sys
if sys.stderr is None:
    import io
    sys.stderr = io.StringIO()
if sys.stdout is None:
    import io
    sys.stdout = io.StringIO()





eel.init("web")


#переменные
version = "1.8.6 alpha"
build = "02/05/25"


#функции
@eel.expose
def do():
    print("Hello world")


@eel.expose
def get_version():
    return version


#@eel.expose
#def db():
    #if not haveDB():return "Sorry, you didnt have game db"
    #else:return "You have game db"


def out(text):
    print(text)


#https://steamcommunity.com/profiles/76561199062880240/






def hellyeah():
    repa = []
    if  not os.path.exists(f"{data.get('st_path')}/hid.dll"):repa.append("hid.dll")
    if  not os.path.exists(f"{data.get('st_path')}/config/stUI/Steamtools.exe"):repa.append("Steamtools.exe")
    if  not os.path.exists(f"{data.get('st_path')}/config/stplug-in/luapacka.exe"):repa.append("luapacka.exe")
    if  not os.path.exists(f"{data.get('st_path')}/config/stplug-in/Steamtools.st"):repa.append("Steamtools.st")
    if  not os.path.exists(f"{data.get('st_path')}/config/stplug-in/Steamtools.lua"):repa.append("Steamtools.lua")

    
    if not os.path.exists("hellyeah"):
        restore_hy("https://github.com/Wl13proger9/Steamer/releases/download/v0.0/hellyeah.zip", "hellyeah.zip")
    
    patch_st(repa)



hellyeah()


#1200/700 is default
#min is 800/600
#semi is 1600/800
#max is your fullscreen



eel.start("main.html", size=(1200, 700)) 

