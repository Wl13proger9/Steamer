#pyinstaller main.py --onefile --add-data "commands.py;." --add-data "data.json;."


from commands import *

    
        
print(text2art("Steamer"))
print("Made by WL13Proger9") 


st_path = js.get("data.json","steam-path")



while True:
    try:
        world = input("[/help]> ")

        if world == "/help":
            print('''
--------help--------
Just enter game ID or URL to add game from DB..
/help - show this message
/about - show about
/rm <ID> - remove game with ID
/bye - exit
/restart - restart Steam
/setpath - set path to Steam
----------------------
            ''')


        elif world == "/bye":
            break


        elif world == "/about":
            print('''
--------about--------
-made by WL13Proger9
-build: 26/01/25cmd
----------------------
''')


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
            js.set("data.json","steam-path",input(f"{what}Enter path to Steam> "))     
            print(f"{yes}Done!")




        else:
            
            if input(f"{what}You want add game <{get_name_by_id(f'{search((world))}.st')}> with ID: <{search((world))}>?  [y/n]> ") == "y":
                copy_files_by_type_in_zip(search((world)), 
                                        f"{st_path}/config/stplug-in", 
                                        f"{st_path}/config/depotcache")
                print(f"{yes}Done!")

                if input(f"{what}Restart Steam?[y/n]> ")  == "y":restart_st()
                else:continue


    except Exception as e:print(e)




#268500

