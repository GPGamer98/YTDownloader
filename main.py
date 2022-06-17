from time import sleep
from pytube import YouTube
from colorama import init, Fore
from moviepy.editor import *
import os
import shutil
import requests
import webbrowser

dir_path=os.path.dirname(os.path.realpath(__file__))
version = 1.3
 
def on_complete(stream, filepath):
    print('Download completed')
    sleep(0.5)
    print("Last checks in progress...")
    sleep(0.6)
    if download_choice=="a":
        print("Conversion...")

        mp4=filepath.replace("\\","/")
        mp3=mp4.replace(".mp4", ".mp3")

        with VideoFileClip(mp4) as clip:
            audio=clip.audio
            audio.write_audiofile(mp3)

        shutil.move(mp4.replace(".mp4", ".mp3"), mp3.replace("mp4_to_mp3_cache", "audio"))

        filepathAudio=filepath.replace(".mp4", ".mp3").replace("mp4_to_mp3_cache", "audio")

        print("All completed!")

        sleep(0.2)
        print("The file is in",filepathAudio)
        input("Press any key to exit... ")
    else:
        print("All completed!")

        sleep(0.2)
        print("The file is in",filepath)
        input("Press any key to exit... ")
 
def on_progress(stream, chunk, bytes_remaining):
    progress_string = f'{round(100 - (bytes_remaining / stream.filesize * 100),2)}%'
    print("Progress:",progress_string)

def check_updates():
    try:
        response = requests.get('https://pastebin.com/raw/dkUr58S3')
        data = response.text

        if float(data) > float(version):
            print('Update available!')

            updateRequest = input(f'''YTDownloader {version} Can be updated to {data}.
            Yes or no? (y/n)  ''')

            if updateRequest == "y":
                webbrowser.open_new_tab(f'https://github.com/GPGamer98/YTDownloader/releases/download/v{data}/YTDownloader{data}_setup.exe')
            else:
                pass
    except Exception as e:
        print("Can't check for updates, ask on GitHub. Error: " + str(e))
 
init()
check_updates()
link = input('YouTube link: ')
video_object = YouTube(link, on_complete_callback = on_complete, on_progress_callback = on_progress)

print(Fore.RED + f'Title:  \033[39m {video_object.title}')
print(Fore.RED + f'Duration in minutes: \033[39m {round(video_object.length / 60,2)}')
print(Fore.RED + f'Views:  \033[39m {video_object.views}')
print(Fore.RED + f'Author: \033[39m {video_object.author}')

print(
    Fore.RED + 'Download: ' + 
    Fore.GREEN + '(b)etter \033[39m|' + 
    Fore.YELLOW + '(w)orse \033[39m|' + 
    Fore.BLUE + '(a)udio \033[39m| (e)xit')
download_choice = input('Choice: ')
 
match download_choice:
    case 'b':
        video_object.streams.get_highest_resolution().download(dir_path+r"\YTDownloader\downloaded\highquality")
    case 'w':
        video_object.streams.get_lowest_resolution().download(dir_path+r"\YTDownloader\downloaded\lowquality")
    case 'a':
        video_object.streams.get_highest_resolution().download(dir_path+r"\YTDownloader\downloaded\mp4_to_mp3_cache")
