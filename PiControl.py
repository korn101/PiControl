#!/usr/bin/python
# Example using a character LCD plate.
# KT VENT

#SLOOSH

import math
import time
import socket
import Adafruit_CharLCD as LCD
import fcntl
import struct
import os
import subprocess
import re

from configobj import ConfigObj

# Initialize the LCD using the pins 
lcd = LCD.Adafruit_CharLCDPlate()

# first menu screen by default
global menuCurr
global menuSelect
global diagSelect
global lcd_columns
lcd_columns = 16
menuSelect = 0
menuCurr = 0
diagSelect = 0

# create some custom characters
lcd.create_char(1, [0,27,14,4,14,27,0, 0]) #cross X
lcd.create_char(2, [0, 1, 3, 22, 28, 8, 0, 0]) #tick
lcd.create_char(3, [0, 14, 21, 23, 17, 14, 0, 0]) #clock
lcd.create_char(4, [0,10,31,31,14,4,0, 0]) #heart
lcd.create_char(5, [8, 12, 10, 9, 10, 12, 8, 0]) #right arrow
lcd.create_char(6, [2, 6, 10, 18, 10, 6, 2, 0]) # left arrow
#lcd.create_char(7, [31, 17, 21, 21, 21, 21, 17, 31]) #domino?
lcd.create_char(7, [31,31,31,31,31,31,31,0]) #square

# TIME TILL BACKLIGHT OFF
MENU_BLANK_TIME = 20
CLOCK_BLANK_TIME = 120

#config:


menuList=["Idle mode","WiFi Diag", "Pi Diag", "Halt", "Reboot", "Display OFF", "Settings", "About", "PiNumberStation", "Stop PiNS"]
menuDesc=["Show Clock&Date", "Connection Info", "Temp/Mem/Clock", "Shutdown System", "Reboot System", "Turn off display", "Change Options", ".. PiControl", "tvoya tsel zdes", "PiNumberStation"]
piDiagList=["Temp", "Memory Split", "Clocks"]
wifiDiagList=["SSID Info", "IP Info", "Test Con."]
wifiDiagDesc=["Show wifi SSID", "List interfaces", "Router&Web access"]


def findThisProcess( process_name ):
  ps     = subprocess.Popen("ps -eaf | grep "+process_name, shell=True, stdout=subprocess.PIPE)
  output = ps.stdout.read()
  ps.stdout.close()
  ps.wait()

  return output

# This is the function you can use  
def isThisRunning( process_name ):
  output = findThisProcess( process_name )

  if re.search('path/of/process'+process_name, output) is None:
    return False
  else:
    return True

# Restart Function: Reboots Pi
def reboot():

	lcd.clear()
	lcd.message("System Reboot in\n5 Seconds..")

	time.sleep(5)
	lcd.set_backlight(0)
	lcd.enable_display(False)
	command = "/usr/bin/sudo /sbin/shutdown -r now"
	import subprocess
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	
# Shutsdown pi
def halt():

	lcd.clear()
	lcd.message("System Halt in\n5 Seconds..")

	time.sleep(5)
	lcd.set_backlight(0)
	lcd.enable_display(False)
	command = "/usr/bin/sudo /sbin/halt"
	import subprocess
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]

def get_ssid():
	from subprocess import check_output
	ssid = "NONE"
	ssid = check_output(["iwgetid", "-r"])
	return ssid

def get_temp():
	from subprocess import check_output
	#vc gen cmd causes issues. Try not to use it in future.
	#temp = check_output(["vcgencmd", "measure_temp"])
	temp = int(check_output(["cat", "/sys/class/thermal/thermal_zone0/temp"])) / 1000
	
	return temp
	
def get_curclock():
	from subprocess import check_output
	cur = int(check_output(["cat", "/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"]))
	return str(cur/100000) + "MHz"

def get_maxclock():
	from subprocess import check_output
	max = int(check_output(["cat", "/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"]))
	return str(max/100000) + "MHz"
	
def get_memARM():
	from subprocess import check_output
	mem = check_output(["vcgencmd", "get_mem arm"])
	return mem
	
def get_memGPU():
	from subprocess import check_output
	mem = check_output(["vcgencmd", "get_mem gpu"])
	return mem

