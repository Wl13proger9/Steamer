#pyinstaller steamer1.7.py --onefile --add-data "commands.py;." --add-data "data.txt;." --hidden-import=commands
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



def tran(lang,id):
    
    ru = {
        "1": '''
--------help--------
Просто введи ID или URL игры для добавления из ДатаБазы..
1) /help - показывает этот текстик
2) /about - показывает об программе
3) /rm <ID> - убирает игру с ID
4) /bye - выход
5) /restart - перезапуск Steam
6) /setpath - установление папки для Steam
7) /clear - стирает консоль
8) /mygames - показывает ваши игры
9) /autoset - автоматически устанавливает папку Steam
10 /c - убирает всякие цвета
11) /lang - устанавливает язык [1 = ru/2 = eng]
12) /fixes - устанавливает фиксы
----------------------
''',
        
        "2": f'''
--------about--------
-сделано: WL13Proger9
-билд: {version_build}
-версия: {version}
-url проекта: https://github.com/Wl13proger9/Steamer
-games.zip архив:               
  mega:        \033[1mhttps://mega.nz/file/EchSlZLL#BbT7-qtm26ZnaTpzpj0AjgNemHh6av68MyAN7IuTfOE\033[0m
  google disk: \033[1mhttps://drive.google.com/file/d/1-lZ0OJGEFUd9kEHfWaJEjk1zYU894J1L/view?usp=drive_link\033[0m
----------------------
''',

        "3": 'Перезапустить Steam?[y/n]>',

        "4": "Готово!",

        "5": "Вы хотите убрать:",

        "6": "с ID:",

        "7": "Ваша прошлая Steam папка:",

        "8": "Пожалуйста подождите...",

        "9": "Ваши игры:",

        "10": "Введите ID игры к который вы хотите добавить достижения: ",

        "11": "Используйте только [1 = ru/2 = eng]!",

        "12": "Комманд <{world}> не найдено...",

        "13": "Вы хотите добавить игру",

        "14": "Игра с ID ",

        "15": "не найдено...",

        "16": "Введите ID с листа>",

        "17": "Папка <fix> не найдена, вы можете скачать ее с github",

        "18": "Вот ссылка: \033[1mhttps://github.com/Wl13proger9/Steamer\033[0m",

        "19": "Вы не имеете папку с патчем, просто скачайте ее с github",

        "20": "Нажмите Enter для выхода..",
        
        "21": "games.zip не найдено!",

        "22": "Вы должны скачать Дата Базу:",

        "23": "data.txt не ннайден! Пожалуйста подождите...",

        "24": "Дата База не найдена! Пожалуйста подождите...",

    }


    eng = {
        "1": '''
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
11) /lang - changing language [1 = ru/2 = eng]
12) /fixes - downloading fixes
----------------------
''',

        "2": f'''
--------about--------
-made by: WL13Proger9
-build: {version_build}
-version: {version}
-project url: https://github.com/Wl13proger9/Steamer
-games.zip archive:               
  mega:        \033[1mhttps://mega.nz/file/EchSlZLL#BbT7-qtm26ZnaTpzpj0AjgNemHh6av68MyAN7IuTfOE\033[0m
  google disk: \033[1mhttps://drive.google.com/file/d/1-lZ0OJGEFUd9kEHfWaJEjk1zYU894J1L/view?usp=drive_link\033[0m
----------------------
''',

        "3": 'Restart Steam?[y/n]>',

        "4": "Done!",

        "5": "You want remove:",

        "6": "with ID:",

        "7": "Your past Steam path:",

        "8": "Please wait...",

        "9": "Your games:",

        "10": "Enter ID you want to add achievment: ",

        "11": "Print only [1 = ru/2 = eng]!",

        "12": "Command <{world}> not found...",

        "13": "You want add game",

        "14": "Game with ID ",

        "15": "not found...",

        "16": "Enter ID from list you want>",
        
        "17": "Path <fix> not exist, you can downlaod it from github",

        "18": "Here is the link: \033[1mhttps://github.com/Wl13proger9/Steamer\033[0m",

        "19": "So you haven't repatch folder, just download it from github",

        "20": "Press Enter to exit..",

        "21": "games.zip not found!",

        "22": "You need to download DataBase:",

        "23": "data.txt not found! Please wait...",

        "24": "DataBase not found! Please wait...",
        
    }




    if lang == 1:
       return  ru.get(str(id)) 
    else:
        return eng.get(str(id))


