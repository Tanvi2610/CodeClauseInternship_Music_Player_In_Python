import time
from tkinter import *
from tkinter import filedialog
from pygame import mixer
import os
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
mixer.init()
root = Tk()

frame =Frame(root, width=700, height=400)
frame.pack()

image = Image.open("44zG.gif")
frameCnt = image.n_frames
frames = []

for i in range(frameCnt):
    image.seek(i)
    photo = ImageTk.PhotoImage(image.copy().resize((700,400)))
    frames.append(photo)

label = Label(frame)
label.pack(fill="both", expand=True) 

label.config(image=frames[0])

def update(ind):
    frame = frames[ind]
    label.config(image=frame)
    ind += 1
    if ind == frameCnt:
        ind = 0
    root.after(100, update, ind)
    
update(0)

paused_time = 0 
is_paused = False 
start_time = 0  

def AddMusic():
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs = os.listdir(path)
        for song in songs:
            if song.endswith(".mp3"):
                PlayList.insert(END, song)

def PlayMusic():
    global is_paused, paused_time, start_time
    Music_Name = PlayList.get(ACTIVE)
    if Music_Name:
        if is_paused:
            mixer.music.unpause()
            start_time = time.time() - paused_time
            is_paused = False
        else:
            print(f"Playing: {Music_Name}")
            mixer.music.load(Music_Name)
            mixer.music.play()
            paused_time = 0
            start_time = time.time()
        UpdateMusicTime()
        PlayButton.config(image=PauseImage, command=PauseMusic)
    else:
        print("No song selected or song name is empty")

def PauseMusic():
    global is_paused, paused_time
    if mixer.music.get_busy():
        mixer.music.pause()
        is_paused = True
        paused_time = time.time() - start_time
        PlayButton.config(image=PlayImage, command=PlayMusic)

def StopMusic():
    global is_paused, paused_time
    mixer.music.stop()
    is_paused = False
    paused_time = 0
    timeline_label.config(text="00:00 / 00:00")
    PlayButton.config(image=PlayImage, command=PlayMusic)

def PreviousMusic():
    try:
        current_selection = PlayList.curselection()
        if current_selection[0] > 0:
            previous_index = current_selection[0] - 1
            PlayList.selection_clear(0, END)
            PlayList.activate(previous_index)
            PlayList.selection_set(previous_index)
            PlayMusic()
    except IndexError:
        print("No previous song in the playlist")

def NextMusic():
    try:
        current_selection = PlayList.curselection()
        if current_selection[0] < PlayList.size() - 1:
            next_index = current_selection[0] + 1
            PlayList.selection_clear(0, END)
            PlayList.activate(next_index)
            PlayList.selection_set(next_index)
            PlayMusic()
    except IndexError:
        print("No next song in the playlist")

def UpdateMusicTime():
    global paused_time, is_paused
    if mixer.music.get_busy() and not is_paused:
        current_time = time.time() - start_time 
        formatted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
        Music_Name = PlayList.get(ACTIVE)
        song_mut = MP3(Music_Name)
        song_length = song_mut.info.length
        formatted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
        timeline_label.config(text=f"{formatted_current_time} / {formatted_song_length}")
        root.after(1000, UpdateMusicTime)
    elif is_paused:
        formatted_paused_time = time.strftime('%M:%S', time.gmtime(paused_time))
        Music_Name = PlayList.get(ACTIVE)
        song_mut = MP3(Music_Name)
        song_length = song_mut.info.length
        formatted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
        timeline_label.config(text=f"{formatted_paused_time} / {formatted_song_length}")
    else:
        timeline_label.config(text="00:00 / 00:00")

root.title("Music Player")
root.geometry("500x700+290+10")
root.configure(background="grey")

lower_frame = Frame(root, bg="#333333", width=500, height=180)
lower_frame.place(x=0, y=400)

image_icon = PhotoImage(file="playlist.png")
root.iconphoto(False, image_icon)

Frame_Music = Frame(root, bd=2, relief=RIDGE)
Frame_Music.place(x=0, y=585, width=485, height=100)

PlayImage = ImageTk.PhotoImage(Image.open("play-button.png").resize((60,60)))
PauseImage = ImageTk.PhotoImage(Image.open("pause.png").resize((50, 50)))
PlayButton = Button(root, image=PlayImage, bg="grey", bd=0, height=60, width=60, command=PlayMusic)
PlayButton.place(x=220, y=480)

ButtonStop = ImageTk.PhotoImage(Image.open("stop-button.png").resize((50, 50)))
Button(root, image=ButtonStop, bg="grey", bd=0, height=50, width=50, command=StopMusic).place(x=35, y=487)

ButtonPrevious = ImageTk.PhotoImage(Image.open("previous.png").resize((50, 50)))
Button(root, image=ButtonPrevious, bg="grey", bd=0, height=50, width=50, command=PreviousMusic).place(x=130, y=487)

ButtonNext = ImageTk.PhotoImage(Image.open("next-button.png").resize((50, 50)))
Button(root, image=ButtonNext, bg="grey", bd=0, height=50, width=50, command=NextMusic).place(x=320, y=487)

ButtonVol = ImageTk.PhotoImage(Image.open("volume1.png").resize((50, 50)))
Button(root, image=ButtonVol, bg="grey", bd=0, height=50, width=50).place(x=415, y=487)

Button(root, text="Search Music", width=42, height=1, font=("Times New Roman", 16, "bold"), fg="Black", bg="grey", cursor="hand2", command=AddMusic).place(x=0, y=550)

Scroll = Scrollbar(Frame_Music)
PlayList = Listbox(Frame_Music, width=100, font=("Calibri", 15), bg="grey", fg="white", selectbackground="black", cursor="hand2", bd=0, yscrollcommand=Scroll.set)
Scroll.config(command=PlayList.yview)
Scroll.pack(side=RIGHT, fill=Y)
PlayList.pack(side=RIGHT, fill=BOTH)

timeline_label = Label(lower_frame, text="00:00 / 00:00", font=("Times New Roman", ), bg="grey", fg="black")
timeline_label.place(x=195, y=25)

root.mainloop()
