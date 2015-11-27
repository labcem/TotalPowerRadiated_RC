# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 17:18:33 2012
Stirrer
@author: E68972
"""

import minimalmodbus
import time
from numpy import *

class Stirrer(minimalmodbus.Instrument):
    """ Instrument class for the stirrer at Les Renardières.
    Args:
        * portname (str)
        *slaveaddress (int): address RTU (1)
    """
    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self,portname,slaveaddress)
        self.serial.baudrate = 9600
        #self.serial.parity = serial.PARITY_NONE
        self.serial.bytesize = 8
        self.serial.stopbits = 1
        self.serial.timeout = 0.05

    def reset(self):
        """ back to 0°"""
        self.write_long(57766,0)
        posmesuree=self.read_long(58144,3)
        while posmesuree != 0:
            posmesuree=self.read_long(58144,3)
            time.sleep(.5)
        print 'Reset OK'

    def getPosition(self):
        """ get the current stirrer position"""
        return self.read_long(58144,3)

    def setPosition(self,position):
        """ go to the angle  +/- angle in °"""
        self.write_long(57766,position*10,signed=True)
        posmesuree=nan
        while posmesuree != position*10:
            posmesuree=self.read_long(58144,3)
            time.sleep(.1)
        #print 'Position OK'
