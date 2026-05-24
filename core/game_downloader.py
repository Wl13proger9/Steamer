import os
import requests






def download_game(file_id:str, download_dir:str = "downloads") -> None:
    url = f"https://files.catbox.moe/{file_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    

    DOWNLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), download_dir)
    if not os.path.exists(DOWNLOADS_DIR):os.makedirs(DOWNLOADS_DIR, exist_ok=True)

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        with open( os.path.join(DOWNLOADS_DIR, file_id), 'wb') as f:
            f.write(response.content)
        



download_game("tmozsh.zip")


