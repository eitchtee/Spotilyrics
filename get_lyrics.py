import requests
import re
from bs4 import BeautifulSoup, Comment
from urllib.parse import quote
from unicodedata import normalize
import os
import urllib.request as ur


def internet_on():
    try:
        stri = "https://www.google.com"
        ur.urlopen(stri)
    except Exception:
        return False
    else:
        return True


def saved_lyric(artist, song):
    # checks if there is a file with the song name and artist on
    # the lyrics folder
    print('Checking for saved lyrics')
    song = song.split(' - ', 1)[0]
    filepath = os.getcwd()
    if os.path.isfile('{0}/lyrics/{1} - {2}.txt'.format(
            filepath, song, artist)):
        with open('{0}/lyrics/{1} - {2}.txt'.format(
                filepath, song, artist), 'r') as lyricfile:
            lyrics = lyricfile.read()
            lyricfile.close()
        return lyrics
    else:
        return None


def lyricswikia(artist, song):
    # original code found @
    # https://github.com/geekpradd/PyLyrics/blob/master/PyLyrics/functions.py
    song = song.split(' - ', 1)[0]
    artist = artist.replace(' ', '_')
    song = song.replace(' ', '_')
    url = 'http://lyrics.wikia.com/{0}:{1}'.format(artist, song)
    print('Trying:', url)
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'html.parser')
    # Get main lyrics holder
    lyrics = s.find("div", {'class': 'lyricbox'})
    if lyrics is not None:
        # Remove Scripts
        [s.extract() for e in lyrics('script')]

        # Remove Comments
        comments = lyrics.findAll(text=lambda text: isinstance(text, Comment))
        [comment.extract() for comment in comments]

        # Remove unecessary tags
        for tag in ['div', 'i', 'b', 'a']:
            for match in lyrics.findAll(tag):
                match.replaceWithChildren()
        # Get output as a string and remove non unicode characters and replace
        # <br> with newlines
        lyrics = str(lyrics).encode('utf-8', errors='replace')[22:-6:].decode(
            "utf-8").replace('\n', '').replace('<br/>', '\n')
    try:
        return lyrics
    except:
        return lyrics.encode('utf-8')


def vagalume(artist, song):
    # Removes exerything after a " - " on a song title
    song = song.split(' - ', 1)[0]
    song = normalize('NFKD', song).encode('ASCII', 'ignore').decode('ASCII')
    artist = normalize('NFKD', artist).encode(
        'ASCII', 'ignore').decode('ASCII')
    song = song.lower()
    artist = artist.lower()
    # Replace spaces with dashes to improve URL logging.
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


def letrasmusbr(artist, song):
    # Removes exerything after a " - " on a song title
    song = song.split(' - ', 1)[0]
    song = normalize('NFKD', song).encode('ASCII', 'ignore').decode('ASCII')
    artist = normalize('NFKD', artist).encode(
        'ASCII', 'ignore').decode('ASCII')
    song = song.lower()
    artist = artist.lower()
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


def metrolyrics(artist, song):
    # Removes exerything after a " - " on a song title
    song = song.split(' - ', 1)[0]
    song = normalize('NFKD', song).encode('ASCII', 'ignore').decode('ASCII')
    artist = normalize('NFKD', artist).encode(
        'ASCII', 'ignore').decode('ASCII')
    song = song.lower()
    artist = artist.lower()
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


def lyricsdotcom(artist, song):
    # Removes exerything after a " - " on a song title
    song = song.split(' - ', 1)[0]
    song = normalize('NFKD', song).encode('ASCII', 'ignore').decode('ASCII')
    artist = normalize('NFKD', artist).encode(
        'ASCII', 'ignore').decode('ASCII')
    song = song.lower()
    artist = artist.lower()
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
            lyrics = lyrics.split('---', 1)[0]

            return lyrics
        else:
            return None
    except:
        return None
