# Spotilyrics

With the removal of the Lyrics feature from Spotify, i've decided to hack together a tool to sort of replace that, and with that came Spotilyrics, it automatically fetch and shows you the lyrics from the songs you are listening, and even allows you to pause or skip a song.

---
### Warnings

* Currently this script is WINDOWS only
* There are no binaries avaliable, although that is on the TO-DO list

---

### How to Install
**You can just download the executable [here](https://github.com/eitchtee/Spotilyrics/releases/latest)**

Or if you prefer thing the hard way:

1. You will need Python 3.5(this is the version it is developed and tested on, altough it may work on Python 3.x)

2. You will need [PyLyric](https://pypi.python.org/pypi/PyLyrics/1.1.0)

  `pip install PyLyrics`
  
3. And Pmw

  `pip install Pmw`

4. Run your main Spotify program

5. Run the `spotilyrics.py` script

6. Enjoy your lyrics!

---

### To-Do
* Make the overall app look nicer
* Compile .exe files
* Add other ways than PyLyrics to find lyrics, in case that fails to find what you want
