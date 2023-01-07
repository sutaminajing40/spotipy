import csv
from curses.ascii import isalpha
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import spotify_id as si
import re
import pandas as pd
import os
import pykakasi


def is_japanese(str):
    return 'ja' if re.search(r'[ぁ-んァ-ン]', str) else 'en'

flag = True
#標準入力でアーティスト名を取得

art_name = input('アーティスト名を入力 >>')

print(art_name)

client_id = si.id()
client_secret = si.secret()
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager,language='ja')
df = pd.DataFrame()

for name in art_name:
    #全曲
    cnt = 0
    continuous_times = 0
    while(1):
        #print(art_name)
        tracks = sp.search(q=art_name, limit=1, offset=cnt, type='track')['tracks']['items']
        cnt +=1
        #print(tracks)
        #pprint.pprint(tracks)
        if len(tracks) == 0:
            break
        if (('原曲'or'カラオケ') in tracks[0]['name']) or continuous_times >30:
            break
        if tracks[0]['artists'][0]['name'] != name:
            continuous_times+=1
            continue
        
        continuous_times = 0
        for track in tracks:
            #print(track['id'])
            result = sp.audio_features(track['id'])
            if result[0] is None:
                continue
            pprint.pprint('曲名 ' +track['name'])
            print('アーティスト '+ tracks[0]['artists'][0]['name'])
            result[0]['name'] = track['name']
            #result[0]['id'] = track['id']
            #pprint.pprint(result)
            s = pd.DataFrame(result[0].values(),index=result[0].keys()).T
            s = s.set_index('name')
            #print(s)
            df = pd.concat([df,s])
            #print(df)
            #df = df.rename(index={'0':track['name']})
    #print(df)

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