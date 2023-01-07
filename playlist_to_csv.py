# -*- coding: utf-8 -*-

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

#日本語か判定
def is_japanese(str):
    return 'ja' if re.search(r'[ぁ-んァ-ン]', str) else 'en'

flag = True

#プレイリストからアーティスト名を取得
art_names = gan.get_favorite_artist_names()
print(art_names)
#lang = is_japanese(art_names)

#認証
client_id = si.id()
client_secret = si.secret()
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager,language='ja')

#データフレーム宣言
df = pd.DataFrame()


for art_name in art_names:
    #全曲
    #offsetずらす用のcnt
    cnt = 0
    #連続で見つからない回数
    continuous_times = 0
    df = pd.DataFrame()

    while(cnt < 1000):

        tracks = sp.search(q=art_name, limit=1, offset=cnt, type='track')['tracks']['items']
        cnt +=1
        if len(tracks) == 0:
            break
        if (('原曲'or'カラオケ') in tracks[0]['name']) or continuous_times >50:
            break
        if tracks[0]['artists'][0]['name'] != art_name:
            continuous_times+=1
            continue
        
        continuous_times = 0
        for track in tracks:
            result = sp.audio_features(track['id'])
            if result[0] is None:
                continue
            pprint.pprint('曲名 ' +track['name'])
            print('アーティスト '+ tracks[0]['artists'][0]['name'])
            result[0]['name'] = track['name']
            s = pd.DataFrame(result[0].values(),index=result[0].keys()).T
            s = s.set_index('name')
            df = pd.concat([df,s])

    name = ''
    if len(df) != 0:
        kks = pykakasi.kakasi() # インスタンスの作成

        result = kks.convert(str(art_name))
        for kanji in result:
            name = name + kanji['passport']
            
        name = str(name) + '.csv'
        print(name)
        df = df.drop_duplicates()
        dir = os.path.dirname(__file__)
        file_name = os.path.join('/Users/iguchihiroto/Documents/programming/spotipy/csvfile',name)
        df.to_csv(file_name,encoding='utf-8',index=True)

"""
#x曲限定
#tracks = sp.search(q=art_name, limit=50, offset=cnt, type='track', market=None)['tracks']['items']
#pprint.pprint(tracks)


for track in tracks:
    #print(track['id'])
    result = sp.audio_features(track['id'])
    pprint.pprint(track['name'])
    result[0]['name'] = track['name']
    #result[0]['id'] = track['id']
    #pprint.pprint(result)
    s = pd.DataFrame(result[0].values(),index=result[0].keys()).T
    s = s.set_index('name')
    #print(s)
    df = pd.concat([df,s])
    #print(df)
    #df = df.rename(index={'0':track['name']})
#print(df)"""

"""df = df.drop_duplicates()
dir = os.path.dirname(__file__)
file_name = os.path.join('/Users/iguchihiroto/Documents/programming/spotipy/csvfile','test.csv')
df.to_csv(file_name,encoding='utf-8',index=True)"""