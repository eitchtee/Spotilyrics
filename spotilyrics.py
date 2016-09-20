import spotilib
from PyLyrics import *
from tkinter import *
import Pmw
import os
import get_lyrics as lyric
import platform
import configparser
from functools import partial


# returns the correct fontstyle
def fontstyle():
    config = configparser.ConfigParser()
    configini = os.getcwd() + '/config.ini'
    config.read(configini)
    bold = config.get('LYRIC', 'bold')
    italics = config.get('LYRIC', 'italics')
    if bold == '1' and italics == '1':
        return ('bold italic')
    elif bold == '1' and italics == '0':
        return ('bold')
    elif bold == '0' and italics == '1':
        return ('italic')
    elif bold == '0' and italics == '0':
        return ('normal')


# Returns the fontsize
def fontsize():
    config = configparser.ConfigParser()
    configini = os.getcwd() + '/config.ini'
    config.read(configini)
    fontsize = config.get('LYRIC', 'fontsize')
    return fontsize


def config():
    def reset_to_default():
        font_size_var.set(10)
        bold_check.deselect()
        italics_check.deselect()
        save(False)

    def set_on_start():
        # sets fontsize to current config file one
        font_size_var.set(fontsize())
        # sets fontstyle to current config file one
        config = configparser.ConfigParser()
        configini = os.getcwd() + '/config.ini'
        config.read(configini)
        bold = config.get('LYRIC', 'bold')
        italics = config.get('LYRIC', 'italics')
        if bold == '1':
            bold_check.select()
        else:
            bold_check.deselect()
        if italics == '1':
            italics_check.select()
        else:
            italics_check.deselect()

    # Update the lyric_space widget with the new changes
    def update():
        # Creates the tag to centralize the lyrics
        lyric_space.tag_configure('config', justify='center',
                                  foreground='white',
                                  font=('arial', fontsize(), fontstyle()))
        # centralizes the Lyric Text using a tag
        lyric_space.tag_add("config", 1.0, "end")

    # saves the new configs on config.ini
    def save(save_button=True):
        config = configparser.SafeConfigParser()
        config.read('config.ini')
        # font size save function
        if font_size.get().isdigit():
            font_size_num = font_size.get()
        else:
            font_size_num = '10'
        # bold and italics save function
        bold_info = bold_var.get()
        italics_info = italics_var.get()

        # set configs
        config.set('LYRIC', 'FontSize', font_size_num)
        config.set('LYRIC', 'bold', bold_info)
        config.set('LYRIC', 'italics', italics_info)

        # write configs
        with open('config.ini', 'w+') as configfile:
            config.write(configfile)
            configfile.close()
        if save_button is True:
            config_window.destroy()
            update()
        else:
            update()

    # Creates the config window
    config_window = Toplevel(master)

    # Font size configs
    Label(config_window, text='Font Size:').grid(sticky='w', row=0, column=0)
    font_size_var = StringVar()
    font_size = Spinbox(
        config_window, from_=1, to=50, textvariable=font_size_var, width=3)
    font_size.grid(row=0, column=1)

    # Font Style configs
    Label(config_window, text='Font Style:').grid(sticky='w', row=1, column=0)
    bold_var = StringVar()
    bold_check = Checkbutton(config_window, text="Bold",
                             font=('arial', '10', 'bold'),
                             variable=bold_var)
    bold_check.grid(row=1, column=1)

    italics_var = StringVar()
    italics_check = Checkbutton(config_window, text="Italics", font=(
        'arial', '10', 'italic'), variable=italics_var, state='normal')
    italics_check.grid(row=1, column=2)

    # sets the configs as it is on the config file
    set_on_start()
    # save configs button
    Button(config_window, text='Reset to default',
           command=reset_to_default).grid(row=3, column=1)
    Button(config_window, text='Save', command=save).grid(row=3, column=2)


def check_save_button():
    artist = spotilib.artist()
    song = spotilib.song().split(' - ', 1)[0]
    if os.path.isfile('{0}/lyrics/{1} - {2}.txt'.format(
            os.getcwd(), song, artist)):
        save_button.configure(image=saved_icon, state='normal')
        master.focus()

    else:
        save_button.configure(image=save_icon, state='normal')
        master.focus()


def save():
    global lyrics
    directory = '{0}/lyrics/'.format(os.getcwd())
    if not os.path.exists(directory):
        os.makedirs(directory)
    artist = spotilib.artist()
    song = spotilib.song().split(' - ', 1)[0]
    file = '{0}/lyrics/{1} - {2}.txt'.format(os.getcwd(), song, artist)
    if not os.path.isfile(file):
        # lyrics = lyric.get(artist, song)
        with open(file, 'w') as lyricfile:
            lyricfile.write(lyrics)
            lyricfile.close()
        print('File "{0}" saved \n'.format(file))
        check_save_button()

    else:
        os.remove(file)
        print('File "{0}" removed \n'.format(file))
        check_save_button()


