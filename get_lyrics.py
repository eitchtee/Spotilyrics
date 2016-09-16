import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
from unicodedata import normalize
from PyLyrics import *
# from requests import ConnectionError, HTTPError, Timeout


def get(artist, song):
    def lyricsdotcom(artist, song):
        n_artist = artist.replace("'", '').replace('-', '')
        n_song = song.replace("'", '').replace('-', '')
        # This regex mathches anything other than Alphanumeric, spaces and
        # dashes
        # and removes them.
        # Make regex unicode aware 're.UNICODE' for Python27. It is redundant
        # for
        # Python3.
        regex_non_alphanum = re.compile(r'[^\w\s\-]*', re.UNICODE)
        n_artist = regex_non_alphanum.sub('', n_artist)
        n_song = regex_non_alphanum.sub('', n_song)
        url = 'http://www.lyrics.com/%s-lyrics-%s.html' % (quote(
            n_song), quote(n_artist))
        print('Trying ', url, '\n')
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
        n_artist = artist.replace("'", '').replace('&', 'and').replace('-', '')
        n_song = song.replace("'", '').replace('-', '')
        # This regex mathches anything other than Alphanumeric, spaces and
        # dashes
        # and removes them.
        # Make regex unicode aware 're.UNICODE' for Python27. It is redundant
        # for
        # Python3.
        regex_non_alphanum = re.compile(r'[^\w\s\-]*', re.UNICODE)
        n_artist = regex_non_alphanum.sub('', n_artist)
        n_song = regex_non_alphanum.sub('', n_song)
        url = 'http://www.metrolyrics.com/%s-lyrics-%s.html' % (quote(
            n_song), quote(n_artist))
        print('Trying ', url)
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
        # Replace upper(apostrophe) commas with dashes '-'
        n_artist = artist.replace("'", '')
        n_song = song.replace("'", '')
        # This regex mathches anything other than Alphanumeric, spaces and
        # dashes
        # and removes them.
        # Make regex unicode aware 're.UNICODE' for Python27. It is redundant
        # for
        # Python3.
        regex_non_alphanum = re.compile(r'[^\w\s\-]*', re.UNICODE)
        n_artist = regex_non_alphanum.sub('', n_artist)
        n_song = regex_non_alphanum.sub('', n_song)
        url = 'https://www.letras.mus.br/%s/%s' % (
            quote(n_artist), quote(n_song))
        print('Trying ', url)
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
        # Replace upper(apostrophe) commas with nothing
        n_artist = artist.replace("'", '')
        n_song = song.replace("'", '')
        # This regex mathches anything other than Alphanumeric, spaces and
        # dashes
        # and removes them.
        # Make regex unicode aware 're.UNICODE' for Python27. It is redundant
        # for
        # Python3.
        regex_non_alphanum = re.compile(r'[^\w\s\-]*', re.UNICODE)
        n_artist = regex_non_alphanum.sub('', n_artist)
        n_song = regex_non_alphanum.sub('', n_song)
        url = 'https://www.vagalume.com.br/%s/%s.html' % (
            quote(n_artist), quote(n_song))
        print('Trying ', url)
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
        print('Trying PyLyrics with "', song, '-', artist + '"')
        try:
            lyrics = PyLyrics.getLyrics(artist, song)
        except ValueError:
            return None
        else:
            return lyrics

    print(song, '-', artist)
    song = song.split(' - ', 1)[0]
    lyrics = lyricswikia(artist, song)
    if lyrics is not None:
        print('Found! \n')
        return lyrics
    else:
        # Replace spaces with dashes to imporve URL logging.
        regex_spaces = re.compile(r'[\s]+', re.UNICODE)
        artist = regex_spaces.sub('-', artist)
        song = regex_spaces.sub('-', song)
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
