#ライブラリ読み込み
import glob
import pprint
import random
import numpy as np
import pandas as pd
import spotify_id as si
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from sklearn.cluster import KMeans
import create_playlist
import datetime
import make_excel
import tqdm

#columnsで与えられた値だけを取り出す。.locだとseries型で渡されるので扱いにくい
def get_csv_value(df,columns):
    b = df.loc[:,columns]
    c = b.iloc[-1]
    return c

#再帰的クラスタリング
def clustering(df):
    n_clusters = 2
    #必要な属性だけ抜き出す
    cust_array = np.array([df['loudness'].tolist(),
                       df['loudness'].tolist(),
                       df['mode'].tolist(),
                       df['speechiness'].tolist(),
                       df['mode'].tolist(),
                       df['speechiness'].tolist(),
                       df['acousticness'].tolist(),
                       df['instrumentalness'].tolist(),
                       df['liveness'].tolist(),
                       df['valence'].tolist(),
                       df['tempo'].tolist(),
                       df['duration_ms'].tolist(),
                       df['time_signature'].tolist()
                       ], np.int32)

    #反転
    cust_array = cust_array.T
        #attributeにクラスタリング結果
    attribute = KMeans(n_clusters=n_clusters).fit_predict(cust_array)
        #cluster_idにattributeを
    df['attribute']=attribute
        #注目している曲のクラスタリング結果をtarget_song_attributeに代入
    target_song_attribute = get_csv_value(df[df.notice == 1],'attribute')
        #注目している曲とattributeが一緒のもののみ残す
    new_df = df[df.attribute == target_song_attribute]

    new_df_cnt = new_df['id'].nunique()
    if new_df_cnt < 6:
        return new_df
        #クラスタリング
    return clustering(new_df)


    #認証
client_id = si.id()
client_secret = si.secret()
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="playlist-modify-public"),
                                               language='ja')


#データセット読み込み
csv_song_path = glob.glob("/Users/iguchihiroto/Documents/programming/spotipy/csvfile/*.csv")
target_song_data = pd.read_csv('/Users/iguchihiroto/Documents/programming/spotipy/csvfile/target_playlist_items.csv')

all_song_data = pd.DataFrame()


#csvfile内の全ての.csvのパスを取得
print('Excelファイル読み込み中...')
for path in tqdm.tqdm(csv_song_path):
    data = pd.read_csv(path)
    all_song_data = pd.concat([all_song_data,data])


#注目する曲に1をそれ以外に0を
all_song_data['notice'] = 0
target_song_data['notice'] = 1


#プレイリスト名設定
dt_now = str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
name = 'おすすめ'+dt_now

#Excelファイルに今回作成したプレイリストの名前を入力
make_excel.make_backup('evaluation.xlsx')
make_excel.write([name])


recomends = pd.DataFrame()
recomend_ids = []

print('おすすめ曲作成中...')
for index,song_data in tqdm.tqdm(target_song_data.iterrows()):
    #推薦元の曲のidを取得
    ori_song_id = song_data['id']
    #推薦元の曲のアーティスト名を取得
    ori_art_name = sp.track(ori_song_id)['artists'][0]['name']
    #推薦元の曲名を取得
    ori_song_name = song_data['name']

    #全曲データに対象の曲を1曲ずつ合体!
    current_music_data = all_song_data.append(song_data)
    #重複を削除
    current_music_data = current_music_data.drop_duplicates(subset='name',keep='last')
    #クラスタリング
    result = clustering(current_music_data)
    #注目した楽曲を削除しておすすめの曲だけにする
    recomends = pd.concat([recomends,result[result.notice == 0]])

    #ランダム値を生成 (0 <= n <= 行数-1)
    rand = random.randint(0,len(recomends)-1)
    #おすすめ結果の中からランダムで一曲抽出
    recomend = recomends[rand:rand+1]
    #おすすめされた曲名
    recomended_song_name = get_csv_value(recomend,'name')
    #おすすめされた曲のid
    recomended_song_id = get_csv_value(recomend,'id')
    #おすすめされた曲のアーティスト名
    recomended_art_name = sp.track(recomended_song_id)['artists'][0]['name']
    #idを抜き出してrecomend_idsにlistで格納
    recomend_ids.append(recomended_song_id)

    #excelに書き込む用のlistを用意
    to_excel = [ori_song_name,ori_art_name,'->',recomended_song_name,recomended_art_name,'']
    make_excel.write(to_excel)



playlist_id = create_playlist.create_playlist(name)
sp.playlist_add_items(playlist_id=playlist_id,items = recomend_ids)
