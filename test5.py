import glob
import os

file_names = glob.glob('/Users/iguchihiroto/Documents/programming/spotipy/csvfile/*')

for file_name in file_names:
    os.remove(file_name)