from __future__ import unicode_literals

import os
import sys
from concurrent.futures.process import ProcessPoolExecutor
from pprint import pformat

import requests
from googleapiclient.discovery import build
from pydub import AudioSegment
from pytube import YouTube
from tqdm import tqdm

from deezer_dl import logger
from deezer_dl.model import DeezerDLmodel
from deezer_dl.utils import google_service_name, youtube_api_version, video, youtube_url_pattern


class Deezer:

    def __init__(self, url, _dir=None):
        self.url = url
        self.logger = logger
        self.dir = _dir or os.path.expanduser('~')

    def download(self):

        songs = list()
        if 'playlist' in self.url:
            self.logger.info('A Playlist was found.')
            songs = self.fetch_tracks_from_playlist(self.url)
        if 'track' in self.url:
            self.logger.info('A Track was found.')
            songs = self.fetch_track_from_url(self.url)

        for song in songs:
            title = [song[k]['title'] for k in song.keys()][0]
            artist = [k for k in song.keys()][0]
            youtube_url = ''.join([youtube_url_pattern, [song[k]['sha1'] for k in song.keys()][0]])
            self.logger.info('Downloading {} - {} from {}'.format(title, artist, youtube_url))
            s = [song[k]['sha1'] for k in song.keys()]
            self.__download_songs(s[0])

    def __download_songs(self, url):
        """
        Downloads songs from the YouTube URL passed to either
           current directory or download_directory, is it is filled.
        """

        def on_progress(stream, chunk, file_handle, bytes_remaining):
            pbar.update(len(chunk))

        url = youtube_url_pattern + url
        self.logger.info('Downloading from: {url}'.format(url=url))
        yt = YouTube(url)
        stream = yt.streams.filter(subtype='mp4', progressive=True).order_by('abr').last()
        self.logger.debug('Stream: {}'.format(stream))
        try:
            total_size = stream.filesize
            self.logger.debug('File size: {}'.format(total_size))
            pbar = tqdm(total=total_size)
            yt.register_on_progress_callback(on_progress)
            output_path = os.path.join(self.dir, 'deezer_dl', 'songs')
            os.makedirs(output_path, exist_ok=True)
            file_location = stream.download(output_path=output_path)
            self.logger.info('File location: {}'.format(file_location))
            AudioSegment.from_file(file_location).export(os.path.join(output_path, yt.title) + '.mp3', format="mp3")
            os.remove(file_location)
            pbar.close()
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            self.logger.info('Error: {}'.format(e))

    def fetch_tracks_from_playlist(self, playlist):
        """Fetches tracks from deezer tracks or from playlist."""

        self.logger.debug('Fetching tracks from playlist.')
        songs_list = list()
        url_playlist = playlist.replace('www', 'api')
        res = requests.get(url_playlist).json()['tracks']['data']
        self.logger.debug('Result from Deezer API: {}'.format(pformat(res)))

        with ProcessPoolExecutor(max_workers=15) as executor:
            for r in executor.map(self.fetch_yt_url, res):
                songs_list.append(r)
        return songs_list

    def fetch_track_from_url(self, url_track):
        self.logger.debug('Fetching tracks from deezer url.')
        song = list()
        url_track = url_track.replace('www', 'api')
        res = requests.get(url_track).json()
        self.logger.debug('Result from Deezer API: {}'.format(pformat(res)))
        song.append(self.fetch_yt_url(res))
        return song

    def fetch_yt_url(self, search_term):
        """For each song name/artist name combo, fetch the YouTube URL
            and return the list of URLs"""

        item = DeezerDLmodel.find_by_song(search_term["title"])

        if item:
            return item.json()

        youtube_dev_key = os.getenv('YOUTUBE_DEV_KEY')
        self.logger.debug('Youtube dev key: {}'.format(youtube_dev_key))
        youtube = build(google_service_name, youtube_api_version, developerKey=youtube_dev_key, cache_discovery=False)
        qsearch = ' '.join([search_term['title'], search_term['artist']['name']])
        self.logger.info("Searching for {}".format(qsearch))
        search_response = youtube.search().list(q=qsearch,
                                                part='id, snippet',
                                                order='relevance',
                                                type='video',
                                                maxResults=1).execute()
        for v in search_response['items']:
            if v['id']['kind'] == video:
                self.logger.debug('Adding Video id {}'.format(v['id']['videoId']))
                add_song = DeezerDLmodel(artist=search_term["artist"]["name"],
                                         song=search_term["title"],
                                         sha1=v['id']['videoId'])

                try:
                    add_song.save_to_db()
                except Exception as e:
                    self.logger.error('Error: {0}'.format(e))

                return add_song.json()
