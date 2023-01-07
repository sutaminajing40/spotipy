import os
import pprint
import numpy as np
import pandas as pd
import spotify_id as si
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from sklearn.cluster import KMeans


#認証
client_id = si.id()
client_secret = si.secret()
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="playlist-modify-public"),
                                               language='ja')


def make_df(art_name:str,tra_name:str):
    cnt = 0
    while(1):
        #トラック名でsp.search
        tra_search = sp.search(tra_name,type='track',limit = 1,offset=cnt) 
        #pprint.pprint(tra_search)
        tra_id = tra_search['tracks']['items'][0]['id'] 
        #検索結果のidをゲット

        #検索結果のアーティスト名が入力したアーティスト名だったら次に進む
        if tra_search['tracks']['items'][0]['artists'][0]['name'] == art_name:
            break
        cnt +=1


    result = sp.audio_features(tra_id)

    s = pd.DataFrame()
    #audio_featuresの中身がNone型だった時Falseを返す
    if result[0] is None:
        print('None型です。')
        return s
    pprint.pprint('曲名 ' +tra_search['tracks']['items'][0]['name'] )
    print('アーティスト '+ tra_search['tracks']['items'][0]['artists'][0]['name'])

    #dataframe作成
    result[0]['name'] = tra_search['tracks']['items'][0]['name']
    s = pd.DataFrame(result[0].values(),index=result[0].keys()).T
    s = s.set_index('name')
    #dataframeを返す
    return s


def make_csv(file_name:str,df):
    df = df.drop_duplicates()
    file_name = os.path.join('/Users/iguchihiroto/Documents/programming/spotipy/csvfile',file_name+'.csv')
    df.to_csv(file_name,encoding='utf-8',index=True)
    return 

if __name__ == '__main__':
    continuous_times = 0
    flag = True
    #データフレーム宣言
    df = pd.DataFrame()
    cnt = 0

    while(1):
        art_name = input('アーティスト名を入力 >> ')
        tra_name = input('曲名を入力 >> ')
        
        s = make_df(art_name,tra_name)
        if s.empty == True:
            continue
        df = pd.concat([df,s])


        continuous_times +=1
        if input('続けますかy/n >>') == 'n' or continuous_times == 50:
            break

    make_csv('target_playlist_items',df)