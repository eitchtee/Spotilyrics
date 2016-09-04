import spotilib
from PyLyrics import *
from tkinter import *
import Pmw


# Main function to get the lyrics(for now)
# TO-DO: Add another website for searching for lyrics
# in case the first one fails
def get_lyrics(old_song=None, old_artist=None):
    # Gets artist name from spotilib and stores it in the artist var
    artist = spotilib.artist()
    # Gets song name from spotilib and stores it in the song var
    song = spotilib.song()
    try:
        # Checks if there is nothing playing
        if (artist == 'There is noting playing at this moment') or (
                song == 'There is noting playing at this moment'):
            # Then set the lyric to tell the user about it
            lyric_space.setvalue('Nada tocando no momento!')
            # centralizes the Lyric Text using a tag
            lyric_space.tag_add("center", 1.0, "end")
            # Changes the song title on the upper part of the window
            song_title.set('Nada tocando')
            # Changes the artist title on the upper part of the window
            artist_title.set('no momento')
            # Set program title
            master.title('Nada tocando no momento')
            # Set the play/pause button to play option
            play_button.set('▶')
            # Set the old_song and old_artist variable to check for changes
            old_song = song
            old_artist = artist
        # checks if the old_song or old_artist variable are different
        # from the current one
        elif old_song != song or old_artist != artist:
            # then try to get the lyric with that info
            lyrics = PyLyrics.getLyrics(artist, song)
            # Changes the lyric text to the current lyric
            lyric_space.setvalue(lyrics)
            # centralizes the Lyric Text using a tag
            lyric_space.tag_add("center", 1.0, "end")
            # Changes the song title on the upper part of the window
            song_title.set(song)
            # Changes the artist title on the upper part of the window
            artist_title.set(artist)
            # Set program title
            master.title('{0} - {1}'.format(song, artist))
            # Set the play/pause button to play option
            play_button.set('⏸')
            # Set the old_song and old_artist variable to check for changes
            old_song = song
            old_artist = artist
        # if it's the same song from the last time it ran
        else:
            # just resets the value of old_song and old_artist
            old_song = song
            old_artist = artist
    # if the PyLyrics module fails to get the lyric
    except ValueError:
        # warns the user on the lyric text about the failure
        lyric_space.setvalue('Música não encontrada!')
        # centralizes the Lyric Text using a tag
        lyric_space.tag_add("center", 1.0, "end")
        # Changes the song title on the upper part of the window
        song_title.set(song)
        # Changes the artist title on the upper part of the window
        artist_title.set(artist)
        # Set program title
        master.title('{0} - {1}'.format(song, artist))
        # Set the play/pause button to play option
        play_button.set('⏸')
        # Set the old_song and old_artist variable to check for changes
        old_song = song
        old_artist = artist
        # Skip the error
        pass
    # Repeats this function every 1 second(1000ms)
    master.after(1000, get_lyrics, old_song, old_artist)

# creates the main window
master = Tk()
# -------------- SET POSITION OF THE WINDOW --------------
w = 430  # width for the Tk root
h = 577  # height for the Tk root

# get screen width and height
ws = master.winfo_screenwidth()  # width of the screen
hs = master.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
master.geometry('%dx%d+%d+%d' % (w, h, x, y))
# ---------------------------------------------------------

# creates the variables for the song title and artist title on the upper part
# and the play/pause button
song_title = StringVar()
artist_title = StringVar()
play_button = StringVar()
# Frame for the tiles
title = Frame(master)
# frame for the controls
controls = Frame(master)

# Creates the Song Title text
Message(title, textvariable=song_title,
        font='arial 11 bold', width=440).grid()
# Creates the Artist Title text
Message(title, textvariable=artist_title,
        font='arial 11 bold', width=440).grid()
# Button for previous song
Button(controls, text='⏮', command=spotilib.previous).grid(
    sticky='n', row=0, column=0)
# Button for pausing/playing song
Button(controls, textvariable=play_button, command=spotilib.pause).grid(
    sticky='n', row=0, column=1)
# Button for the next song
Button(controls, text='⏭', command=spotilib.next).grid(
    sticky='n', row=0, column=2)
# Creates the Text widget for the lyrics
lyric_space = Pmw.ScrolledText(
    master)  # usehullsize=1, hull_width=430, hull_height=500)
# Configures the Lyric Text as follows:
# Disable typing
# Changes the background for the window background
# Wraps the text on words, if it doesn't fit
lyric_space.configure(text_state='disabled', text_bg=master.cget(
    'bg'), text_wrap='word')
# Creates the tag to centralize the lyrics
lyric_space.tag_configure('center', justify='center')

# Places all the gui items on the window
title.pack()
controls.pack()
lyric_space.pack(expand=True, fill='both')

# Starts the function to get the lyrics and its loop
get_lyrics()

# tkinter mainloop
master.mainloop()
