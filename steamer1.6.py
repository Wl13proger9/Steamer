#pyinstaller steamer1.6.py --onefile --add-data "commands.py;." --add-data "data.txt;." --hidden-import=commands
from commands import *
import re
import zipfile
import os
import time
import subprocess
import zipfile
import os
import shutil
from art import *
import tkinter as tk
from tkinter import filedialog
#import json
import threading
import os
import sys
import itertools
import winreg
import sys
import commands









if txt.get("data.txt","steam-path") == None:
    txt.set("data.txt","\nsteam-path",get_steam_path())






if txt.get("data.txt","hi") == None:
    txt.set("data.txt","\nhi","Made by: WL13Proger9")  






if not os.path.exists("./DataBase/"):
    print(f"{commands.no}DataBase not found! Please wait...")
    os.makedirs("./DataBase/")


if not os.path.exists("./data.txt"):
    print(f"{commands.no}data.txt not found! Please wait...")
    with open("data.txt", "w") as file:
        file.write('steam-path - \nhi - Made by WL13Proger9')
        file.close()


if not os.path.exists("./DataBase/games.zip"):
    print(f'''{commands.no}games.zip not found!
{commands.no}You need to download DataBase:
{commands.hm}mega: \033[1mhttps://mega.nz/file/EchSlZLL#BbT7-qtm26ZnaTpzpj0AjgNemHh6av68MyAN7IuTfOE\033[0m
{commands.hm}google disk: \033[1mhttps://drive.google.com/file/d/1-lZ0OJGEFUd9kEHfWaJEjk1zYU894J1L/view?usp=drive_link\033[0m
''')
    input(f"{commands.hm}Press Enter to exit..")
    quit()


if not os.path.exists("./hellyeah/"):
    print(f"{commands.hm}So you haven't repatch folder, just download it from github")




repa = []
if  not os.path.exists(f"{txt.get('data.txt','steam-path')}/hid.dll"):repa.append("hid.dll")
if  not os.path.exists(f"{txt.get('data.txt','steam-path')}/config/stUI/Steamtools.exe"):repa.append("Steamtools.exe")
if  not os.path.exists(f"{txt.get('data.txt','steam-path')}/config/stplug-in/luapacka.exe"):repa.append("luapacka.exe")
if  not os.path.exists(f"{txt.get('data.txt','steam-path')}/config/stplug-in/Steamtools.st"):repa.append("Steamtools.st")
if  not os.path.exists(f"{txt.get('data.txt','steam-path')}/config/stplug-in/Steamtools.lua"):repa.append("Steamtools.lua")



if repa != []:
    print(f"{commands.no}Your steam not patched!")
    if input(f"{commands.what} Do you want to patch it?[y/n]> ") == "y":
            patching(repa)
            #print(f"{yes}Done, now you need to restart it")
            print(f"{yes}Done!\n{commands.hm} If something went wrong, just restart it")
            



    
        
print(text2art("Steamer v1.6"))
print(txt.get("data.txt","hi")) 



def main():
    while True:
        try:
            st_path = txt.get("data.txt","steam-path")
            world = input("[/help]> ")

            if "/help" in world:
                print('''
--------help--------
Just enter game ID or URL to add game from DB..
1) /help - show this message
2) /about - show about
3) /rm <ID> - remove game with ID
4) /bye - exit
5) /restart - restart Steam
6) /setpath - set path to Steam
7) /clear - clear console
8) /mygames - show your games
9) /autoset - auto set path to Steam
10 /c - removing any colors
----------------------
''')


            elif "/bye" in world:
                break


            elif "/about" in world:
                print('''
--------about--------
-made by WL13Proger9
-build: 16/02/25cmd
-version: 1.6 standalone
-project url: https://github.com/Wl13proger9/Steamer
-games.zip archive:               
  mega: \033[1mhttps://mega.nz/file/EchSlZLL#BbT7-qtm26ZnaTpzpj0AjgNemHh6av68MyAN7IuTfOE\033[0m
  google disk: \033[1mhttps://drive.google.com/file/d/1-lZ0OJGEFUd9kEHfWaJEjk1zYU894J1L/view?usp=drive_link\033[0m
----------------------
''')


            elif "/clear" in world:
                os.system('cls' if os.name == 'nt' else 'clear')


            elif "/rm" in world:
                #res = search(rm(world))
                #393080
                if check_file_in_folder(f'{st_path}/config/stplug-in', f"{search(rm(world))}.st") == True:
                

                    if input(f"{commands.what}You want remove: <{get_name_by_id(f'{search(rm(world))}.st')}> with ID: <{search(rm(world))}>?  [y/n]> ") == "y":

                        os.remove(f"{st_path}/config/stplug-in/{search(rm(world))}.st")

                        print(f"{commands.yes}Done!")

                        if input(f"{commands.what}Restart Steam?[y/n]> ")  == "y":restart_st()
                        else:continue
                    else:continue
                else:
                    print(f'{commands.no}Game with ID {search(rm(world))} not found...')


            elif "/restart" in world:
                restart_st()


            elif "/setpath" in world:
                print(f"{commands.hm}Your past path to Steam: ",st_path)
                select_folder() 
                print(f"{commands.yes}Done!")

   
            elif "/mygames" in world:
                #os.walk(f"{st_path}/config/stplug-in")
                print("Your games:")
                for root, dirs, files in os.walk(f"{st_path}/config/stplug-in"):
                    for file in files:
                        if file.endswith(".st"):
                            print(f"{commands.hm}ID: {file.split('.')[0]} - {get_name_by_id(file)}")


            elif "/autoset" in world:
                print(f"{commands.hm}Please wait...")
                txt.set("data.txt","\nsteam-path",get_steam_path())
                print(f"{commands.yes}Done!")


            elif "/c" in world:
                no = ""
                yes = ""
                hm = ""
                what = ""
                print(f"{yes}Done!")


            else:
                
                if world.startswith("/"):print(f"{commands.no}Command <{world}> not found...")
                
                else:
                    if is_game_in_db(search(world)) == True:
                        
                        if input(f"{commands.what}You want add game <{get_name_by_id(f'{search((world))}.st')}> with ID: <{search((world))}>?  [y/n]> ") == "y":
                            copy_files_by_type_in_zip(search((world)), 
                                                f"{st_path}/config/stplug-in", 
                                                f"{st_path}/config/depotcache")
                            print(f"{commands.yes}Done!")
                            if input(f"{commands.what}Restart Steam?[y/n]> ")  == "y":restart_st()
                            else:continue

                    else:
                        print(f'{commands.no}Game with ID {search(world)} not found...')


        except Exception as e:print(e)


if __name__ == "__main__":
    main()

#268500

