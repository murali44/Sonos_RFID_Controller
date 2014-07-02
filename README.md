RFID based controller for Sonos
===============================

[ ![Codeship Status for murali44/Sonos_RFID_Controller](https://www.codeship.io/projects/a2d7e410-dde9-0131-2d72-66d7dc599325/status)](https://www.codeship.io/projects/24742)

This is an experimental project that plays music on your
Sonos speaker using RFID cards. Just scan a card and play
a radio station or playlist associated with the card.


Raspberry Pi Setup
==================

I'm using raspbian on my raspbian pi.
You'll find instructions here. http://bit.ly/1jKKAHr

Hardware Setup
==============

I used a RC522 RFID sensor with my Raspberry Pi.
You can find one for $6 of cheaper on ebay. http://bit.ly/1mUNOgl


First it is necessary to enable the peripheral.

Edit the following file:
    /etc/modprobe.d/raspi-blacklsit.conf

Add '#' in front of the line 'spi-bcm2708' and save the file.

Next reboot the Pi.
    sudo reboot

At the prompt type:
    lsmod

You should see spi_bcm2708 in the list. So far so good.

Next we have to update the Raspberry Pi in order to be able to
find the files in the following steps. Update using:
    sudo apt-get update

With that completed, install python-dev with:
    sudo apt-get install python-dev

 Next, connect your Raspberry Pi to the RC522 FRID sensor.

 ![ScreenShot](http://3.bp.blogspot.com/-93KdBuWD1g8/UdEamKhesBI/AAAAAAAADdg/AtIY45vsAgs/s715/Diagrama_Conexion.jpeg)