def is_connected(REMOTE_SERVER):
	try:
		host = socket.gethostbyname(REMOTE_SERVER)
		s = socket.create_connection((host, 80), 2)
		return True
	except:
		pass
	return False
	
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


# Make list of button value
buttons = [LCD.SELECT, LCD.LEFT, LCD.UP, LCD.DOWN, LCD.RIGHT]

def check_connectivity():
	response2 = False
	response1 = check_router()
	
	if response1 == True:
		response2 = check_google()
	
	lcd.clear()
	lcd.message("Connectivity: \n")
	
	if response1==True and response2==True:
		lcd.message("Full web access")
	if response1==True and response2 ==False:
		lcd.message("No web access")
	if response1==False:
		lcd.message("No router")
		
	time.sleep(2)
	lcd.clear()
	return

def check_router():
	response = False
	lcd.clear()
	lcd.message('Checking Router..\n')
    
	if is_connected('10.0.0.2') == True:
		lcd.message('->ROUTER OK \2')
		response = True
	else:
		lcd.message('->ROUTER FAIL \1')
		response = False
		
	time.sleep(1)
	
	lcd.clear()
	return response
	
	
def check_google():
	response = False
	lcd.clear()
	lcd.message('Checking Google..\n')

	if is_connected('www.google.com') == True:
		lcd.message('->GOOGLE OK \2')
		response = True
	else:
		lcd.message('->GOOGLE FAIL \1')
		response = False
	
	time.sleep(1)
	lcd.clear()
	
	return response


def update_wifi_menu( param ):
	lcd.clear()
	lcd.message("[1][" + str(param) + "]-")
	lcd.message(str(wifiDiagList[param]) + "\n")
	lcd.message(str(wifiDiagDesc[param]))
	lcd.show_cursor(True)
	lcd.set_cursor(4,0)
	
	time.sleep(0.1)
	
			
def wifi_diag():

	diagSelect = 0
	update_wifi_menu(diagSelect)
	
	while True:
		
		if lcd.is_pressed(LCD.RIGHT):
			#if diagSelect == len(wifiDiagList) - 1:
			#	return
			if diagSelect < len(wifiDiagList) - 1:
				diagSelect = diagSelect + 1
				time.sleep(0.1)
			update_wifi_menu(diagSelect)
			
		if lcd.is_pressed(LCD.LEFT):
			if diagSelect == 0:
				return
			if diagSelect > 0:
				diagSelect = diagSelect - 1
				time.sleep(0.1)
			update_wifi_menu(diagSelect)
			
		if lcd.is_pressed(LCD.SELECT):
			if diagSelect == 0:
				display_ssid()
			if diagSelect == 1:
				display_ip()
			if diagSelect == 2:
				check_connectivity()
				
			update_wifi_menu( diagSelect )
				
def prompt( text ):

	lcd.clear()
	lcd.autoscroll(False)
	lcd.set_cursor(0,0)
	lcd.blink(False)
	
	i = 0
	while (i < len(text)):
		if i == 16 or i == 48 or i == 80 or i == 112:
			lcd.message("\n")
			
		if i == 32 or i == 64 or i == 96 or i == 128:
			lcd.blink(True)
			time.sleep(1)
			lcd.clear()
			lcd.blink(False)
			lcd.home()
		if i < len(text):
			lcd.message(text[i])
		else:
			lcd.message(" ")
		i = i + 1
		time.sleep(0.05)
		
	
	lcd.autoscroll(False)
	lcd.home()
	time.sleep(1)
	lcd.clear()
	lcd.blink(True)
				
def about_diag():

	#prompt("This software is distributed under the MIT license. Please read the readme on github.")

	msg = ['P','i','C','o','n','t','r','o','l']

	lcd.clear()
	#lcd.autoscroll(True)
	k = 0
	i = 0
	while (k<2):
		while (i < 17):
			lcd.set_cursor(i,k)
			lcd.message("\7")
			i=i+1
		k=k+1
		i=0
		
	while (k>=0):
		while (i < 17):
			if i > 5 and k==0:
				lcd.message(msg[i-15])
			else:
				lcd.message(" ")
			lcd.set_cursor(i-1,k)
			i=i+1
		k=k-1
		i=0
	'''
	i = 14
	while i < 16:
		lcd.set_cursor(i,0)
		lcd.message(" ")
		time.sleep(0.1)
		i=i+1 '''
		
		
	lcd.clear()
	lcd.message("    PiControl    \n  Jaime Fouche  ")
	warning(1)
	lcd.show_cursor(False)
	lcd.blink(False)
	time.sleep(1)
	lcd.clear()
	lcd.message("   Written in \n     Python ")
	time.sleep(0.5)
	lcd.message("\2")
	time.sleep(0.5)
	lcd.clear()
	
