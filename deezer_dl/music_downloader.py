
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


exportFolder = "C:/Users/vultorio/Desktop/"


def addMeta(title, artist, album, path):

    filez = glob.glob(path)
    # loop through the mp3 files, extracting the track number,
    # then setting the album, albumartist and track number
    # to the appropriate values
    for i in np.arange(0, len(filez)):
        # extract the length of the directory
        length_directory = len(filez[i].split("/"))
        # extract the track number from the last element of the file path
        tracknum = filez[i].split("/")[length_directory - 1][0:2]
        # mp3 name (with directory) from filez
        song = filez[i]
        # turn it into an mp3 object using the mutagen library
        mp3file = MP3(song, ID3=EasyID3)
        # set the album name
        mp3file['title'] = [title]
        mp3file['album'] = [album]

        # set the albumartist name
        mp3file['artist'] = [artist]

        # save the changes that we've made
        mp3file.save()

import shutil

def moveFile(origine, destination):
    print("moving file from: "+ origine+ " to: "+destination)
    shutil.move(origine, destination)

def mp4tomp3(mp4file, mp3file):
    videoclip = VideoFileClip(mp4file)
    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3file)
    audioclip.close()
    videoclip.close()



def __download_songs(url, title, artist, album):
    """
           Downloads songs from the YouTube URL passed to either
              current directory or download_directory, is it is filled.
           """

    def on_progress(stream, chunk, file_handle):
        pbar.update(len(chunk))

    print('Downloading from: {url}'.format(url=url))
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True).order_by('abr').last()
    print('Stream: {}'.format(stream))

    total_size = stream.filesize
    print('File size: {}'.format(total_size))
    pbar = tqdm(total=total_size)
    yt.register_on_progress_callback(on_progress)
    output_path = os.path.join(os.getcwd(), 'deezer_dl', 'songs')
    os.makedirs(output_path, exist_ok=True)
    file_location = stream.download(output_path=output_path)
    file_location = str(file_location)
    file_location = file_location.replace('*', "")

    title = title.replace('*', "")
    title = title.replace("’", "")
    title = title.replace("'", "")
    title = title.replace("?", "")

    print('File location: {}'.format(file_location))
    mp4tomp3(file_location, os.path.join(output_path, title) + '.mp3')
    os.remove(file_location)
    addMeta(title, artist, album, os.path.join(output_path, title) + '.mp3')
    pbar.close()



#http://www.deezer.com/playlist/11366038524

def fetch_tracks_from_playlist(playlist):
    """Fetches tracks from deezer tracks or from playlist."""

    print('Fetching tracks from playlist.')
    songs_list = list()
    url_playlist = playlist.replace('www', 'api')
    data = requests.get(url_playlist).json()
    res = requests.get(url_playlist).json()['tracks']['data']
    #print('Result from Deezer API: {}'.format(pformat(res)))

    playlistTitle = data['title']

    songs = []

    export = exportFolder+"/music/"
    # Check whether the specified path exists or not
    isExist = os.path.exists(export)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(export)
        print("The new directory is created: " + export)

    export = exportFolder+"/music/"+playlistTitle+"/"
    # Check whether the specified path exists or not
    isExist = os.path.exists(export)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(export)
        print("The new directory is created: " + export)

    moi = exportFolder+"/music/"+playlistTitle+"/transit"
    # Check whether the specified path exists or not
    isExist = os.path.exists(moi)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(moi)
        print("The new directory is created: " + moi)

    downloadList = []

    for x in res:
        title = x['title']
        artiste = x['artist']['name']
        album = x['album']['title']

        title = title.replace("?","")

        song = {'title': title, 'artist': artiste, 'album': album}
        songs.append(song)


        check = True

        for path in os.listdir(export):
            # check if current path is a file
            if os.path.isfile(os.path.join(export, path)):
                if title in path:
                    check = False
                    break

                else:
                    check = True

        if check == True:
            downloadList.append(title)

    i = 0

    for x in res:
        title = x['title']
        artiste = x['artist']['name']
        album = x['album']['title']

        title = title.replace("?","")

        song = {'title': title, 'artist': artiste, 'album': album}
        songs.append(song)


        check = True

        for path in os.listdir(export):
            # check if current path is a file
            if os.path.isfile(os.path.join(export, path)):
                #print(title + " :::: " + (path))
                if title in path:
                    #print(title + " :::: "+ (path))
                    #print(title + " is alrweady doawload")
                    check = False
                    break

                else:

                    check = True


        #print(check)

        if check == True:
            qsearch = ' '.join([title, artiste])

            spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

            print("download list = "+ str(downloadList))

            print('song:' + title + " " + artiste + " " + album + " on " + str(len(downloadList)))

            search = title + " " + artiste + " " + album

            results = spotify.search(q=search, type='track')

            url = results["tracks"]['items'][0]['external_urls']['spotify']

            print("downloading : " +title)
            os.system(".\spotdl.exe " + url)
            for path in os.listdir(os.getcwd()):
                # check if current path is a file
                if os.path.isfile(os.path.join(os.getcwd(), path)):
                    if ".mp3" in path:
                        print(path)
                        print(export + artiste+ " - " + title+".mp3")
                        moveFile(os.getcwd() + "/" + path, export + "transit/"+artiste+ " - " + title+".mp3")

            i = i+1



    print(songs)





# 3 https://www.deezer.com/playlist/11366444044
# 4 https://www.deezer.com/playlist/11366812924


fetch_tracks_from_playlist("https://www.deezer.com/playlist/11366812924")