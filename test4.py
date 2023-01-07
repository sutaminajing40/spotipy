import csv
from curses.ascii import isalpha
import pykakasi
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import spotify_id as si
import re
import pandas as pd
import os
import get_artist_names as gan

#認証
client_id = si.id()
client_secret = si.secret()
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager,language='ja')

result = sp.search('ポルノグラフィティ',limit=2,type='track')['tracks']['items']

ids = []
for id in result:
    ids.append(id['id'])

pprint.pprint(sp.audio_features(ids))