# Main function to get the lyrics
def get_lyrics(refresh=False, old_song=None, old_artist=None):
    global lyrics
    # Gets artist name from spotilib and stores it in the artist var
    artist = spotilib.artist()
    # Gets song name from spotilib and stores it in the song var
    song = spotilib.song()
    # Checks if there is nothing playing
    if (artist == 'There is nothing playing at this moment') or (
            song == 'There is nothing playing at this moment'):
        save_button.configure(image=no_save_icon, state='disabled')
        # Then set the lyric to tell the user about it
        lyric_space.setvalue('There is nothing playing at this moment')
        # Creates the tag to centralize the lyrics
        lyric_space.tag_configure('config', justify='center',
                                  foreground='white',
                                  font=('arial', fontsize(), fontstyle()))
        # centralizes the Lyric Text using a tag
        lyric_space.tag_add("config", 1.0, "end")
        # Changes the song title on the upper part of the window
        song_title.set('There is nothing playing')
        # Changes the artist title on the upper part of the window
        artist_title.set('at this moment')
        # Set the play/pause button to play option
        if platform.system() == 'Windows':
            play_button.configure(image=play_icon)
        # Set the old_song and old_artist variable to check for changes
        old_song = song
        old_artist = artist
    # checks if the old_song or old_artist variable are different
    # from the current one
    elif old_song != song or old_artist != artist:
        check_save_button()
        master.update()
        # Changes the song title on the upper part of the window
        song_title.set(song)
        # Changes the artist title on the upper part of the window
        artist_title.set(artist)
        # Set the play/pause button to pause option
        if platform.system() == 'Windows':
            play_button.configure(image=pause_icon)
        # Placeholder while system searchs for lyric
        lyric_space.setvalue('Searching...')
        # Creates the tag to centralize the lyrics
        lyric_space.tag_configure('config', justify='center',
                                  foreground='white',
                                  font=('arial', fontsize(), fontstyle()))
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
                                      font=('arial', fontsize(), fontstyle()))
            # centralizes the Lyric Text using a tag
            lyric_space.tag_add("config", 1.0, "end")
            # Set the old_song and old_artist variable to check for changes
        else:
            # warns the user on the lyric text about the failure
            lyric_space.setvalue('Lyric not found!')
            # Creates the tag to centralize the lyrics
            lyric_space.tag_configure('config', justify='center',
                                      foreground='white',
                                      font=('arial', fontsize(), fontstyle()))
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
    if refresh is False:
        # Repeats this function every 1 second(1000ms)
        master.after(1000, get_lyrics, False, old_song, old_artist)


# creates the main window
lyrics = None
master = Tk()
master.title('Spotilyrics')
master.configure(background='#282828')
# Icon support
if os.path.isfile(os.getcwd() + '/gfx/lyrics.png'):
    img = Image("photo", file=os.getcwd() + "/gfx/lyrics.png")
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
previous_icon = PhotoImage(file="gfx/previous.png")
previous_button = Button(controls,
                         image=previous_icon,
                         relief='raised',
                         activebackground='#282828',
                         bg='#282828',
                         borderwidth=0,
                         bd=0,
                         highlightthickness=0,
                         command=spotilib.previous
                         )

# Button for pausing/playing song
play_icon = PhotoImage(file="gfx/play.png")
pause_icon = PhotoImage(file="gfx/pause.png")
play_button = Button(controls,
                     image=play_icon,
                     relief='raised',
                     activebackground='#282828',
                     bg='#282828',
                     borderwidth=0,
                     highlightthickness=0,
                     bd=0,
                     command=spotilib.pause
                     )

# Button for the next song
next_icon = PhotoImage(file="gfx/skip.png")
next_button = Button(controls,
                     image=next_icon,
                     relief='raise',
                     activebackground='#282828',
                     bg='#282828',
                     bd=0,
                     highlightthickness=0,
                     borderwidth=0,
                     command=spotilib.next
                     )

# Button for the settings
config_icon = PhotoImage(file="gfx/settings.png")
config_button = Button(controls,
                       image=config_icon,
                       relief='raised',
                       activebackground='#282828',
                       bg='#282828',
                       bd=0,
                       highlightthickness=0,
                       borderwidth=0,
                       command=config)

# Button for saving lyrics
save_icon = PhotoImage(file="gfx/save.png")
saved_icon = PhotoImage(file="gfx/saved.png")
no_save_icon = PhotoImage(file="gfx/no_save.png")
save_button = Button(controls,
                     image=save_icon,
                     relief='raised',
                     activebackground='#282828',
                     bg='#282828',
                     bd=0,
                     highlightthickness=0,
                     borderwidth=0,
                     command=save)

# Places the music controls
save_button.grid(sticky='n', row=0, column=0)
previous_button.grid(sticky='n', row=0, column=1)
play_button.grid(sticky='n', row=0, column=2)
next_button.grid(sticky='n', row=0, column=3)
config_button.grid(sticky='n', row=0, column=4)

# Creates the Text widget for the lyrics
lyric_space = Pmw.ScrolledText(master, borderframe=1, scrollmargin=0)
# Configures the Lyric Text as follows:
# Disable typing
# Changes the background for the window background
# Wraps the text on words, if it doesn't fit
lyric_space.configure(
    text_state='disabled', text_bg='#282828', text_wrap='word')


# Places all the gui items on the window
title.pack()
controls.pack()
lyric_space.pack(expand=True, fill='both')

# Allows for refreshing the lyrics with F5
master.bind('<F5>', partial(get_lyrics, True))

# Starts the function to get the lyrics and its loop
get_lyrics()

# tkinter mainloop
master.mainloop()
