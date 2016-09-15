import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
from unicodedata import normalize
from PyLyrics import *
# from requests import ConnectionError, HTTPError, Timeout


def get(artist, song):
    def lyricswikia(artist, song):
        try:
            lyrics = PyLyrics.getLyrics(artist, song)
        except ValueError:
            return None
        else:
            return lyrics

    def letrasmusbr(artist, song):
        url = 'https://www.letras.mus.br/%s/%s' % (
            quote(artist), quote(song))
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
        except:
            return None

    def vagalume(artist, song):
        url = 'https://www.vagalume.com.br/%s/%s.html' % (
            quote(artist), quote(song))
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
                letrasmusbr(artist, song)
        except:
            letrasmusbr(artist, song)

    lyrics = lyricswikia(song, artist)
    if lyrics is not None:
        return lyrics
    else:
        # Replace upper(apostrophe) commas with dashes '-'
        artist = artist.replace("'", '-')
        song = song.replace("'", '-')
        # This regex mathches anything other than Alphanumeric, spaces and
        # dashes
        # and removes them.
        # Make regex unicode aware 're.UNICODE' for Python27. It is redundant
        # for
        # Python3.
        regex_non_alphanum = re.compile(r'[^\w\s\-]*', re.UNICODE)
        artist = regex_non_alphanum.sub('', artist)
        song = regex_non_alphanum.sub('', song)
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
        lyrics = vagalume(artist, song)
        if lyrics is None:
            return 'Lyric not found'
        else:
            return lyrics
