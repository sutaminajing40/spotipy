import os
import pprint

import pandas as pd
import spotify_id as si
from spotipy.oauth2 import SpotifyOAuth
import spotipy

client_id = si.id()
client_secret = si.secret()
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
target_playlist_id = '37i9dQZEVXcQxp5nXUJnTQ'
df = pd.DataFrame()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-read-recently-played"),
                                               language='ja')

#pprint.pprint(sp.playlist_items(target_playlist_id)['items'])
playlist_items = sp.playlist_items(target_playlist_id)['items']

for track in playlist_items:
    #pprint.pprint(track['track']['id'])
    result = sp.audio_features(track['track']['id'])
    #pprint.pprint(track['name'])
    result[0]['name'] = track['track']['name']
    #result[0]['id'] = track['id']
    #pprint.pprint(result)
    s = pd.DataFrame(result[0].values(),index=result[0].keys()).T
    s = s.set_index('name')
    #print(s)
    df = pd.concat([df,s])
    #print(df)
    #df = df.rename(index={'0':track['name']})

dir = os.path.dirname(__file__)
file_name = os.path.join(dir,'target_playlist_items.csv')
print(file_name)
df.to_csv(file_name,encoding='utf-8',index=True)