import json
import os
import re
import RPi.GPIO as GPIO
import signal
import soco
import soundcloud
import subprocess
import sys
import time
import urllib2

from random import shuffle
from ConfigParser import SafeConfigParser
import mfrc522.MFRC522 as mfrc522


continue_reading = True
MEDIA_STREAM_URL = 'http://media.soundcloud.com/stream/'


def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)

MIFAREReader = mfrc522.MFRC522()

parser = SafeConfigParser()
parser.read('config.ini')

rfid_card1 = parser.get('rfid', 'whitecard')
npr_card = parser.get('rfid', 'npr')
sc_client_id = parser.get('soundcloud', 'client_id')
sc_url = parser.get('soundcloud', 'url')

zone_name = parser.get('zone', 'zonename')
zones = list(soco.discover())
zone = soco.SoCo(zones[0].get_group_coordinator(zone_name))

while continue_reading:
    time.sleep(2)
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print "Card found."

    (status, backData) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        key_str = str(backData[0]) + str(backData[1]) + str(backData[2]) \
            + str(backData[3]) + str(backData[4])

        # Beep
        GPIO.output(7, False)
        GPIO.output(7, True)
        time.sleep(0.05)
        GPIO.output(7, False)

        if(key_str == npr_card):
            zone.play_uri('nprdmp.ic.llnwd.net/stream/nprdmp_live01_mp3')
        elif(key_str == rfid_card1):
            zone.clear_queue()
            client = soundcloud.Client(client_id=sc_client_id)
            tracks = client.get('/users/1343418/favorites', limit=5)
            shuffle(tracks)
            for track in tracks:
                regex = re.compile('\/([a-zA-Z0-9]+)_')
                r_url = regex.search(track.waveform_url)
                stream_id = r_url.groups()[0]
                media_url = MEDIA_STREAM_URL + str(stream_id)
                req = urllib2.Request(media_url)
                res = urllib2.urlopen(req)
                finalurl = res.geturl()
                item = [('InstanceID', 0),
                        ('EnqueuedURI', finalurl),
                        ('EnqueuedURIMetaData', ''),
                        ('DesiredFirstTrackNumberEnqueued', 0),
                        ('EnqueueAsNext', 1)]
                zone.avTransport.AddURIToQueue(item)
            zone.play_from_queue(0)
        else:
            # Beep. Beep. Card not recognized.
            GPIO.output(7, False)
            GPIO.output(7, True)
            time.sleep(0.02)
            GPIO.output(7, False)
            time.sleep(0.04)
            GPIO.output(7, True)
            time.sleep(0.02)
            GPIO.output(7, False)
