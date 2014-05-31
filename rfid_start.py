import signal
import time
import os
import sys
sys.path.insert(0, '/CodeBase/Sonos_RFID_Controller/SoCo')
import soco
import subprocess
import json
from random import shuffle
from ConfigParser import SafeConfigParser
from MFRC522 import MFRC522


continue_reading = True
# Capture SIGINT
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup() # Suggested by Marjan Trutschl

signal.signal(signal.SIGINT, end_read)

MIFAREReader = MFRC522.MFRC522()

parser = SafeConfigParser()
parser.read('config.ini')

rfid_card1 = parser.get('rfid', 'whitecard')
sc_client_id = parser.get('soundcloud', 'client_id')


zone_name = 'Living Room'
zones = list(soco.discover())

while continue_reading:
    time.sleep(2)
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
    if status == MIFAREReader.MI_OK:
        print "Card found."
    
    (status,backData) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        key_str = str(backData[0])+str(backData[1])+str(backData[2])+str(backData[3])+str(backData[4])
        
        # Beep
    	GPIO.output(7, False)
    	GPIO.output(7, True)
    	time.sleep(0.05)
    	GPIO.output(7, False)
        
    	if(key_str == rfid_card1):
            url = 'https://api.soundcloud.com/users/muralia/favorites.json?client_id=' + sc_client_id + '&limit=5'
            
            proc = subprocess.Popen(["curl", url], stdout=subprocess.PIPE)
            (out, err) = proc.communicate()
            track_info = json.loads(out)
            
            sc_tracks = []
            shuffle(track_info)
            
            for item in track_info:
        		if item.get('kind') != 'track':
                    continue
        		if item.get("stream_url") is not None:
                    stream_url = item.get("stream_url") + "?client_id=" + sc_client_id
                    proc = subprocess.Popen(["curl", "--head", stream_url], stdout=subprocess.PIPE)
                    (out, err) = proc.communicate()
                    for part in [s.strip().split(': ') for s in out.splitlines()]:
                        if (part[0] == 'Location'):
                            mp3url = part[1]
                            sc_tracks.append(mp3url)
            
            
            zone_name = 'Living Room'
            zones = list(soco.discover())
            living_room = soco.SoCo(zones[0].get_group_coordinator(zone_name))
            living_room.clear_queue()
            
            for track in sc_tracks:
        		item = [
                        ('InstanceID', 0),
                        ('EnqueuedURI', track),
                        ('EnqueuedURIMetaData', ''),
                        ('DesiredFirstTrackNumberEnqueued', 0),
                        ('EnqueueAsNext', 1)
                        ]
        		living_room.avTransport.AddURIToQueue(item)
            
            
            living_room.play_from_queue(0)								
    	else:
        	print "Card not recognized."