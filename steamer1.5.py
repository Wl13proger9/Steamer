#pyinstaller steamer1.5.py --onefile --add-data "commands.py;." --add-data "data.json;."


from commands import *




if js.get("data.json","steam-path") == "":
    print(f"{no}Path to Steam not found! Please set path to Steam...") 
    select_folder()
    print(f"{yes}Done!") 
    st_path = js.get("data.json","steam-path")


if not os.path.exists("./DataBase/"):
    print(f"{no}DataBase not found! Please wait...")
    os.makedirs("./DataBase/")


if not os.path.exists("./data.json"):
    print(f"{no}data.json not found! Please wait...")
    with open("data.json", "w") as file:
        file.write('{"steam-path":""}')
        file.close()
    print(f"{yes}Done!")


if not os.path.exists("./DataBase/games.zip"):
    print(f"{no}games.zip not found!\n{no}You need to downlaod DataBase\n{hm}Here URL: \033[1mhttps://mega.nz/file/EchSlZLL#BbT7-qtm26ZnaTpzpj0AjgNemHh6av68MyAN7IuTfOE\033[0m")
    exit()






print(text2art("Steamer"))
print("Made by WL13Proger9") 
st_path = js.get("data.json","steam-path")


def main():

    while True:
        try:
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
    ----------------------
                ''')


            elif "/bye" in world:
                break


            elif "/about" in world:
                print('''
    --------about--------
    -made by WL13Proger9
    -build: 04/02/25cmd
    -version: 1.5
    ----------------------
    ''')


            elif "/clear" in world:
                os.system('cls' if os.name == 'nt' else 'clear')


            elif "/rm" in world:
                #res = search(rm(world))
                #393080
                if check_file_in_folder(f'{st_path}/config/stplug-in', f"{search(rm(world))}.st") == True:
                

                    if input(f"{what}You want remove: <{get_name_by_id(f'{search(rm(world))}.st')}> with ID: <{search(rm(world))}>?  [y/n]> ") == "y":

                        os.remove(f"{st_path}/config/stplug-in/{search(rm(world))}.st")

                        print(f"{yes}Done!")

                        if input(f"{what}Restart Steam?[y/n]> ")  == "y":restart_st()
                        else:continue
                    else:continue
                else:
                    print(f'{no}Game with ID {search(rm(world))} not found...')


            elif "/restart" in world:
                restart_st()


            elif "/setpath" in world:
                print(f"{hm}Your past path to Steam: ",st_path)
                select_folder() 
                print(f"{yes}Done!")

   
            elif "/mygames" in world:
                #os.walk(f"{st_path}/config/stplug-in")
                print("Your games:")
                for root, dirs, files in os.walk(f"{st_path}/config/stplug-in"):
                    for file in files:
                        if file.endswith(".st"):
                            print(f"{hm}ID: {file.split('.')[0]} - {get_name_by_id(file)}")

           
            else:
                
                if world.startswith("/"):print(f"{no}Command <{world}> not found...")
                
                else:
                    if is_game_in_db(search(world)) == True:
                        
                        if input(f"{what}You want add game <{get_name_by_id(f'{search((world))}.st')}> with ID: <{search((world))}>?  [y/n]> ") == "y":
                            copy_files_by_type_in_zip(search((world)), 
                                                f"{st_path}/config/stplug-in", 
                                                f"{st_path}/config/depotcache")
                            print(f"{yes}Done!")

                            if input(f"{what}Restart Steam?[y/n]> ")  == "y":restart_st()
                            else:continue

                    else:
                        print(f'{no}Game with ID {search(world)} not found...')


        except Exception as e:print(e)


if __name__ == "__main__":
    main()

#268500

