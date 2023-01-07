# -*- coding: utf-8 -*-

import csv
from curses.ascii import isalpha
import pykakasi
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotify_id as si
import re
import pandas as pd
import os
import get_artist_names as gan
import tqdm
import get_vcp_names as gvn

#日本語か判定
def is_japanese(str):
    return 'ja' if re.search(r'[ぁ-んァ-ン]', str) else 'en'

flag = True

switch = input('ボカロ:1、日本人アーティスト:2 >> ')
if switch == '1':
    art_names = gvn.main()
elif switch == '2':
    art_names = gan.get_all_artist_names()

#lang = is_japanese(art_names)

#認証
client_id = si.id()
client_secret = si.secret()
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager,language='ja')

#データフレーム宣言
df = pd.DataFrame()

print('楽曲情報取得中...')
for art_name in tqdm.tqdm(art_names):
    #全曲
    #offsetずらす用のcnt
    cnt = 0
    #連続で見つからない回数
    continuous_times = 0
    df = pd.DataFrame()
    ids = []
    names = []
    art_names = []

    #offsetの上限1000を超えないように
    while(cnt < 20):
        tracks = sp.search(q=art_name, limit=50, offset=cnt*50, type='track')['tracks']['items']
        cnt +=1
        #検索結果がなくなったらbreak
        if len(tracks) == 0 or continuous_times > 100:
            break

        for track in tracks:
            if track is None:
                continue
            if track['artists'][0]['name'] == art_name:
                continuous_times = 0
                ids.append(track['id'])
                names.append(track['name'])
                art_names.append(track['artists'][0]['name'])
            else:
                continuous_times +=1
        
    for i in range(0, len(ids), 100):
        results = sp.audio_features(ids[i:i+100])
        for j,result in enumerate(results):
            if result is None:
                continue
            result['name'] = names[i+j]
            s = pd.DataFrame(result.values(),index=result.keys()).T
            s = s.set_index('name')
            df = pd.concat([df,s])

    name = ''
    if len(df) != 0:
        kks = pykakasi.kakasi() # インスタンスの作成

        result = kks.convert(str(art_name))
        for kanji in result:
            name = name + kanji['passport']
            #ファイル名に使えないものを'-'に変換
            name = re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '-', name)
            
        name = str(name) + '.csv'
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