import threading as th
import asyncio
import time
import vlc

media_player = vlc.MediaPlayer()


def get_file_list():
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
            
    with open("/home/pi/whisper/config/data.json", 'w', encoding='utf-8') as json_file:
        json.dump(dict_files, json_file, indent="\t")    
        
    return dict_files
    
def mp3_player(name, state):
    
    path = "/home/pi/whisper/mp3/" + name
    global media_player
    media = vlc.Media(path) 

    # setting media to the media player 
    media_player.set_media(media) 

    # start playing video 
    media_player.play() 
    

def nfc_reader_I2C():
    import board
    import busio
    from digitalio import DigitalInOut
    from adafruit_pn532.i2c import PN532_I2C
    
    temp = list()

    i2c = busio.I2C(board.SCL, board.SDA)
    #board.D1, board.D0
    #reset_pin = DigitalInOut(board.D6)
    #req_pin = DigitalInOut(board.D12)
    
    #pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)
    pn532 = PN532_I2C(i2c, debug=False)
    pn532.SAM_configuration()
    
    print("Start NFC Reader!!")
    
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)

        # Try again if no card is available.
        if uid is None:
            temp.clear()
            continue
        
        list_id = [hex(i) for i in uid]
        
        if temp.count(list_id[0]) == 0:
            temp.append(list_id[0])
        #print("Found card with UID : ", list_id)
        print(temp)
            
        #time.sleep(0.2)
        
async def nfc_reader_spi():
    import board
    import busio
    from digitalio import DigitalInOut
    from adafruit_pn532.spi import PN532_SPI
    
    temp = list()
    
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs_pin = DigitalInOut(board.D24)
    pn532 = PN532_SPI(spi, cs_pin, debug=False)

    pn532.SAM_configuration()
    
    print("Start NFC Reader!!")
    
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)

        # Try again if no card is available.
        if uid is None:
            temp.clear()
            continue
        
        list_id = [hex(i) for i in uid]
        
        if temp.count(list_id[0]) == 0:
            temp.append(list_id[0])
        #print("Found card with UID : ", list_id)
        print(temp)
            
        time.sleep(0.2)

async def seri_lolin():
    import serial
    
    port="/dev/serial0"
    seri = serial.Serial(port, 115200)
    print(seri.portstr)

    while True:
        msg = seri.readline().decode()
        print(str(msg))
        time.sleep(0.2)

    
if __name__ == "__main__":

    nfc_thread=th.Thread(target=nfc_reader_I2C, args=())
    nfc_thread.start()
    
    temp = get_file_list()
    
    #print(dir(nfc_thread))
    #asyncio.run(nfc_reader())
    
    name = "cheerup.mp3"
    state = "start"
    
    mp3_thread=th.Thread(target=mp3_player, args=(name, state))
    mp3_thread.start()
    
    #asyncio.run(mp3_player(name, state))
    
    #seri_thread=Thread(target=seri_lolin, args=())
    #seri_thread.start()
    while(1):
        for i in range(100):
            print(i)
            time.sleep(1)
    