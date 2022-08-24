#!/usr/bin/python3

import json
import os
import sys
import eyed3
import logging

import spotipy
import requests
from yt_dlp import YoutubeDL
from spotipy.oauth2 import SpotifyClientCredentials

# two iterations cause __file__ includes a period for some reason
WORKING_DIR = os.path.dirname(os.path.dirname(__file__))

logger = logging.getLogger("yt-dlp")
logger.setLevel(logging.INFO)

YDL_OPTS = {
    "format": "mp3/bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3"
        },
    ],
    "logger": logger
}

if __name__ == "__main__":
    HOME = os.path.expanduser("~")
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ['CLIENT_ID'],
                                                               client_secret=os.environ['CLIENT_SECRET']))

    arg = sys.stdin.readline().strip()
    uri = arg.split(" ")[-1][1:-1]

    track = sp.track(uri)
    album = sp.album(track['album']['uri'])

    artists = ", ".join(map(lambda a: a['name'], album["artists"]))
    
    ALBUM_DIR = os.path.join(WORKING_DIR, "albums/{}".format(album['name']))

    if os.path.exists(ALBUM_DIR):
        logging.info("Noticed album directory already exists, skipping to configuration")
    else:
        os.mkdir(ALBUM_DIR)

        with open(os.path.join(ALBUM_DIR, "cover.png"), "wb+") as cover:
            cover.write(requests.get(album['images'][0]['url']).content)

        for track in album['tracks']['items']:
            query = '%s - %s' % (track['name'], artists)

            print("\033[1mDownloading %s\033[0m" % query)

            YDL_OPTS["outtmpl"] = os.path.join(ALBUM_DIR, "{}.%(ext)s".format(query))
            ydl = YoutubeDL(YDL_OPTS)
            ydl.download('ytsearch:' + query)

            audiofile = eyed3.load(os.path.join(WORKING_DIR, "albums/%s/%s.mp3" % (album['name'], query)))

            if audiofile.tag is None:
                raise Exception("tag property doesn't exist WHAT")

            audiofile.tag.album = album['name']
            audiofile.tag.album_artist = audiofile.tag.artist = artists
            audiofile.tag.title = track['name']
            audiofile.tag.track_num = track['track_number']

            audiofile.tag.save()

    CONFIG = os.path.join(HOME, ".config/mpd-discord-richpresence/config.json")

    # TODO: involve XDG_CONFIG_DIR
    with open(CONFIG, "r+") as configuration:
        data = json.load(configuration)
        if not data.get("covers"): data['covers'] = {}
        data["covers"][album['name']] = { 'type': 'ALBUM', 'url': album['images'][0]['url'] }

    with open(CONFIG, "w") as configuration:
        json.dump(data, configuration)

    print("Done lmao")

