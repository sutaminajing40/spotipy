from curses.ascii import isalpha
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import spotify_id as si
import re

def is_japanese(str):
    return 'ja' if re.search(r'[ぁ-んァ-ン]', str) else 'en'

flag = True
cnt = 0
print('アーティスト名を入力')
art_name = input()
print('曲名を入力')
tra_name = input()
lang = is_japanese(art_name)

client_id = si.id()
client_secret = si.secret()
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager,language=lang)

while flag:
    tracks = sp.search(tra_name,type='track',offset=cnt*10)['tracks']['items']
    #print(type(tracks[0]['artists']))
    tra_id_name=[]
    for track in tracks:
        #print(track['artists'][0]['name'])
        dict = {'name':track["name"],'artist':track['artists'][0]['name'],'id':track["id"]}
        if art_name in track['artists'][0]['name'] and flag:
            result = sp.audio_features(track['id'])
            pprint.pprint('name   : ' +track['name'])
            pprint.pprint('artist : ' +track['artists'][0]['name'])
            pprint.pprint(result)
            flag = False
        tra_id_name.append(dict)
    cnt += 1

"""tra_names = []
f = open('name_data.txt','w')
for i in range(10):
    tra_names = []
    tracks = sp.search(tra_name,type='track',offset=i*10)['tracks']['items']
    for track in tracks:
        dict = {'name':track["name"]}
        tra_names.append(dict)
    
    for name in tra_names:
        #f.write("%s\n" % tra_names)
        print(name,file=f,)
    print(1,file=f)"""

"""
f = open('name_data.txt','w')
for name in tra_names:
    #f.write("%s\n" % tra_names)
    print(name,file=f)"""