if txt.get("data.txt","steam-path") == None:
    txt.set("data.txt","\nsteam-path",get_steam_path())


if txt.get("data.txt","hi") == None:
    txt.set("data.txt","\nhi","Made by: WL13Proger9")  


if txt.get("data.txt","c") == None:
    txt.set("data.txt","\nc","0")  


if not os.path.exists("./DataBase/"):
    print(f"{commands.no}{tran(lang,'24')}")
    os.makedirs("./DataBase/")


if not os.path.exists("./data.txt"):
    print(f"{commands.no}{tran(lang,'23')}")
    with open("data.txt", "w") as file:
        file.write('steam-path - \nhi - Made by WL13Proger9\nc = 0')
        file.close()


if not os.path.exists("./DataBase/games.zip"):
    print(f'''{commands.no}{tran(lang,'21')}
{commands.no}{tran(lang,'22')}
{commands.hm}mega:        \033[1mhttps://mega.nz/file/EchSlZLL#BbT7-qtm26ZnaTpzpj0AjgNemHh6av68MyAN7IuTfOE\033[0m
{commands.hm}google disk: \033[1mhttps://drive.google.com/file/d/1-lZ0OJGEFUd9kEHfWaJEjk1zYU894J1L/view?usp=drive_link\033[0m
''')
    input(f"{commands.hm}{tran(lang,'20')}")
    quit()


if not os.path.exists("./hellyeah/"):
    print(f"{commands.hm}{tran(lang,'19')}")


if not os.path.exists("./fix"):
    print(f"{commands.hm}{tran(lang,'17')}")
    print(f"{commands.hm}{tran(lang,'18')}")


if txt.get("data.txt","c") == "0":
    commands.no   = ('\033[31m' + '[!]'+'\033[39m') #no
    commands.yes  = ('\033[32m' + '[+]'+'\033[39m') #yes
    commands.what = ('\033[34m' + '[?]'+'\033[39m') #what
    commands.hm   = ('\033[35m' + '[-]'+'\033[39m') #hm
else:
    commands.no = ""
    commands.yes = ""
    commands.hm = ""
    commands.what = ""



lang = 0 #1 - ru, 2 - en
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
            


version_build = "11/03/25cmd"
version = "1.7 Beta"
        
print(text2art("Steamer v1.7 Beta"))
print(txt.get("data.txt","hi")) 




