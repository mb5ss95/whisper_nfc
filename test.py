import pyrebase
import json

with open("/home/pi/whisper/config/config.json") as json_file:
    json_data = json.load(json_file)

firebase_storage = pyrebase.initialize_app(json_data)
storage = firebase_storage.storage()

all_files = storage.list_files()

dict_files = dict()

for file in all_files:
    name = file.name  
    temp = name.split("/")
    
    if temp[0] in dict_files:
        dict_files[temp[0]].append(temp[1])
    else:
        dict_files.setdefault(temp[0], list())
        
print(dict_files)
#storage.child("please.mp3").put("/home/pi/whisper/mp3/cheerup.mp3")
#storage.child("story1/song1.mp3").download("/home/pi/whisper/mp3/test.mp3")  