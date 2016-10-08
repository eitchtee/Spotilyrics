import os
import platform
if platform.system() == 'Windows':
    import win32gui
    import win32api
elif platform.system() == 'Linux':
    import dbus

###Virtual-KeyCodes###
Media_Next = 0xB0
Media_Previous = 0xB1
Media_Pause = 0xB3  # Play/Pause
Media_Mute = 0xAD


###SpotifyInfo###
def linux_status():
    try:
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                             "/org/mpris/MediaPlayer2")
        spotify_properties = dbus.Interface(spotify_bus,
                                            "org.freedesktop.DBus.Properties")
        status = spotify_properties.Get("org.mpris.MediaPlayer2.Player",
                                        "PlaybackStatus")
        return status
    except:
        return "Paused"


def song_info_linux():
    if linux_status() == "Playing":
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                             "/org/mpris/MediaPlayer2")
        spotify_properties = dbus.Interface(spotify_bus,
                                            "org.freedesktop.DBus.Properties")
        metadata = spotify_properties.Get(
            "org.mpris.MediaPlayer2.Player", "Metadata")
        song_info = metadata['xesam:title']
        return song_info
    else:
        return "There is nothing playing at this moment"


def artist_info_linux():
    if linux_status() == "Playing":
        session_bus = dbus.SessionBus()
        spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                             "/org/mpris/MediaPlayer2")
        spotify_properties = dbus.Interface(spotify_bus,
                                            "org.freedesktop.DBus.Properties")
        metadata = spotify_properties.Get(
            "org.mpris.MediaPlayer2.Player", "Metadata")
        artist_info = metadata['xesam:artist'][0]
        return artist_info
    else:
        return "There is nothing playing at this moment"


def getwindow(Title="SpotifyMainWindow"):
    window_id = win32gui.FindWindow(Title, None)
    return window_id


def song_info():
    try:
        song_info = win32gui.GetWindowText(getwindow())
    except:
        pass
    return song_info


def artist():
    if platform.system() == 'Windows':
        try:
            temp = song_info()
            artist, song = temp.split("-", 1)
            artist = artist.strip()
            return artist
        except:
            return "There is nothing playing at this moment"
    elif platform.system() == 'Linux':
        try:
            return artist_info_linux()
        except:
            return "There is nothing playing at this moment"


def song():
    if platform.system() == 'Windows':
        try:
            temp = song_info()
            artist, song = temp.split("-", 1)
            song = song.strip()
            return song
        except:
            return "There is nothing playing at this moment"
    elif platform.system() == 'Linux':
        try:
            return song_info_linux()
        except:
            return "There is nothing playing at this moment"

###SpotifyBlock###


def createfolder(folder_path="C:\SpotiBlock"):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        pass


def createfile(file_path="C:\SpotiBlock\Block.txt"):
    if not os.path.exists(file_path):
        file = open(file_path, "a")
        file.write("ThisFirstLineWillBeIgnoredButIsNecessaryForUse")


def blocklist(file_path="C:\SpotiBlock\Block.txt"):
    block_list = []
    for line in open(file_path, "r"):
        if not line == "":
            block_list.append(line.strip())
    return block_list


def add_to_blocklist(file_path="C:\SpotiBlock\Block.txt"):
    with open(file_path, 'a') as text_file:
        text_file.write("\n" + song_info())


def reset_blocklist(file_path="C:\SpotiBlock\Block.txt"):
    with open(file_path, 'w') as text_file:
        text_file.write("ThisFirstLineWillBeIgnored")
        pass


###Media Controls###
def hwcode(Media):
    hwcode = win32api.MapVirtualKey(Media, 0)
    return hwcode


def next():
    if platform.system() == 'Linux':
        bus = dbus.SessionBus()
        proxy = bus.get_object(
            'org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
        interface = dbus.Interface(
            proxy, dbus_interface='org.mpris.MediaPlayer2.Player')
        interface.Next()
    elif platform.system() == 'Windows':
        win32api.keybd_event(Media_Next, hwcode(Media_Next))


def previous():
    if platform.system() == 'Linux':
        bus = dbus.SessionBus()
        proxy = bus.get_object(
            'org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
        interface = dbus.Interface(
            proxy, dbus_interface='org.mpris.MediaPlayer2.Player')
        interface.Previous()
    elif platform.system() == 'Windows':
        win32api.keybd_event(Media_Previous, hwcode(Media_Previous))


def pause():
    if platform.system() == 'Linux':
        bus = dbus.SessionBus()
        proxy = bus.get_object(
            'org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
        interface = dbus.Interface(
            proxy, dbus_interface='org.mpris.MediaPlayer2.Player')
        interface.PlayPause()
    elif platform.system() == 'Windows':
        win32api.keybd_event(Media_Pause, hwcode(Media_Pause))


def play():
    if platform.system() == 'Linux':
        bus = dbus.SessionBus()
        proxy = bus.get_object(
            'org.mpris.MediaPlayer2.spotify', '/org/mpris/MediaPlayer2')
        interface = dbus.Interface(
            proxy, dbus_interface='org.mpris.MediaPlayer2.Player')
        interface.PlayPause()
    elif platform.system() == 'Windows':
        win32api.keybd_event(Media_Pause, hwcode(Media_Pause))


def mute():
    win32api.keybd_event(Media_Mute, hwcode(Media_Mute))
