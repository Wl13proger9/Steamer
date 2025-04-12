#python -m eel steamer.py web --onefile --noconsole

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




eel.init("web")


#переменные
version = "1.8.5 alpha"
build = "27/03/25"


#функции
@eel.expose
def do():
    print("Hello world")


@eel.expose
def get_version():
    return version


@eel.expose
def db():
    if not haveDB():return "Sorry, you didnt have game db"
    else:return "You have game db"


def out(text):
    print(text)


#https://steamcommunity.com/profiles/76561199062880240/




#1250/800 is default
#min is 1000/600
#max is your fullscreen
'''
----THIS IS CUT CONTENT----

<div id="ent">
    <input id="entr" type="text" placeholder="enter ID">
    <button class="icon-button" onclick="eel.restart_st()">
        <img src="icons/restart.png" width="30px">
    </button>
</div>


<div class="righaaat_container">
    <img id="game-icon" src="icons/non_game.png" />
    <h1 id="game_txt">Games</h1>
</div>


<h1 id="game_txt">name: Metal Gear Solid 1</h1>


<p id="status">status: Added</p>
            '''



eel.start("main.html", size=(1250, 800)) 