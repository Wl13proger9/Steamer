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
import requests
import zipfile
import tarfile
import os











root = tk.Tk()
root.withdraw()  


zip_path = "DataBase/games.zip"
img_data_path = "DataBase/game-data.txt"
now = datetime.now()
textbox_cont = []



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
    


@eel.expose
def have_db():
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
def msg(text,name="Steamer message"): 
    root.attributes('-topmost', 1)
    messagebox.showinfo(name,text)
    root.attributes('-topmost', 0)




@eel.expose
def add_game(file_id): 
    nowt = now.strftime("[%H:%M]")
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

            
    except:pass



@eel.expose
def rem_game(file_id):
    nowt = now.strftime("[%H:%M]")
    try:
        os.remove(f"{get_st_path()}/config/stplug-in/{file_id}.st")
        textbox_cont.append(f'{nowt}removed game with ID <{file_id}> from your library')
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
            if len(parts) > 1 and parts[-1] == str(file_id)+".st": 
                return parts[0].replace("_","")  
            
            if len(parts) > 1 and parts[-1] == str(file_id)+".lua": 
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
    try:
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
    except TypeError:
       return "none"
    


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
        #avatar - your steam profile
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



@eel.expose
def search(text):
    if "https://steamdb.info/app/" in text:
        match = re.search(r'/app/(\d+)/', text)
        if match:return match.group(1)
        else:return text  

    elif "https://store.steampowered.com/app/" in text:
        match = re.search(r'/app/(\d+)/', text)
        if match:return match.group(1)
        else:return text  
    elif "https://store.steampowered.com/agecheck/app/" in text:
        match = re.search(r'/app/(\d+)/', text)
        if match:return match.group(1)
        else:return text  
    else:return text  




class data: 
    @eel.expose
    def get(id, spl="=", file="data.txt"):
        try:
            out = {} 
            with open(file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or spl not in line:continue  
                    parts = line.split(spl, 1) 
                    key = parts[0].strip()
                    value = parts[1].strip() if len(parts) > 1 else None
                    out[key] = value  
            og = out.get(str(id), None)
            if og in ['True', 'False', 'None']:return eval(og)
            return og
        except Exception as e:return None  

    @eel.expose
    def set(key, value, spl="=", file="data.txt"):
        key = str(key).strip()
        value = str(value).strip()
        found = False
        lines = []
        try:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    if spl in line and not line.strip().startswith("#"):
                        before, after = line.split(spl, 1)
                        k = before.strip()
                        if k == key:
                            spaces_before = len(before) - len(before.rstrip())
                            spaces_after = len(after) - len(after.lstrip())
                            new_line = f"{k}{' ' * spaces_before}{spl}{' ' * spaces_after}{value}\n"
                            lines.append(new_line)
                            found = True
                        else:lines.append(line)
                    else:lines.append(line)
        except FileNotFoundError:pass
        if not found:lines.append(f"{key} {spl} {value}\n")
        with open(file, "w", encoding="utf-8") as f:f.writelines(lines)

    @eel.expose
    def check_data():
        if not os.path.exists(f"DataBase/{zip_path}"):
            print("no db")
            
    @eel.expose   
    def return_data():
        need = {"st_path": get_st_path(),
                "win_width": "1200",
                "win_height": "700",
                "win_start": "main",   
                "show_b_r": "True",
                "show_b_prof": "True",
                "show_b_ver": "True",
                "db": "DataBase/games.zip",
                }
        for key in need:
            if data.get(str(key)) == "":
                data.set(str(key),need[key]) 

            if data.get(str(key)) == None:
                data.set(str(key),need[key]) 
               
       
 
@eel.expose
def settings(id):
    if id == "auto_set":
        data.set("st_path", get_st_path())
        


def restore_hy(urls,local_filename="hellyeah.zip"):
    def download_file(url, filename):
        response = requests.get(url, stream=True)
        response.raise_for_status()  # выбрасывает ошибку, если код ответа не 200
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def extract_archive_flat(filepath, extract_to='.'):
        os.makedirs(extract_to, exist_ok=True)

        if filepath.endswith('.zip'):
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                members = zip_ref.namelist()
                top_folder = os.path.commonprefix(members).rstrip('/')

                for member in members:
                    rel_path = member[len(top_folder)+1:] if member.startswith(top_folder + '/') else member
                    if not rel_path or member.endswith('/'):
                        continue
                    target_path = os.path.join(extract_to, rel_path)
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                        target.write(source.read())

        elif filepath.endswith(('.tar.gz', '.tgz', '.tar')):
            with tarfile.open(filepath, 'r:*') as tar_ref:
                members = tar_ref.getmembers()
                top_folder = os.path.commonprefix([m.name for m in members]).rstrip('/')

                for member in members:
                    rel_path = member.name[len(top_folder)+1:] if member.name.startswith(top_folder + '/') else member.name
                    if not rel_path:
                        continue
                    member.name = rel_path
                    tar_ref.extract(member, extract_to)
        else:
            raise ValueError("Unsupported archive format")


    download_file(urls, local_filename)
    extract_archive_flat(local_filename, extract_to="hellyeah")




def patch_st(details):
    #./hellyeah/
    if not os.path.exists(data.get("st_path")+"/config/stUI"):
        os.makedirs(data.get("st_path")+"/config/stUI")

    if not os.path.exists(data.get("st_path")+"/config/depotcache"):
        os.makedirs(data.get("st_path")+"/config/depotcache")

    if not os.path.exists(data.get("st_path")+"/config/stplug-in"):
        os.makedirs(data.get("st_path")+"/config/stplug-in")


    to = {"hid.dll":data.get("st_path"),
          "Steamtools.lua":data.get("st_path")+"/config/stplug-in",
          "Steamtools.st":data.get("st_path")+"/config/stplug-in",
          "luapacka.exe":data.get("st_path")+"/config/stplug-in",
          "Steamtools.exe":data.get("st_path")+"/config/stUI"}

    for det in details:
        #print(det)
        if det in os.listdir("./hellyeah/"):
            #print(to[det].replace("/","\\"))
            shutil.copy(f"./hellyeah/{det}",to[det].replace("/","\\"))
