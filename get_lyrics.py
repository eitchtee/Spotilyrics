import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
from unicodedata import normalize
from PyLyrics import *
import os
# from requests import ConnectionError, HTTPError, Timeout


def get(artist, song):
    def lyricsdotcom(artist, song):
        artist = artist.replace("'", '').replace('-', '')
        song = song.replace("'", '').replace('-', '')
        # Replace spaces with dashes to imporve URL logging.
        regex_spaces = re.compile(r'[\s]+', re.UNICODE)
        artist = regex_spaces.sub('-', artist)
        song = regex_spaces.sub('-', song)
        # This regex mathches anything other than Alphanumeric, spaces and
        # dashes
        # and removes them.
        # Make regex unicode aware 're.UNICODE' for Python27. It is redundant
        # for
        # Python3.
        regex_non_alphanum = re.compile(r'[^\w\s\-]*', re.UNICODE)
        artist = regex_non_alphanum.sub('', artist)
        song = regex_non_alphanum.sub('', song)
        url = 'http://www.lyrics.com/%s-lyrics-%s.html' % (quote(
            song), quote(artist))
        print('Trying:', url, '\n')
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html.parser')
            lyrics = soup.find(itemprop='description')
            if lyrics is not None:
                lyrics = str(lyrics).replace('<br>', '\n\n').replace(
                    '<p>', '').replace('<br/>', '').replace('</div>', '')
                lyrics = lyrics.replace(
                    '<div class="SCREENONLY" id="lyrics" itemprop="description">', '')
                sep = '---'
                lyrics = lyrics.split(sep, 1)[0]

                return lyrics
            else:
                return None
        except:
            return None

    def metrolyrics(artist, song):
        artist = artist.replace("'", '').replace('&', 'and').replace('-', '')
        song = song.replace("'", '').replace('-', '')
        # Replace spaces with dashes to imporve URL logging.
        regex_spaces = re.compile(r'[\s]+', re.UNICODE)
        artist = regex_spaces.sub('-', artist)
        song = regex_spaces.sub('-', song)
        # This regex mathches anything other than Alphanumeric, spaces and
        # dashes
        # and removes them.
        # Make regex unicode aware 're.UNICODE' for Python27. It is redundant
        # for
        # Python3.
        regex_non_alphanum = re.compile(r'[^\w\s\-]*', re.UNICODE)
        artist = regex_non_alphanum.sub('', artist)
        song = regex_non_alphanum.sub('', song)
        url = 'http://www.metrolyrics.com/%s-lyrics-%s.html' % (quote(
            song), quote(artist))
        print('Trying:', url)
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html.parser')
            lyrics = soup.find(id='lyrics-body-text')
            if lyrics is not None:
                lyrics = str(lyrics).replace(
                    '\n', '').replace('<br>', '\n').replace(
                    '</p>', '\n\n').replace('<p>', '').replace(
                    '</br>', '').replace('</div>', '')
                lyrics = lyrics.replace('<p class="verse">', '').replace(
                    '<div class="js-lyric-text" id="lyrics-body-text">', '')
                return lyrics
            else:
                return None
        except:
            return None

    def letrasmusbr(artist, song):
        # Replace spaces with dashes to imporve URL logging.
        regex_spaces = re.compile(r'[\s]+', re.UNICODE)
        artist = regex_spaces.sub('-', artist)
        song = regex_spaces.sub('-', song)
        # Replace upper(apostrophe) commas with dashes '-'
        artist = artist.replace("'", '')
        song = song.replace("'", '')
        # This regex mathches anything other than Alphanumeric, spaces and
        # dashes
        # and removes them.
        # Make regex unicode aware 're.UNICODE' for Python27. It is redundant
        # for
        # Python3.
        regex_non_alphanum = re.compile(r'[^\w\s\-]*', re.UNICODE)
        artist = regex_non_alphanum.sub('', artist)
        song = regex_non_alphanum.sub('', song)
        url = 'https://www.letras.mus.br/%s/%s' % (
            quote(artist), quote(song))
        print('Trying:', url)
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            lyrics = soup.find(class_='cnt-letra')
            if lyrics is not None:
                lyrics = str(lyrics).replace(
                    '\n', '').replace('<br/>', '\n').replace(
                    '</p>', '\n\n').replace('<p>', '')
                lyrics = lyrics.replace(
                    '<div class="cnt-letra p402_premium"> ', '').replace(
                    '</div>', '')
                lyrics = lyrics.replace(
                    '<article> ', '').replace('</article>', '')
                return lyrics
            else:
                return None
        except Exception:
            return None

    def vagalume(artist, song):
        # Replace spaces with dashes to imporve URL logging.
        regex_spaces = re.compile(r'[\s]+', re.UNICODE)
        artist = regex_spaces.sub('-', artist)
        song = regex_spaces.sub('-', song)
        # Replace upper(apostrophe) commas with nothing
        artist = artist.replace("'", '')
        song = song.replace("'", '')
        # This regex mathches anything other than Alphanumeric, spaces and
        # dashes
        # and removes them.
        # Make regex unicode aware 're.UNICODE' for Python27. It is redundant
        # for
        # Python3.
        regex_non_alphanum = re.compile(r'[^\w\s\-]*', re.UNICODE)
        artist = regex_non_alphanum.sub('', artist)
        song = regex_non_alphanum.sub('', song)
        url = 'https://www.vagalume.com.br/%s/%s.html' % (
            quote(artist), quote(song))
        print('Trying:', url)
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            lyrics = soup.find(itemprop='description')
            if lyrics is not None:
                lyrics = str(lyrics).replace(
                    '\n', '').replace('<br/>', '\n')
                lyrics = lyrics.replace('<div itemprop="description">', '')
                lyrics = lyrics.replace('</div>', '')
                return lyrics
            else:
                return None
        except:
            return None

    def handler(artist, song):
        lyrics = vagalume(artist, song)
        if lyrics is not None:
            return lyrics
        else:
            lyrics = letrasmusbr(artist, song)
            if lyrics is not None:
                return lyrics
            else:
                lyrics = metrolyrics(artist, song)
                if lyrics is not None:
                    return lyrics
                else:
                    lyrics = lyricsdotcom(artist, song)
                    if lyrics is not None:
                        return lyrics
                    else:
                        return None

    def lyricswikia(artist, song):
        print('Trying: PyLyrics with "{0} - {1}"'.format(song, artist))
        try:
            lyrics = PyLyrics.getLyrics(artist, song)
        except ValueError:
            return None
        else:
            return lyrics

    # Prints song name and artist for console logging
    print(song, '-', artist)
    # Removes exerything after a " - " on a song title
    song = song.split(' - ', 1)[0]

    # checks if there is a file with the song name and artist on
    # the lyrics folder
    print('Checking for saved lyrics')
    if os.path.isfile('{0}/lyrics/{1} - {2}.txt'.format(
            os.getcwd(), song, artist)):
        print('Found! \n')
        with open('{0}/lyrics/{1} - {2}.txt'.format(
                os.getcwd(), song, artist), 'r') as lyricfile:
            lyrics = lyricfile.read()
            lyricfile.close()
        return lyrics

    else:
        lyrics = lyricswikia(artist, song)
        if lyrics is not None:
            print('Found! \n')
            return lyrics
        else:
            song = normalize('NFKD', song).encode('ASCII', 'ignore').decode(
                'ASCII')
            artist = normalize('NFKD', artist).encode(
                'ASCII', 'ignore').decode('ASCII')
            song = song.lower()
            artist = artist.lower()

            lyrics = handler(artist, song)
            if lyrics is not None:
                print('Found! \n')
                return lyrics
            else:
                print('Not found! \n')
                return 'Lyric not found'
