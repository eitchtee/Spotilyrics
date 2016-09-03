# Spotilyrics

With the removal of the Lyrics feature from Spotify, i've decided to hack together a tool to sort of replace that, and with that came Spotilyrics, it automatically fetch and shows you the lyrics from the songs you are listening, and even allows you to pause or skip a song.

---
### Warnings

* Currently this script is WINDOWS only
* There are no binaries avaliable, although that is on the TO-DO list

---

### How to Install
While there are no binaries for ease of use, you'll have to do the following:

1. You will need [PyLyric](https://pypi.python.org/pypi/PyLyrics/1.1.0)

  `pip install PyLyrics`

2. Get the `spotilib.py` file from [here](https://github.com/XanderMJ/spotilib), and place it on the same folder as our script.

3. Run your main Spotify program.

4. Run the `spotilyrics.py` script.

5. Enjoy your lyrics.

---

### To-Do
* Make the overall app look nicer
* Compile .exe files
* Add other ways than PyLyrics to find lyrics, in case that fails to find what you want
