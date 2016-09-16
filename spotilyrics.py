import spotilib
from PyLyrics import *
from tkinter import *
import Pmw
import os
import get_lyrics as lyric
import platform
import configparser


# Returns the fontsize
def fontsize():
    config = configparser.ConfigParser()
    configini = os.getcwd() + '/config.ini'
    config.read(configini)
    fontsize = config.get('LYRIC', 'fontsize')
    return fontsize


def config():
    # Update the lyric_space widget with the new changes
    def update():
        # Creates the tag to centralize the lyrics
        lyric_space.tag_configure('config', justify='center',
                                  foreground='white',
                                  font='arial {}'.format(fontsize()))
        # centralizes the Lyric Text using a tag
        lyric_space.tag_add("config", 1.0, "end")

    # saves the new configs on config.ini
    def save():
        config = configparser.SafeConfigParser()
        if font_size.get().isdigit():
            font_size_num = font_size.get()
        else:
            font_size_num = '10'
        config.read('config.ini')
        config.set('LYRIC', 'FontSize', font_size_num)

        with open('config.ini', 'w+') as configfile:
            config.write(configfile)
            configfile.close()
        config_window.destroy()
        update()
    # Creates the config window
    config_window = Toplevel(master)
    Label(config_window, text='Font Size:').grid(sticky='e', row=0, column=0)
    font_size_var = StringVar()
    font_size_var.set(fontsize())
    font_size = Spinbox(
        config_window, from_=1, to=50, textvariable=font_size_var)
    font_size.grid(row=0, column=1)
    Button(config_window, text='Save', command=save).grid(column=1)


# Main function to get the lyrics
def get_lyrics(old_song=None, old_artist=None):
    # Gets artist name from spotilib and stores it in the artist var
    artist = spotilib.artist()
    # Gets song name from spotilib and stores it in the song var
    song = spotilib.song()
    # Checks if there is nothing playing
    if (artist == 'There is nothing playing at this moment') or (
            song == 'There is nothing playing at this moment'):
        # Then set the lyric to tell the user about it
        lyric_space.setvalue('There is nothing playing at this moment')
        # Creates the tag to centralize the lyrics
        lyric_space.tag_configure('config', justify='center',
                                  foreground='white',
                                  font='arial {}'.format(fontsize()))
        # centralizes the Lyric Text using a tag
        lyric_space.tag_add("config", 1.0, "end")
        # Changes the song title on the upper part of the window
        song_title.set('There is nothing playing')
        # Changes the artist title on the upper part of the window
        artist_title.set('at this moment')
        # Set the play/pause button to play option
        if platform.system() == 'Windows':
            play_button_text.set(u"\u25B6")
        else:
            play_button_text.set(u"\u25B6")
        # Set the old_song and old_artist variable to check for changes
        old_song = song
        old_artist = artist
    # checks if the old_song or old_artist variable are different
    # from the current one
    elif old_song != song or old_artist != artist:
        master.update()
        # Changes the song title on the upper part of the window
        song_title.set(song)
        # Changes the artist title on the upper part of the window
        artist_title.set(artist)
        # Set the play/pause button to pause option
        if platform.system() == 'Windows':
            play_button_text.set(u"\u23F8")
        else:
            play_button_text.set(u"\u25B6")
        # Placeholder while system searchs for lyric
        lyric_space.setvalue('Searching...')
        # Creates the tag to centralize the lyrics
        lyric_space.tag_configure('config', justify='center',
                                  foreground='white',
                                  font='arial {}'.format(fontsize()))
        lyric_space.tag_add("config", 1.0, "end")
        # updates the window
        master.update()
        # then try to get the lyric with that info
        # lyrics = PyLyrics.getLyrics(artist, song)
        lyrics = lyric.get(artist, song)
        if lyrics != 'Lyric not found':
            # Changes the lyric text to the current lyric
            lyric_space.setvalue(lyrics)
            # Creates the tag to centralize the lyrics
            lyric_space.tag_configure('config', justify='center',
                                      foreground='white',
                                      font='arial {}'.format(fontsize()))
            # centralizes the Lyric Text using a tag
            lyric_space.tag_add("config", 1.0, "end")
            # Set the old_song and old_artist variable to check for changes
        else:
            # warns the user on the lyric text about the failure
            lyric_space.setvalue('Lyric not found!')
            # Creates the tag to centralize the lyrics
            lyric_space.tag_configure('config', justify='center',
                                      foreground='white',
                                      font='arial {}'.format(fontsize()))
            # centralizes the Lyric Text using a tag
            lyric_space.tag_add("config", 1.0, "end")
            # Set the old_song and old_artist variable to check for changes
        old_song = song
        old_artist = artist
        # if it's the same song from the last time it ran
    else:
        # just resets the value of old_song and old_artist
        old_song = song
        old_artist = artist
    # Repeats this function every 1 second(1000ms)
    master.after(1000, get_lyrics, old_song, old_artist)


