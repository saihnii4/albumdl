#!/usr/bin/python3

import os
import sys
import logging

import spotipy
import requests
from yt_dlp import YoutubeDL
from spotipy.oauth2 import SpotifyClientCredentials

WORKING_DIR = os.path.dirname(__file__)

YDL_OPTS = {
    "format": "mp3/bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3"
        },
    ],
}

if __name__ == "__main__":
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ['CLIENT_ID'],
                                                               client_secret=os.environ['CLIENT_SECRET']))

    arg = sys.stdin.readline().strip()
    uri = arg.split(" ")[-1][1:-1]
    print(uri.encode())

    track = sp.track(uri)
    album = sp.album(track['album']['uri'])

    artists = ", ".join(map(lambda a: a['name'], album["artists"]))
    
    try:
        os.mkdir(os.path.join(WORKING_DIR, "albums/%s" % album['name']))
    except:
        logging.debug("Album directory already exists, skipping...")
        pass # STFU


    with open(os.path.join(WORKING_DIR, "albums/%s/cover.png" % album['name']), "wb+") as cover:
        cover.write(requests.get(album['images'][0]['url']).content)

    for track in album['tracks']['items']:
        query = '%s - %s' % (track['name'], artists)

        YDL_OPTS["outtmpl"] = os.path.join(WORKING_DIR, "albums/{}/{}.%(ext)s".format(album['name'], query))
        ydl = YoutubeDL(YDL_OPTS)
        ydl.download('ytsearch:' + query)

