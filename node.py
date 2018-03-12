#!/usr/bin/env python

import broadlink

def __init__:
	type = 0x2711
	host = 192.168.1.158
	mac  = 

def connect:
	dev = broadlink.gendevice(type, (host, 80), mac)
	dev.auth()

def on:
	dev.set_power(True)
    if dev.check_power():
        print '== Turned * ON * =='
    else:
        print '!! Still OFF !!'

def off:
	    dev.set_power(False)
    if dev.check_power():
        print '!! Still ON !!'
    else:
        print '== Turned * OFF * =='
