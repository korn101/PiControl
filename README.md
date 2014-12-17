PiControl
=========

Control your headless Raspberry Pi with the AdaFruit LCD Plate
Built on latest Raspbian (2014-09-09) at time of writing readme (2014-12-16)

PiControl lets you control an internet connected Raspberry Pi (NAS optional) running Raspbian, via the Adafruit 16x2 LCD Plate. The idea was to create a simple hierarchical menu system to provide basic system functionality for a NAS Pi through the use of the LCD and Tactile buttons provided by the Adafruit i2c LCD Plate.

System Functions include:
  
    -Idle Mode (with clock display)
  
    -PiDiag (see crucial hardware specs ie. clock speeds, temp, memory split)
  
    -Wifi Diag (see current Wifi network, check connectivity to router and internet)
  
    -Halt System (perform a safe system halt/shutdown)
  
    -Restart System (perform a safe system restart)
  
Soon to be functions include:
    -Options dialogs for menu options

    -Run rpi-update, apt-get update, apt-get upgrade

    -Check connected HDD

    -Backup contents of selected drive to ExtHDD

    -Connect/Disconnect to and from different wifi networks (including password entry dialog and basic keyboard system)
    
    - Live & Continuous temperature 'watching' console

To install, run:
    
    git clone https://github.com/korn101/PiControl/

And automate network_check.py to run at boot, using either rc.local or equivalent.
