# Spotilyrics

With the removal of the Lyrics feature from Spotify, i've decided to hack together a tool to sort of replace that, and with that came Spotilyrics, it automatically fetch and shows you the lyrics from the songs you are listening, and even allows you to pause or skip a song.

---

### Install
<p align="center">
  <a href="https://github.com/eitchtee/Spotilyrics/releases/latest"><img src="http://imgur.com/NmGvnqx.png"></a><br>
  For Linux and Windows
</p>

### Manual Install(**Windows and Linux only**)

1. You will need Python 3.5

2. You will need [PyLyrics](https://pypi.python.org/pypi/PyLyrics/1.1.0)

  `pip install PyLyrics`

3. Run your main Spotify program

4. Run the `spotilyrics.py` script

5. Enjoy your lyrics!

---

### Troubleshooting

1. **Missing mcvcr100.dll on Windows**  
Download Microsoft Visual C++ 2010 Redistributable [32bit(x86)](https://www.microsoft.com/en-us/download/details.aspx?id=5555) or [64bit(x64)](https://www.microsoft.com/en-us/download/details.aspx?id=14632)

2. **Missing api-ms-win-crt-runtime-l1-1-0.dll on Windows**  
Check if your have the Windows Update [KB2999226](https://support.microsoft.com/en-gb/kb/2999226) installed on your system, if you don't, install it.  
In case the error persists, install Visual C++ Redistributable for Visual Studio 2015. [32bit](http://download.microsoft.com/download/9/3/F/93FCF1E7-E6A4-478B-96E7-D4B285925B00/vc_redist.x86.exe) or [64bit](http://download.microsoft.com/download/9/3/F/93FCF1E7-E6A4-478B-96E7-D4B285925B00/vc_redist.x64.exe)


---
### Thanks and Credits
* Thanks to [XanderMJ](https://github.com/XanderMJ/) for creating the great [spotilib](https://github.com/XanderMJ/spotilib) which without it this project wouldn't be possible
* Thanks to [Ernesto Savoretti](https://sourceforge.net/u/sandy2008/) for fixig the [pmwbundle.py](https://sourceforge.net/p/pmw/discussion/131281/thread/24235048/) code and posting it on some obscure sourceforge thread
* Icons made by Freepik from www.flaticon.com
