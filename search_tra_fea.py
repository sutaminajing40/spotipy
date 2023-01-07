import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import spotify_id as si

flag = True
art_name = input('アーティスト名を入力 >> ')
tra_name = input('曲名を入力 >> ')

client_id = si.id()
client_secret = si.secret()
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

art_search = sp.search(art_name,type='artist') 
#アーティスト名でsp.search
art_id = art_search['artists']['items'][0]['id'] 
#辞書型で渡されるので、その中のidを参照(同名アーティストがいたらまずい)

art_alb = sp.artist_albums(art_id, limit=50,album_type='album') 
#アーティストidでアルバムを検索

alb_ids = [alb['id'] for alb in art_alb['items']] 
#alb_idsにアルバムのIDが最大50個格納されてる

tra_id_name = []
for alb_id in alb_ids:
    tracks = sp.album_tracks(alb_id, limit=50)["items"]
    for track_num,track in enumerate(tracks):
        dict = {'name':track["name"],'id':track["id"]}
        if track["name"] == tra_name and flag:
            result = sp.audio_features(track['id'])
            pprint.pprint('name     : ' +track['name'])
            if result[0] is None:
                print('NoneTypeです')
            pprint.pprint(result[0])
            flag = False
        tra_id_name.append(dict)
#pprint.pprint(tra_id_name)