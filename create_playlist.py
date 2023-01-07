import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotify_id as si
from spotipy.oauth2 import SpotifyOAuth

def create_playlist(playlist_name):
    scope = "playlist-modify-public"
    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(si.id(), si.secret())

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=si.id(),
                                                client_secret=si.secret(),
                                                redirect_uri="http://localhost:8888/callback",
                                                scope=scope),
                                                language='ja')

    id = sp.user_playlist_create(user='nohoarito_yuzu_334129',name=playlist_name)['id']
    return id

