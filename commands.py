import os
import requests
from bs4 import BeautifulSoup
import zipfile
import shutil
import eel
import winreg
import time
import subprocess
import webbrowser
from datetime import datetime
import re#sident evil
import tkinter as tk
from tkinter import messagebox




root = tk.Tk()
root.withdraw()  


zip_path = "DataBase/games.zip"
img_data_path = "DataBase/game-data.txt"
now = datetime.now()
nowt = now.strftime("[%H:%M]")

#'[16:19]transfared: 1488.st to: ./stplug-in/','[16:19]transfared: manifest to: ./depotcache/','[16:19]added: popa games','[16:19]removed: popa games'
textbox_cont = []


#print('\n'.join(textbox_cont))


@eel.expose 
def tbox():
    return textbox_cont


@eel.expose
def tbox_debug():
    textbox_cont.append("test")
    print(textbox_cont)




@eel.expose
def get_st_path():
    try:
        key_path = r"SOFTWARE\Wow6432Node\Valve\Steam"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            steam_path, _ = winreg.QueryValueEx(key, "InstallPath")
            return steam_path
    except FileNotFoundError:
        return None
    

def haveDB():
    return os.path.exists("DataBase/games.zip")



def has_internet():
    try:
        response = requests.get("https://www.google.com", timeout=5)  
        return response.status_code == 200
    except requests.RequestException:return False



def get_steam_avatar(steam_id):
    try:
        if has_internet():
            url = f"https://steamcommunity.com/profiles/{steam_id}/"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:return "web/icons/none.png"
            soup = BeautifulSoup(response.text, "html.parser")
            avatar_img = None
            for img in soup.select(".playerAvatarAutoSizeInner img"):
                if not img.find_parent(class_="profile_avatar_frame"):  
                    avatar_img = img
                    break
            return avatar_img["src"] if avatar_img else "web/icons/none.png"
        else:return 'web/icons/none.png'
    except:return 'web/icons/none.png'



def get_user_id(steam_path):
    loginusers_path = os.path.join(os.path.expanduser(steam_path), "config", "loginusers.vdf")
    if not os.path.exists(loginusers_path): return
    with open(loginusers_path, 'r', encoding='utf-8') as file:lines = file.readlines()
    current_steam_id = None
    steam_id = None
    most_recent = False
    for line in lines:
        line = line.strip() 
        if line.startswith('"') and line[1:18].isdigit(): steam_id = line[1:18]
        if steam_id and '"MostRecent"' in line and '"1"' in line:
            current_steam_id = steam_id
            break
    if current_steam_id: 
        return current_steam_id
    else:
        return "none"

 

@eel.expose
def add_game(file_id): 
    try: 
        with zipfile.ZipFile(zip_path, 'r') as archive:
            found_folder = None
            
            for file in archive.namelist():
                parts = file.split('/')
                if len(parts) > 1 and parts[-1] == f"{file_id}.st": 
                    found_folder = parts[0] 
                    break
            if not found_folder:  
                return None
            if not os.path.exists(get_st_path()+"/config/stplug-in"):os.makedirs(get_st_path()+"/config/stplug-in")
            if not os.path.exists(get_st_path()+"/config/depotcache"):os.makedirs(get_st_path()+"/config/depotcache")
            manifests = 0
            for file in archive.namelist():
                parts = file.split('/')
                
                if parts[0] == found_folder:  
                    if file.endswith('.st'):
                        with archive.open(file) as f:
                            target_path = os.path.join(get_st_path()+"/config/stplug-in", file.split('/')[-1])
                            with open(target_path, 'wb') as out_file:shutil.copyfileobj(f, out_file)
                            textbox_cont.append(f'{nowt}transferred: {file} to: ./config/stplug-in/')
                    elif file.endswith('.manifest'):
                        with archive.open(file) as f:
                            target_path = os.path.join(get_st_path()+"/config/depotcache", file.split('/')[-1])
                            with open(target_path, 'wb') as out_file:shutil.copyfileobj(f, out_file)
                            manifests += 1

            textbox_cont.append(f'{nowt}transferred: {manifests} manifests files to: ./config/depotcache/')
            textbox_cont.append(f'{nowt}added game with ID <{file_id}> to your library, enjoy it')

            root.attributes('-topmost', 1)
            messagebox.showinfo("it`s added", "Added")
            root.attributes('-topmost', 0)

    except:pass



@eel.expose
def rem_game(file_id):
    try:
        os.remove(f"{get_st_path()}/config/stplug-in/{file_id}.st")
        textbox_cont.append(f'{nowt}removed game with ID <{file_id}> from your library')
        root.attributes('-topmost', 1)
        messagebox.showinfo("it`s removed", "Removed")
        root.attributes('-topmost', 0)
    except:pass



