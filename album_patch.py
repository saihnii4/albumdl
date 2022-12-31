#!/usr/bin/python
# i use spotdl for downloading liked songs, this creates a mpd-rpc album art entry for them

import eyed3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import json
import sys
import os

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ['CLIENT_ID'],
                                                           client_secret=os.environ['CLIENT_SECRET']))

dir = sys.argv[1]

HOME = os.path.expanduser("~")
CONFIG = os.path.join(HOME, ".config/mpd-discord-richpresence/config.json")

with open(CONFIG, "r+") as config:
    data = json.load(config)
    if not data.get("covers"): data['covers'] = []

    try:
        for file in os.listdir(dir):
            track = eyed3.load(os.path.join(dir, file))

            if not track or not track.tag:
                continue

            song = sp.search(q="%s - %s" % (track.tag.artist, track.tag.title), limit=20, type='track')['tracks']['items'][0]['album']['uri']

            album = sp.album(song)
            
            # i hate this i hate this i hate this
            if any([cross_ref.get("value") == album['name'] for cross_ref in data['covers']]):
                continue

            data["covers"].append({ 'type': 0, 'value': album['name'], 'dest_url': album['images'][0]['url'] })

    except (KeyboardInterrupt, Exception):
        print("interesting shit happened here")
        config.close()

        with open(CONFIG, "w") as config:
            json.dump(data, config)

    config.close()

    # probably not i/o safe but who cares amirite
    with open(CONFIG, "w") as config:
        json.dump(data, config)

