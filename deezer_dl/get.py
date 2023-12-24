import requests
from pprint import pformat

from concurrent.futures.process import ProcessPoolExecutor
google_service_name = "youtube"
youtube_api_version = "v3"
video = 'video'
youtube_url_pattern = 'https://www.youtube.com/watch?v='

import os

from googleapiclient.discovery import build

import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials


from pydub import AudioSegment
from pytube import YouTube
from tqdm import tqdm


import sys

import requests

from bs4 import BeautifulSoup

from moviepy.editor import *

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


import glob

import numpy as np

import shutil





spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())



s =  \
"""All I need de lloyd
All by myself de Ellie Goulding et David Guetta 
Drunk in love Beyoncé et Jay-Z 
Outside Calvin Harris et Ellie Goulding 
Havana, Shameless, crying in the club de Camilla Cabello
Can't remember to forger you Rihanna et Shakira 
Doing it Charlie XCX et Rita Ora 
Change your life Iggy azalea 
Friends et slow down, swim de chase Atlantic 
Cool for the summer de Demi Lovato 
Crazy Kids de Kesha 
I'm good de David Guetta 
God's plan de Drake 
Shape of you de Ed Sheeran 
Feeling good de Mickaël Buble
That's my girl de fifth harmony
Right round de Florida
Friday de dopamine edit
Una vaina loca de Fuego (ou l'inverse)
It's my life de bon jovi
Juice et 2 be loved de Lizzo
Collide de Justine Skye et Tyga
All the stars de Kendrick Lamar et sza
Do it right de Martin Solveig 
Me and u de cassie 
2 on de tinashe
No lie de Sean Paul et dua lipa
Or nah de the weekend et ty dolla sign
Poker face de lady gaga
The way I are de timbaland
Waves de yonaka
"""


def moveFile(origine, destination):
    print("moving file from: "+ origine+ " to: "+destination)
    shutil.move(origine, destination)


urls = {}

lines = s.split('\n')
print(lines)
for line in lines:
    print(line)


    search = line

    results = spotify.search(q=search, type='track')

    url = results["tracks"]['items'][0]['external_urls']['spotify']

    print(url)

    urls[line] = url

print(urls)



