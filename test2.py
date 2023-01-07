import os
import pprint
import numpy as np
import pandas as pd
import spotify_id as si
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import make_target_csv as mtc

#認証
client_id = si.id()
client_secret = si.secret()
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
user_name = si.user_name()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="playlist-modify-public"),
                                               language='ja')

rst = sp.user_playlist(user_name,playlist_id='6uhEvsVewoYIdiKp5EMA7X')
pprint.pprint(rst)