def pi_diag():

	diagSelect = 0
	update_diag_menu(diagSelect)

	while True:
		
		if lcd.is_pressed(LCD.RIGHT):
			if diagSelect < len(piDiagList) - 1:
				diagSelect = diagSelect + 1
				time.sleep(0.1)
			update_diag_menu(diagSelect)
			
		if lcd.is_pressed(LCD.LEFT):
			if diagSelect == 0:
				return
			if diagSelect > 0:
				diagSelect = diagSelect - 1
				time.sleep(0.1)
			update_diag_menu(diagSelect)
			
			
			
def setting_diag():
	lcd.clear()
	#lcd.message(str(booleanDialog("Show splash?")))
	
	#open config
	import configobj
	
	confwrite = configobj.ConfigObj()
	confwrite.filename = "piconf.ini"
	
	splash = str(booleanDialog("Show Splash ?"))
	load_men = str(booleanDialog("Boot to menu ?"))
	if load_men == "True":
		def_men = integerDialog("Default menu ?", 0, len(menuList) - 1)
	else:
		def_men = 0
	
	confwrite["show_splash"] = splash
	confwrite["load_default_menu"] = load_men
	confwrite["default_menu"] = def_men
	
	confwrite.write()
	lcd.message("Done \2")
	time.sleep(1)
	
	return
			
def anythingPressed():

	if lcd.is_pressed(LCD.RIGHT) or lcd.is_pressed(LCD.LEFT) or lcd.is_pressed(LCD.UP) or lcd.is_pressed(LCD.DOWN) or lcd.is_pressed(LCD.SELECT):
		return True
	else:
		return False
			
def idleMode():

	el_start = time.time()

	lcd.clear()
	lcd.message("To exit clock..\nPress Left")
	time.sleep(1)
	lcd.clear()
	
	lcd.message("      " + time.strftime("%H:%M") + "     \n")
	lcd.message("   " + time.strftime("%Y/%m/%d") + "   ")
	
	while True:
		if lcd.is_pressed(LCD.RIGHT) or lcd.is_pressed(LCD.UP) or lcd.is_pressed(LCD.DOWN) or lcd.is_pressed(LCD.SELECT):
			lcd.set_backlight(1)
			el_start = time.time()
			
		if lcd.is_pressed(LCD.LEFT):
			return
		
		else:
			# get time:
			disp = "      " + time.strftime("%H:%M") + "     \n" + "   " + time.strftime("%Y/%m/%d") + "   "
			time.sleep(0.1)
			disp2 = "      " + time.strftime("%H:%M") + "     \n" + "   " + time.strftime("%Y/%m/%d") + "   "
			if (disp2 != disp):
				lcd.clear()
				lcd.message("      " + time.strftime("%H:%M") + "     \n")
				lcd.message("   " + time.strftime("%Y/%m/%d") + "   ")
				
				
		el_time = time.time() - el_start
		if el_time >= CLOCK_BLANK_TIME:
			lcd.set_backlight(0)
		else:
			lcd.set_backlight(1)
				
	
def update_menu( param ):
	lcd.clear()
	lcd.message("[" + str(param) + "] - ")
	message = str(menuList[param]) + "\n" + str(menuDesc[param])
	lcd.message(message)
	lcd.show_cursor(True)
	lcd.set_cursor(1,0)
	
def update_diag_menu( param ):
	lcd.clear()
	lcd.message("[2][" + str(param) + "]-")
	lcd.message(str(piDiagList[param]) + "\n")
	time.sleep(0.1)
	
	#lcd.blink(False)
	
	if param == 0:
		lcd.message("CPU0: " + str(get_temp())  + " degC")
	if param == 1:
		lcd.clear
		lcd.message(get_memGPU())
	if param == 2:
		lcd.message("\nCur:" + get_curclock() + " Max:" + get_maxclock())
		
	time.sleep(0.1)
		
	#lcd.blink(True)
	