# creates the main window
master = Tk()
master.title('Spotilyrics')
master.configure(background='#282828')
# Icon support
if os.path.isfile(os.getcwd() + '/lyrics.png'):
    img = Image("photo", file=os.getcwd() + "/lyrics.png")
    master.tk.call('wm', 'iconphoto', master._w, img)
# -------------- SET POSITION OF THE WINDOW --------------
w = 430  # width for the Tk root
h = 577  # height for the Tk root

# get screen width and height
ws = master.winfo_screenwidth()  # width of the screen
hs = master.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
# and where it is placed
master.geometry('%dx%d+%d+%d' % (w, h, x, y))
# ---------------------------------------------------------

# creates the variables for the song title and artist title on the upper part
# and the play/pause button
song_title = StringVar()
artist_title = StringVar()
play_button_text = StringVar()
# Frame for the tiles
title = Frame(master)
title.configure(background='#282828')
# frame for the controls
controls = Frame(master)
controls.configure(background='#282828')

# Creates the Song Title text
Message(title, textvariable=song_title, font='arial 11 bold',
        background='#282828', foreground='white', width=440).grid()
# Creates the Artist Title text
Message(title, textvariable=artist_title, font='arial 11 bold',
        background='#282828', foreground='white', width=440).grid()
# Button for previous song
previous_button = Button(controls,
                         text=u'\u23EE',
                         relief='flat',
                         activebackground='#1DB954',
                         activeforeground='#282828',
                         bg='#282828',
                         fg='#1DB954',
                         borderwidth=0,
                         bd=0,
                         highlightthickness=0,
                         font='arial 11',
                         command=spotilib.previous
                         )
# Button for pausing/playing song
play_button = Button(controls,
                     textvariable=play_button_text,
                     relief='flat',
                     activebackground='#1DB954',
                     activeforeground='#282828',
                     bg='#282828',
                     fg='#1DB954',
                     font='arial 11',
                     borderwidth=0,
                     highlightthickness=0,
                     bd=0,
                     command=spotilib.pause
                     )
# Button for the next song
next_button = Button(controls,
                     text=u'\u23ED',
                     relief='flat',
                     activebackground='#1DB954',
                     activeforeground='#282828',
                     bg='#282828',
                     fg='#1DB954',
                     bd=0,
                     highlightthickness=0,
                     borderwidth=0,
                     font='arial 11',
                     command=spotilib.next
                     )
if platform.system() == 'Windows':
    config_button = Button(controls, text=u'\u2699',
                           relief='flat',
                           activebackground='#1DB954',
                           activeforeground='#282828',
                           bg='#282828',
                           fg='#1DB954',
                           bd=0,
                           highlightthickness=0,
                           borderwidth=0,
                           font='arial 11',
                           command=config)

# Places the music controls
previous_button.grid(sticky='n', row=0, column=0)
play_button.grid(sticky='n', row=0, column=1)
next_button.grid(sticky='n', row=0, column=2)
if platform.system() == 'Windows':
    config_button.grid(sticky='n', row=0, column=3)

# Creates the Text widget for the lyrics
lyric_space = Pmw.ScrolledText(master, borderframe=1, scrollmargin=0)
# Configures the Lyric Text as follows:
# Disable typing
# Changes the background for the window background
# Wraps the text on words, if it doesn't fit
lyric_space.configure(
    text_state='disabled', text_bg='#282828', text_wrap='word')

if platform.system() == 'Linux':
    # Adds the config button and menu(LINUX)
    menubar = Menu(master,
                   relief='flat',
                   background='#282828',
                   fg='#1DB954',
                   activebackground='#1DB954',
                   activeforeground='#282828',
                   font='Arial 12')
    menubar.add_command(label=u'\u2699', command=config)
    master.config(menu=menubar)


# Places all the gui items on the window
controls.pack()
title.pack()
lyric_space.pack(expand=True, fill='both')


# Starts the function to get the lyrics and its loop
get_lyrics()

# tkinter mainloop
master.mainloop()