def main():
    global lang 
    while True:
        try:
            st_path = txt.get("data.txt","steam-path")
            world = input("[/help]> ")


            if "/help" in world:    
                print(tran(lang, "1"))


            elif "/bye" in world:
                break


            elif "/about" in world:
                print(tran(lang, "2"))
                

            elif "/clear" in world:
                os.system('cls' if os.name == 'nt' else 'clear')


            elif "/rm" in world:
        
                if check_file_in_folder(f'{st_path}/config/stplug-in', f"{search(rm(world))}.st") == True:
                
                       
                    if input(f"{commands.what}{tran(lang,'5')}<{get_name_by_id(f'{search(rm(world))}.st')}>{tran(lang,'6')} <{search(rm(world))}>?  [y/n]> ") == "y":
                        os.remove(f"{st_path}/config/stplug-in/{search(rm(world))}.st")

                        print(f"{commands.yes}{tran(lang, '4')}")
    
                        if input(f"{commands.what}{tran(lang, '3')} ")  == "y":restart_st()
                        else:continue
                        

                    else:continue
                    
                        


                else:
                    
                    if lang == 1:print(f'{commands.no}Игра с ID {search(rm(world))} не найдена...')
                    else:print(f'{commands.no}Game with ID {search(rm(world))} not found...')


            elif "/restart" in world:
                restart_st()


            elif "/setpath" in world:
                print(f"{commands.hm} {tran(lang,'7')}",st_path)
                select_folder() 
                print(f"{commands.yes}{tran(lang, '4')}")

   
            elif "/mygames" in world:
                #os.walk(f"{st_path}/config/stplug-in")
                print(f"{commands.hm}{tran(lang,'9')}")
                for root, dirs, files in os.walk(f"{st_path}/config/stplug-in"):
                    for file in files:
                        if file.endswith(".st"):
                            print(f"{commands.hm}ID: {file.split('.')[0]} - {get_name_by_id(file)}")


            elif "/autoset" in world:
                print(f"{commands.yes}{tran(lang, '8')}")   
                txt.set("data.txt","\nsteam-path",get_steam_path())
                print(f"{commands.yes}{tran(lang, '4')}")


            elif "/c" in world:
                
                if txt.get("data.txt","c") == "0":
                    commands.no   = ('\033[31m' + '[!]'+'\033[39m') #no
                    commands.yes  = ('\033[32m' + '[+]'+'\033[39m') #yes
                    commands.what = ('\033[34m' + '[?]'+'\033[39m') #what
                    commands.hm   = ('\033[35m' + '[-]'+'\033[39m') #hm
                    txt.set("data.txt","c","1")  
                else:
                    commands.no = ""
                    commands.yes = ""
                    commands.hm = ""
                    commands.what = ""
                    txt.set("data.txt","c","0")  
               
                #print(f"{commands.yes}Done!")
                print(f"{commands.yes}{tran(lang, '4')}")


            elif world.startswith("/lang"):
                
                match = re.search(r'/lang\s*(\d+)', world)


                if match:
                    #print(match.group(1))
                    

                    if match.group(1) == "1":
                        lang = 1
                        print(f"{commands.yes}{tran(lang, '4')}")

                    elif match.group(1) == "0":
                        lang = 0
                        print(f"{commands.yes}{tran(lang, '4')}")

                    else:
                        print(f"{commands.hm}{tran(lang,'11')}")


            elif world.startswith("/fixes"):
                print('''1) [1] - Grand Theft Auto IV
2) [2] - Grand Theft Auto V
3) [3] - Red Dead Redemption 1
4) [4] - Red Dead Redemption 2''')

                what_fix = input(f"{commands.what}{tran(lang,'16')} ")


                root = tk.Tk()
                root.withdraw()  
                folder_selected = filedialog.askdirectory()  
                if folder_selected:fixers(what_fix,folder_selected)




            else:
                
                if world.startswith("/"):
                    print(f"{commands.no}{tran(lang,'12').format(world=world)}")


                    #if lang == 1:print(f"{commands.no}Комманда <{world}> не найдена...")
                    #else:print(f"{commands.no}Command <{world}> not found...")

                
                else:
                
                    if is_game_in_db(search(world)) == True:
                        
                        if input(f"{commands.what}{tran(lang,'13')} <{get_name_by_id(f'{search((world))}.st')}> {tran(lang,'6')} <{search((world))}>?  [y/n]> ") == "y":

                                copy_files_by_type_in_zip(search((world)), 
                                                    f"{st_path}/config/stplug-in", 
                                                    f"{st_path}/config/depotcache")



                                print(f"{commands.yes}{tran(lang, '4')}")

                        else:continue
                        
                        if input(f"{commands.what}{tran(lang,'3')} ")  == "y":restart_st()
                        else:continue

                    else:

                        print(f'{commands.no}{tran(lang,"14")}<{search(world)}> {tran(lang,"15")}')

        except Exception as e:print(e)


if __name__ == "__main__":
    main()


#####ToDo#####
#make installer




