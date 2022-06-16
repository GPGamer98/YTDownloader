from time import sleep
from pytube import YouTube
from colorama import init, Fore
from moviepy.editor import *
import os
import shutil
import requests
import webbrowser

dir_path=os.path.dirname(os.path.realpath(__file__))
version = "1.2"
 
def on_complete(stream, filepath):
    print('Download Completato')
    sleep(0.5)
    print("Ultime verifiche in corso...")
    sleep(0.6)
    if download_choice=="a":
        print("Conversione da mp4 a mp3...")

        mp4=filepath.replace("\\","/")
        mp3=mp4.replace(".mp4", ".mp3")

        with VideoFileClip(mp4) as clip:
            audio=clip.audio
            audio.write_audiofile(mp3)

        shutil.move(mp4.replace(".mp4", ".mp3"), mp3.replace("mp4_to_mp3_cache", "audio"))

        filepathAudio=filepath.replace(".mp4", ".mp3").replace("mp4_to_mp3_cache", "audio")

        print("Tutto completato!")

        sleep(0.2)
        print("Il file si trova in",filepathAudio)
        input("Premi INVIO per uscire... ")
    else:
        print("Tutto completato!")

        sleep(0.2)
        print("Il file si trova in",filepath)
        input("Premi INVIO per uscire... ")
 
def on_progress(stream, chunk, bytes_remaining):
    progress_string = f'{round(100 - (bytes_remaining / stream.filesize * 100),2)}%'
    print("Progresso:",progress_string)

def check_updates():
    try:
        response = requests.get('https://pastebin.com/raw/dkUr58S3')
        data = response.text

        if float(data) > float(version):
            print('Aggiornamento disponibile!')

            updateRequest = input(f'''YTDownloader {version} può essere aggiornato alla versione {data}.
            Si o no? (s/n)  ''')

            if updateRequest == "s":
                webbrowser.open_new_tab('''https://github.com/GPGamer98/YTDownloader/releases/download/v1.2/YTDownloader1.2_setup.exe''')
            else:
                pass
    except Exception as e:
        print('Impossibile cercare gli aggiornamenti, Errore: ' + str(e))
 
init()
check_updates()
link = input('Link di YouTube: ')
video_object = YouTube(link, on_complete_callback = on_complete, on_progress_callback = on_progress)

print(Fore.RED + f'Titolo:  \033[39m {video_object.title}')
print(Fore.RED + f'Durata in minuti: \033[39m {round(video_object.length / 60,2)}')
print(Fore.RED + f'Visualizzazioni:  \033[39m {video_object.views}')
print(Fore.RED + f'Autore: \033[39m {video_object.author}')

print(
    Fore.RED + 'Scarica: ' + 
    Fore.GREEN + '(m)igliore \033[39m|' + 
    Fore.YELLOW + '(p)eggiore \033[39m|' + 
    Fore.BLUE + '(a)udio \033[39m| (u)scire')
download_choice = input('Scelta: ')
 
match download_choice:
    case 'm':
        video_object.streams.get_highest_resolution().download(dir_path+r"\downloaded\highquality")
    case 'p':
        video_object.streams.get_lowest_resolution().download(dir_path+r"\downloaded\lowquality")
    case 'a':
        video_object.streams.get_highest_resolution().download(dir_path+r"\downloaded\mp4_to_mp3_cache")

