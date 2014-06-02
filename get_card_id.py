import RPi.GPIO as GPIO
import signal
import time
import sys
import subprocess
import mfrc522.MFRC522 as mfrc522

continue_reading = True
# Capture SIGINT
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup() # Suggested by Marjan Trutschl

signal.signal(signal.SIGINT, end_read)

MIFAREReader = mfrc522.MFRC522()

while continue_reading:
    time.sleep(1)
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
    if status == MIFAREReader.MI_OK:
        print "Card found."
    
    (status,backData) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        key_str = str(backData[0])+str(backData[1])+str(backData[2])+str(backData[3])+str(backData[4])
        print key_str

        # Beep
    	GPIO.output(7, False)
    	GPIO.output(7, True)
    	time.sleep(0.05)
    	GPIO.output(7, False)
        