def booleanDialog( strPrompt ):
	lcd.clear()
	if len(strPrompt) < 17:
		lcd.message( str(strPrompt) )
	else:
		prompt( strPrompt )
	
	lcd.set_cursor(0,1)
	lcd.message( "Option: " )
	
	lcd.set_cursor(14,1)
	boolVal = True
	lcd.message( "Y" )
	#lcd.set_cursor(14,1)
	while lcd.is_pressed(LCD.SELECT) == False:
		# loop checking keys and flipping Y/N
		if lcd.is_pressed(LCD.UP):
			boolVal = True
			lcd.set_cursor(14,1)
			lcd.message("Y")
		if lcd.is_pressed(LCD.DOWN):
			boolVal = False
			lcd.set_cursor(14,1)
			lcd.message("N")
			
		time.sleep(0.1)
	
		
	lcd.set_cursor(0,0)
	lcd.clear()
	return boolVal
	
def integerDialog( strPrompt , rangeLow, rangeHigh):
	lcd.clear()
	if len(strPrompt) < 17:
		lcd.message( str(strPrompt) )
	else:
		prompt( strPrompt )
	
	lcd.set_cursor(0,1)
	lcd.message( "Option: " )
	
	lcd.set_cursor(14,1)
	intVal = rangeLow
	lcd.message( str(intVal) )
	#lcd.set_cursor(14,1)
	while lcd.is_pressed(LCD.SELECT) == False:
		# loop checking keys and flipping Y/N
		if lcd.is_pressed(LCD.UP):
			if intVal < rangeHigh:
				intVal+=1
			lcd.set_cursor(14,1)
			lcd.message(str(intVal))
		if lcd.is_pressed(LCD.DOWN):
			if intVal > rangeLow:
				intVal-=1
			lcd.set_cursor(14,1)
			lcd.message(str(intVal))
			
		time.sleep(0.1)
	
		
	lcd.set_cursor(0,0)
	lcd.clear()
	return intVal
	
def backlightOff():
	lcd.clear()
	lcd.enable_display(False)
	lcd.set_backlight(0)
	time.sleep(1)
	while True:
		if lcd.is_pressed(LCD.UP):
			lcd.enable_display(True)
			lcd.set_backlight(1)
			return
		if lcd.is_pressed(LCD.DOWN):
			lcd.enable_display(True)
			lcd.set_backlight(1)
			return
		if lcd.is_pressed(LCD.RIGHT):
			lcd.enable_display(True)
			lcd.set_backlight(1)
			return
			
		if lcd.is_pressed(LCD.LEFT):
			lcd.enable_display(True)
			lcd.set_backlight(1)
			return
			
		if lcd.is_pressed(LCD.SELECT):
			lcd.enable_display(True)
			lcd.set_backlight(1)
			return

def pins():

	#strBroadcast = "103.3"
	strBroadcast = str(integerDialog("hundreds", 0, 2))
	strBroadcast += str(integerDialog(strBroadcast[0] + "x", 0, 9))
	strBroadcast += str(integerDialog(strBroadcast[0] + strBroadcast[1] + "x", 0, 9))
	strBroadcast += "."
	strBroadcast += str(integerDialog(strBroadcast[0] + strBroadcast[1] + strBroadcast[2] + ".x",0,9))
	
	subprocess.Popen(["sudo","python", "/home/pi/PiNumberStation/PiNS.py", strBroadcast, "&"])

	prompt("PiNumberStation begun on frequency " + strBroadcast)
	time.sleep(1)

	return

def exit_pins():

	subprocess.call(["sudo", "killall", "pifm"])
	
	subprocess.call(["sudo", "pkill", "-9", "-f", "PiNS.py"])

	import RPi.GPIO as GPIO
	GPIO.setup(4, GPIO.OUT)
	GPIO.output(4, GPIO.LOW)

	return
	
	
