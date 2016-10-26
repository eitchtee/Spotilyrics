# Spotilyrics

With the removal of the Lyrics feature from Spotify, i've decided to hack together a tool to sort of replace that, and with that came Spotilyrics, it automatically fetch and shows you the lyrics from the songs you are listening, and even allows you to pause or skip a song.

**THIS IS WINDOWS AND LINUX ONLY**

---
### Screenshots

Windows 10 and Linux Mint 17 respectively:

![on Windows 10](http://imgur.com/90WRfBb.png "on Windows 10") ![on Linux Mint 17](http://imgur.com/KKWG9OI.png "on Linux Mint 17")  

---

### Install
<p align="center">
  <a href="https://github.com/eitchtee/Spotilyrics/releases/latest"><img src="http://imgur.com/NmGvnqx.png"></a><br>
  For Windows
</p>

As of v1.1.0-beta I've stopped doing Linux executables due to a unknown bug between PIL and Pyinstaller, guiven the circunstance, use the guide below to use this script on Linux.

### Manual Install

1. You will need Python 3.x
  
2. Intall [Spotipy](https://pypi.python.org/pypi/spotipy)

  `pip install Spotipy`
  
3. Install [PIL](https://pypi.python.org/pypi/image/1.5.5)

  `pip install Image`

4. Run Spotify

5. Run the `spotilyrics.py` script

6. Enjoy your lyrics!

---

### Troubleshooting

1. **Missing mcvcr100.dll on Windows**  
Download Microsoft Visual C++ 2010 Redistributable [32bit(x86)](https://www.microsoft.com/en-us/download/details.aspx?id=5555) or [64bit(x64)](https://www.microsoft.com/en-us/download/details.aspx?id=14632)

2. **Missing api-ms-win-crt-runtime-l1-1-0.dll on Windows**  
Check if your have the Windows Update [KB2999226](https://support.microsoft.com/en-gb/kb/2999226) installed on your system, if you don't, install it.  
In case the error persists, install Visual C++ Redistributable for Visual Studio 2015. [32bit](http://download.microsoft.com/download/9/3/F/93FCF1E7-E6A4-478B-96E7-D4B285925B00/vc_redist.x86.exe) or [64bit](http://download.microsoft.com/download/9/3/F/93FCF1E7-E6A4-478B-96E7-D4B285925B00/vc_redist.x64.exe)

---

### Credits
* Icons made by Freepik from www.flaticon.com
