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
import threading
import os
import sys
import itertools
import winreg
import sys








zip_path = "./DataBase/games.zip" 
id_path = "./DataBase/allgames.txt"
geter = ""
no   = ('\033[31m' + '[!]'+'\033[39m') #no
yes  = ('\033[32m' + '[+]'+'\033[39m') #yes
what = ('\033[34m' + '[?]'+'\033[39m') #what
hm   = ('\033[35m' + '[-]'+'\033[39m') #hm
cont = []
root_dir = os.getcwd()




'''
class txt:
    @staticmethod
    def get(file_name, key):
        file_path = os.path.join(root_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split(" - ", 1)
                    if len(parts) == 2 and parts[0].strip() == key:
                        return parts[1].strip()
            return None
        except FileNotFoundError:
            return None

    @staticmethod
    def set(file_name, key, new_value):
        file_path = os.path.join(root_dir, file_name)
        lines = []
        key_found = False
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                for i, line in enumerate(lines):
                    parts = line.strip().split(" - ", 1)
                    if len(parts) == 2 and parts[0].strip() == key:
                        lines[i] = f"{key} - {new_value}\n"
                        key_found = True
                        break
            
            if not key_found:
                lines.append(f"{key} - {new_value}\n")
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)
        except FileNotFoundError:
            return None
'''

class txt:
    def get(id,spl="=",file="data.txt"):
        out = {} 
        with open(file,"r") as f:
            for line in f.readlines():
                parts = line.strip().split(spl)  
                #out[parts[0].replace(' ','')] = parts[1].replace(' ','')
                out[parts[0].strip()] = parts[1].strip() 
        og = out.get(str(id),None)
        if og in ['True','False','None']:return eval(og)
        else: return og


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



def restart_st():
    subprocess.run(["taskkill", "/F", "/IM", "steam.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)   
    #os.system(f"start {txt.get('data.txt','steam-path')}/steam.exe")
    
   
    os.system(f'start "" "{txt.get("steam-path")}\steam.exe"')



def copy_and_sort_files(zip_path, search_id, manifest_folder, st_folder):
    try:
        with zipfile.ZipFile(zip_path, 'r') as archive:
            file_list = archive.namelist()

            matching_files = [
                f for f in file_list 
                if f.endswith(f"{search_id}.st") or f.endswith(f"{search_id}.lua")]

            if matching_files:

                

                game_folders = set(os.path.dirname(f) for f in matching_files)
                

               


               
                for file in matching_files:
                    #print(f"- {file}")
                  
                    if file.endswith(".st"):target_folder = st_folder
                    else:continue

                    os.makedirs(target_folder, exist_ok=True)
                    extracted_path = archive.extract(file, "./temp_extracted")
                    shutil.copy(extracted_path, os.path.join(target_folder, os.path.basename(file)))

        
                for folder in game_folders:

                    input(folder)


                    manifest_files = [
                        f for f in file_list if f.startswith(folder) and f.endswith(".manifest")
                    ]
                    print(f"\n{yes}Found {len(manifest_files)} .manifest in {folder}:")
                    for manifest_file in manifest_files:
                        print(f"- {manifest_file}")
                        os.makedirs(manifest_folder, exist_ok=True)
                        extracted_path = archive.extract(manifest_file, "./temp_extracted")
                        shutil.copy(extracted_path, os.path.join(manifest_folder, os.path.basename(manifest_file)))

                # Удаляем временную папку
                shutil.rmtree("./temp_extracted", ignore_errors=True)

                print(f"\n{yes}Files have been successfully copied to the appropriate folders.")
            else:
                print(f"{no}Files with ID {search_id} not found...")
    
    except FileNotFoundError:
        print(f"{hm}File {zip_path} not found...")
    except zipfile.BadZipFile:
        print(f"{hm}File {zip_path} is corrupted or is not a ZIP archive.")
    except Exception as e:
        print(f"{hm}Error: {e}")



def rm(command):
    if command.startswith("/rm "):return command.split()[1]
    else:print(f"{no}Use: /rm <ID>")



def get_name_by_id(target_filename):
    with zipfile.ZipFile(zip_path, 'r') as archive:
        for file in archive.namelist():  
            parts = file.split('/')  
            if len(parts) > 1 and parts[-1] == target_filename: return parts[0].replace("_","")  
    return None  



def check_file_in_folder(folder_path, target_filename):
    file_path = os.path.join(folder_path, target_filename) 
    return os.path.isfile(file_path)



def copy_files_by_type_in_zip(file_id, target_st_folder, target_manifest_folder):
    with zipfile.ZipFile(zip_path, 'r') as archive:
        found_folder = None
        
        for file in archive.namelist():
            parts = file.split('/')
            if len(parts) > 1 and parts[-1] == f"{file_id}.st": 
                found_folder = parts[0] 
                break
        if not found_folder:  
            return None
        if not os.path.exists(target_st_folder):os.makedirs(target_st_folder)
        if not os.path.exists(target_manifest_folder):os.makedirs(target_manifest_folder)
        for file in archive.namelist():
            parts = file.split('/')
            if parts[0] == found_folder:  
                if file.endswith('.st'):
                    with archive.open(file) as f:
                        target_path = os.path.join(target_st_folder, file.split('/')[-1])
                        with open(target_path, 'wb') as out_file:shutil.copyfileobj(f, out_file)
                elif file.endswith('.manifest'):
                    with archive.open(file) as f:
                        target_path = os.path.join(target_manifest_folder, file.split('/')[-1])
                        with open(target_path, 'wb') as out_file:shutil.copyfileobj(f, out_file)



def is_game_in_db(id):
    with zipfile.ZipFile(zip_path, 'r') as archive:  
        for file in archive.namelist():
            parts = file.split('/')
            if len(parts) > 1 and parts[-1] == f"{search(id)}.st": 
                return True



def select_folder():
    root = tk.Tk()
    root.withdraw()  
    folder_selected = filedialog.askdirectory()  
    if folder_selected:
        print(f"You selected: {folder_selected}")
        txt.set("steam-path",folder_selected)



def get_steam_path():
    try:
        key_path = r"SOFTWARE\Wow6432Node\Valve\Steam"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
            steam_path, _ = winreg.QueryValueEx(key, "InstallPath")
            return steam_path
    except FileNotFoundError:
        return None



def patching(details):
    #./hellyeah/
    if not os.path.exists(txt.get("steam-path")+"/config/stUI"):
        os.makedirs(txt.get("steam-path")+"/config/stUI")

    if not os.path.exists(txt.get("steam-path")+"/config/depotcache"):
        os.makedirs(txt.get("steam-path")+"/config/depotcache")

    if not os.path.exists(txt.get("steam-path")+"/config/stplug-in"):
        os.makedirs(txt.get("steam-path")+"/config/stplug-in")


    to = {"hid.dll":txt.get("steam-path"),
          "Steamtools.lua":txt.get("steam-path")+"/config/stplug-in",
          "Steamtools.st":txt.get("steam-path")+"/config/stplug-in",
          "luapacka.exe":txt.get("steam-path")+"/config/stplug-in",
          "Steamtools.exe":txt.get("steam-path")+"/config/stUI"}

    for det in details:
        #print(det)
        if det in os.listdir("./hellyeah/"):
            #print(to[det].replace("/","\\"))
            shutil.copy(f"./hellyeah/{det}",to[det].replace("/","\\"))






