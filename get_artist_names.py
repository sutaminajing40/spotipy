import pprint
import requests
from bs4 import BeautifulSoup
import spotipy
import spotify_id as si
from spotipy.oauth2 import SpotifyOAuth
import tqdm


#汚いlistを作成する
def make_list(start):
    ls = []
    for i in range(7):
        ls.extend(list(range(start,start+5)))
        start+=11
    ls.extend(list(range(81,84)))
    ls.extend(list(range(90,95)))
    ls.extend(list(range(98,100)))
    ls.remove(52)
    ls.remove(92)
    return ls


# アーティスト名をリストにして渡す
def get_all_artist_names():
    db_artists=[]
    #Rakutenブックス CD J-POP アーティスト一覧
    URL = 'https://books.rakuten.co.jp/cd/artist/japanese-pop-music/#sa'
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    #find_allでタグ:td,class = etc_rankを全て取得
    etc_ranks = soup.find_all('td',class_='etc_rank')

    print('アーティスト名を取得中...')
    for i in tqdm.tqdm(make_list(6)):
        for j in etc_ranks[i].find_all('a'):
            db_artists.append(j.text)

    return db_artists

def get_current_artist_names():
    scope = 'user-read-recently-played'
    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(si.id(), si.secret())
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(si.id(),
                                               si.secret(),
                                               redirect_uri="http://localhost:8888/callback",
                                               scope=scope),
                                               language='ja')
    #pprint.pprint(sp.current_user_recently_played(limit=2)['items'][0]['track']['artists'][0]['name'])                                           
    pprint.pprint(sp.current_user_saved_tracks(limit=2))   


def get_favorite_artist_names():
    artists_names = []
    scope = 'user-library-read'
    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(si.id(), si.secret())
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(si.id(),
                                               si.secret(),
                                               redirect_uri="http://localhost:8888/callback",
                                               scope=scope),
                                               language='ja')    
                                                                                   
    artists_infomention = sp.current_user_saved_tracks(limit=50)
    #pprint.pprint(artists_infomention['items'])
    for artists_name in artists_infomention['items']:
        artists_names.append(artists_name['track']['artists'][0]['name'])
    return artists_names



print(make_list(6))