@eel.expose
def restart_st():
    subprocess.run(["taskkill", "/F", "/IM", "steam.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)   
    os.system(f'start "" "{get_st_path()}\steam.exe"')



@eel.expose
def get_name_by_id(file_id):
    with zipfile.ZipFile(zip_path, 'r') as archive:
        for file in archive.namelist():  
            parts = file.split('/')  
            if len(parts) > 1 and parts[-1] == file_id+".st": 
                return parts[0].replace("_","")  
            
            if len(parts) > 1 and parts[-1] == file_id+".lua": 
                return parts[0].replace("_","")  
            
    return "none"



def get_gb_info():
    if has_internet():
        response = requests.get("https://raw.githubusercontent.com/Wl13proger9/Steamer/main/config.txt")
        if response.status_code == 200:
            config_content = response.text  
            result = {}
            current_key = None
            for line in config_content.split("\n"):
                line = line.strip()  
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    result[key] = value
                    current_key = key  
                elif current_key: result[current_key] += '\n' + line
            return result
        else:return "none"
    else:return "none"
    #get_gb_info().get("mega", "none")



@eel.expose
def img_data(out):
   
    def vladeshkere():
        with open(img_data_path) as f:
            out = []
            dic = {}
            for item in f.readlines():
                out.append(item.split("->"))
                parts = item.split("->")
                if len(parts) == 2:
                    key = parts[0].strip()  
                    value = parts[1].strip()
                    dic[key] = value
            return dic
            #img_data().get('368360', "none")

    return vladeshkere().get(out, "none")
    

#print(img_data('10'))
#2169200

class lib:
    
    def get():
        blacklist = ["Steamtools.st"]
        for file in os.listdir("D:/steam/config/stplug-in"):
            if file.endswith(".st"):
                if file not in blacklist:
                    print(f"{file} - {get_name_by_id(file.replace('.st', ''))}")



@eel.expose
def profile(steam_path, typ):
    #а вы думаете что тут данные крадутся?)
    try:
        if typ == "avatar":
            return get_steam_avatar(get_user_id(steam_path))
            
        elif typ == "name":
            loginusers_path = os.path.join(steam_path, "config", "loginusers.vdf")
            if not os.path.exists(loginusers_path):return "none"
            with open(loginusers_path, 'r', encoding='utf-8') as file:data = file.read()
            accounts = re.findall(r'"(\d{17})"\s*\{(.*?)\}', data, re.DOTALL)
            current_steam_id = None
            persona_name = None
            for steam_id, content in accounts:  
                if re.search(r'"MostRecent"\s*"1"', content):
                    current_steam_id = steam_id
                    persona_match = re.search(r'"PersonaName"\s*"(.+?)"', content)
                    if persona_match:persona_name = persona_match.group(1)
                    break  
            return persona_name if persona_name else "none"


        elif typ == "acc_name":
            loginusers_path = os.path.join(steam_path, "config", "loginusers.vdf")
            if not os.path.exists(loginusers_path):return "none"
            with open(loginusers_path, 'r', encoding='utf-8') as file:data = file.read()
            accounts = re.findall(r'"(\d{17})"\s*\{(.*?)\}', data, re.DOTALL)
            current_steam_id = None
            persona_name = None
            for steam_id, content in accounts:  
                if re.search(r'"MostRecent"\s*"1"', content):
                    current_steam_id = steam_id
                    persona_match = re.search(r'"AccountName"\s*"(.+?)"', content)
                    if persona_match:persona_name = persona_match.group(1)
                    break  
            return persona_name if persona_name else "none"
        

        elif typ == "id":
            return get_user_id(steam_path)
        
        else:return "none"
    except Exception as e:
        print(e)



@eel.expose
def browser_open(url, do=None):
    if do is not None:
        if do == 'avatar':webbrowser.open(f"https://steamcommunity.com/profiles/{profile(get_st_path(),'id')}")
        elif do == 'product':webbrowser.open(f"https://store.steampowered.com/app/{url}")
        elif do == 'gb':webbrowser.open(get_gb_info().get(url, "none"))
        else:return 'none'
        #---some shit---
        #avatar - you steam profile
        #product - steam game page
        #gb - function where i take info from github
    else:webbrowser.open(url)



@eel.expose
def get_data_by_id(id,t='name'):
    try:

        url = f"https://store.steampowered.com/api/appdetails?appids={id}"
        response = requests.get(url)
        data = response.json()
        game_data = data[id]['data']
        alls = []

        if t == 'name':return game_data['name']
        elif t == 'date':return game_data['release_date']['date']
        elif t == 'dev':return''.join(game_data['developers'])
        elif t == 'pub':return''.join(game_data['publishers'])
        elif t == 'url':return url
        elif t == 'all': 
            alls.append(game_data['name'])
            alls.append(game_data['release_date']['date'])
            alls.append(''.join(game_data['developers']))
            alls.append(''.join(game_data['publishers']))
            return alls  
        else:return 'none'

    except TypeError:return 'none'
    except KeyError:return 'none'



