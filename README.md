PiControl
=========

Control your headless Raspberry Pi with the AdaFruit LCD Plate
Built on latest Raspbian (2014-09-09) at time of writing readme (2014-12-16)

PiControl lets you control an internet connected Raspberry Pi (NAS optional) running Raspbian, via the Adafruit 16x2 LCD Plate. The idea was to create a simple hierarchical menu system to provide basic system functionality for a NAS Pi through the use of the LCD and Tactile buttons provided by the Adafruit i2c LCD Plate.

To Install: 
  1. Open terminal window or SSH into pi.
  2. Run the terminal command: "git clone https://github.com/korn101/PiControl"
  3. You now have a working copy of PiControl in your /home/pi/PiControl directory, but we're not done yet.
  4. Automate the running of the /home/pi/PiControl/PiControl.py script. See here: http://www.raspberrypi.org/documentation/linux/usage/rc-local.md

System Functions include:
* Idle Mode (with clock display)
* PiDiag (see crucial hardware specs ie. clock speeds, temp, memory split)
* Wifi Diag (see current Wifi network, check connectivity to router and internet)
* Halt System (perform a safe system halt/shutdown)
* Restart System (perform a safe system restart)
* Run a PiNumberStation in the background. See: https://github.com/korn101/PiNumberStation

New Updates include:
* Check connected HDD ✓
* Settings menu and configuration file support ✓
* PiNumberStation support for broadcast on user-defined frequency ✓
* Integer Dialog Support ✓
* Boolean Dialog Support ✓

Soon to be functions include:
* Run rpi-update, apt-get update, apt-get upgrade
* Backup contents of selected drive to ExtHDD
* Connect/Disconnect to and from different wifi networks (including password entry dialog and basic keyboard system)
* Live & Continuous temperature 'watching' console
* Yowsup functionality to pass commands over Whatsapp

=================

Developers Notes:

Install, Dev & Maintenance Instructions
===
Cloning the repository / Install:
  1. Open terminal and cd to home directory. ie. /home/pi/
  2. Run "git clone https://github.com/korn101/PiControl" to clone repository to the pi.
  3. Project folder is now under /home/pi/PiControl/
  4. Enter the project folder with "cd PiControl"
  5. Make changes as you wish. Then continue to next section of steps.

To commit changes:
  1. Open terminal, cd into /home/pi/PiControl
  2. Run "git add PiControl.py", "git add piconf.ini" , etc. To add to commit list.
  3. Run "git commit -m "<commit message>""
  4. Push the commit to master with: "git push master origin"
  5. Done! :)
(or use the update.sh automated script!)