def menu_exec( param ):

	lcd.blink(False)

	if param == 0:
		idleMode()
		
	if param == 1:
		wifi_diag()
	if param == 2:
		pi_diag()
	if param == 3:
		halt()
	if param == 4:
		reboot()
	if param == 5:
		backlightOff()	
	if param == 6:
		setting_diag()
	if param == 7:
		about_diag()
	if param == 8:
		pins()
	if param == 9:
		exit_pins()
		
	update_menu(menuSelect)
	
	lcd.blink(True)
	
def display_ip():

	lcd.clear()

	interfaces = ['wlan0','eth0','lo']

	for intf in interfaces:
		try:
			lcd.message(intf + ":\n " + get_ip_address(intf))
		except:
			lcd.message(intf + ":\n disconnected")
			
		time.sleep(1)
		lcd.clear()
	
	return
	
def display_ssid():
	lcd.clear()
	lcd.message("Checking Wifi..")
	ssid = get_ssid()
	lcd.message("\nDone \2")
	time.sleep(0.1)
	lcd.clear()

	if ssid != "NONE":
		lcd.message("Connected to:\n")
		lcd.message(str(ssid))
	else:
		lcd.message("SSID missing\n")
		
	time.sleep(3)
	return

def createConfig():
	import configobj
		
	confwrite = configobj.ConfigObj()
	confwrite.filename = "piconf.ini"
		
	splash = "True"
	load_men = "False"
	def_men = 0
		
	confwrite["show_splash"] = splash
	confwrite["load_default_menu"] = load_men
	confwrite["default_menu"] = def_men
		
	confwrite.write()
	
def warning( flashes ):
	tdelay = 0.1
	
	i = 0
	
	while (i < flashes):
		lcd.set_backlight(0)
		time.sleep(tdelay)
		lcd.set_backlight(1)
		time.sleep(tdelay)
		i = i + 1
# START:

try:
	from subprocess import check_output 

	lines = (check_output(["df", "-h", "/dev/sda1"])).splitlines()
	#fields = lines[1].split('  ')
	#prompt(str(fields[0] + ": \n" + (fields[6].split(' '))[0]))
	lcd.clear()
	lcd.message("External HDD:\nMounted \2")
	time.sleep(0.5)
except:
	lcd.clear()
	lcd.message("External HDD:\nNot mounted \1")
	warning(1)
	time.sleep(1)

lcd.show_cursor(True)
lcd.blink(True)

lcd.clear()
# load config file: default menu, splash?
lcd.message("Loading Config..\n")

try:
	config = ConfigObj("piconf.ini")

	splash = config["show_splash"]
	default_menu_enabled = config["load_default_menu"]
	default_menu = config["default_menu"]
	
	lcd.message("SUCCESS \2")
	time.sleep(0.5)
	
except:
	lcd.message("FAILED \1")
	warning(1)
	time.sleep(1)
	splash = True
	default_menu_enabled = False

	prompt("A config file was not found, or has become corrupted.")
	
	if booleanDialog("Use default config?") == True:
		createConfig()
	
lcd.clear()

if splash == "True":
	lcd.clear()
	about_diag()
	lcd.clear()





lcd.message('Select Menu Item\n with UP/DOWN')
time.sleep(1)
lcd.clear()
update_menu(0)

# Main Loop

if default_menu_enabled == "True":
	menu_exec(int(default_menu))

start_time = time.time()
	
while True:
	

	if lcd.is_pressed(LCD.DOWN):
		lcd.set_backlight(1)
		if menuSelect < len(menuList) - 1: 
			menuSelect = menuSelect + 1
			time.sleep(0.1)
		update_menu(menuSelect)
		start_time = time.time()
		
	if lcd.is_pressed(LCD.UP):
		lcd.set_backlight(1)
		if menuSelect > 0:
			menuSelect = menuSelect - 1
			time.sleep(0.1)
		update_menu(menuSelect)
		start_time = time.time()
		
		
	if lcd.is_pressed(LCD.SELECT) or lcd.is_pressed(LCD.RIGHT):
		lcd.set_backlight(1)
		menu_exec(menuSelect)
		time.sleep(0.1)
		start_time = time.time()
		
		
	elapsed_time = time.time() - start_time
	
	if elapsed_time >= MENU_BLANK_TIME:
		lcd.set_backlight(0)
	else:
		lcd.set_backlight(1)
		
	


