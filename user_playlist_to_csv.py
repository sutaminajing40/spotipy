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


def get_playlist_id(pl_name:str):
    pls = sp.user_playlist(user_name)
    pprint.pprint(pls)
    while(1):
        for name in pls['name']:
            if name == pl_name:
                pl_id = pls['id']
                return pl_id



if __name__ == '__main__':
    #プレイリストの名前を入力
    #pl_name = input('プレイリスト名を入力 >> ')
    #get_playlist_id in:プレイリスト名:str out:プレイリストid:str
    #pl_id = get_playlist_id(pl_name)
    
    pl_id = '37i9dQZF1EpwEQqCweow6H'
    #プレイリスト内のitemの情報をpl_itemsに
    pl_items = sp.playlist_items(pl_id,limit = 50,fields='items')
    #pl_itemsからpl_art_namesに各アイテムのartist名を、pl_item_namesに楽曲の名前をlistで
    pl_art_names = []
    pl_item_names = []
    for items in pl_items['items']:
        pl_art_names.append(items['track']['artists'][0]['name'])
        pl_item_names.append(items['track']['name'])

    #dfをDataFrame型で宣言
    df = pd.DataFrame()
    for num,art_name in enumerate(pl_art_names):
        #make_df in:アーティスト名:str,楽曲名:str out:False or Dataflame
        s = mtc.make_df(art_name,pl_item_names[num])

        if s.empty == True:
            continue
        df = pd.concat([df,s])

    mtc.make_csv('target_playlist_items',df)
