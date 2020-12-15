from os import listdir
from os.path import isfile, join
import json

path = './music'

song_list = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.wav')]

print(song_list)

with open('song_list.json', 'w') as file:
    json.dump({"song": song_list}, file)
