#!/usr/bin/python3

import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def parse_object(obj): 
    artists = map(lambda a: a['name'], obj.get("artists")) if obj.get("artists") else ["N/A"]

    return '%s - %s (%s) [%s]' % (obj['name'], ", ".join(artists), obj['type'].upper(), obj['uri'])

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ['CLIENT_ID'],
                                                           client_secret=os.environ['CLIENT_SECRET']))

results = sp.search(q=" ".join(sys.argv[1:]), limit=20, type='track')
for item in results['tracks']['items']:
    print("\"%s\"" % parse_object(item), end=' ')
