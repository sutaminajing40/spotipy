import pprint
import spotipy
import spotify_id as si
from spotipy.oauth2 import SpotifyOAuth

artists_names = []
scope = 'user-library-read'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(si.id(), si.secret())
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(si.id(),
                                            si.secret(),
                                            redirect_uri="http://localhost:8888/callback",
                                            scope=scope),
                                            language='ja')                                        
"""artists_infomention = sp.current_user_saved_tracks(limit=1)
#pprint.pprint(artists_infomention['items'])
for artists_name in artists_infomention['items']:
    artists_names.append(artists_name['track']['artists'][0]['name'])"""
pprint.pprint(sp.current_user_saved_tracks())