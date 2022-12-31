#!/usr/bin/python

import eyed3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import sys
import os

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ['CLIENT_ID'],
                                                           client_secret=os.environ['CLIENT_SECRET']))

for file in [*filter(lambda x: os.path.isfile(x) and os.path.splitext(x)[-1] in (".mp3", ".wav", ".ogg"), os.listdir(os.getcwd()))]:
    track = eyed3.load(os.path.join)

    print(track)

