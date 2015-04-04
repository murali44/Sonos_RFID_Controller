RFID based controller for Sonos
===============================

[ ![Codeship Status for murali44/Sonos_RFID_Controller](https://www.codeship.io/projects/a2d7e410-dde9-0131-2d72-66d7dc599325/status)](https://www.codeship.io/projects/24742)

This is an experimental project that plays music on your
Sonos speaker using RFID cards. Just scan a card and play
a radio station or playlist associated with the card.


Raspberry Pi Setup
==================

I'm using raspbian on my raspberry pi.
You'll find instructions here. http://bit.ly/1jKKAHr

Hardware Setup
==============

I used a RC522 RFID sensor with my Raspberry Pi.
You can find one for $6 or cheaper on ebay. http://bit.ly/1mUNOgl


First, we need to enable the peripheral.

    Edit the following file:
       /etc/modprobe.d/raspi-blacklsit.conf

    Comment the line 'spi-bcm2708' by adding a '#' in front of it. 
    Save the file.
    
    You will also need to add “dtparam=spi=on” to your config.txt and reboot.

    Edit the following file:
        /boot/config.txt

    add…  
    dtparam=spi=on
    …at the end of the file.

    Reboot the Pi.
      Command: sudo reboot

    Check peripheral.
      Command: lsmod

    You should see 'spi_bcm2708' in the list.

    Update your Raspberry Pi.
      Command: sudo apt-get update


 Next, connect your Raspberry Pi to the RC522 RFID sensor.

 ![ScreenShot](http://3.bp.blogspot.com/-93KdBuWD1g8/UdEamKhesBI/AAAAAAAADdg/AtIY45vsAgs/s715/Diagrama_Conexion.jpeg)
