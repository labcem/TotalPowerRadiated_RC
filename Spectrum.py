# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 12:57:09 2013

@author: J89950
"""

from visa import instrument
from numpy import *

class FSV30():
    def __init__(self,address=21):
        self.ctrl = instrument("GPIB::%s" %address,timeout=None)

    def reset(self):
        """ RESET """
        self.ctrl.write("*RST")
        self.ctrl.write(":INST SAN;*SRE 32;STATUS:PRESET")
        self.ctrl.write(":INP1:PRES ON")
        self.ctrl.write("DISP :TRAC:X:SPAC LIN;SCAN:RANG:COUN 1;INIT2:CONT OFF;INIT:IMM;*SRE 136;*ESE 64")
        self.ctrl.write("FORMAT:DATA REAL;*CLS;:CALC:UNIT:POW DBUV")
        self.ctrl.write(":CORR:TRANS OFF;:INIT:CONT ON;:SYST:DISP:UPD ON")
        self.ctrl.write("FORM ASC")
        print 'OK'
        return True

    def centerFreq(self,value):
        """ set the center frequency"""
        return self.ctrl.write("FREQ:CENT %s HZ ;:INIT" %value)

    def startFreq(self,value):
        """ set the start frequency"""
        return self.ctrl.write("FREQ:START %s HZ" %value)

    def stopFreq(self,value):
        """ set the stop frequency"""
        return self.ctrl.write("FREQ:STOP %s HZ" %value)

    def SPAN(self,value):
        """ set the SPAN"""
        return self.ctrl.write("FREQ:SPAN %s HZ" %value)

    def RBW(self,value):
        """ set the RBW"""
        return self.ctrl.write("BAND:RES %s Hz" %value)


    def VBW(self,value):
        """ set the VBW"""
        return self.ctrl.write("BAND:VID %s Hz" %value)

    def Sweep(self,value):
        """ set the sweep time """
        return self.ctrl.write(":SWE:TIME:AUTO OFF;:SWE:TIME %s ms" %value)

    def MaxHold(self):
        """ Max Hold trace mode"""
        return self.ctrl.write("DISP:TRAC:MODE MAXH")

    def readwrite(self):
        """Mode READ/WRITE"""
        return self.ctrl.write("DISP:TRAC:MODE WRIT")

    def SweepPoint(self,value):
        """sweep point number (from 101 to 32001)"""
        return self.ctrl.write("SWE:POIN %s" %value)

    def InputAtt(self,value):
        """set the value of the input attenuator"""
        return self.ctrl.write("INP:ATT %s dB " %value)

    def InputAttAuto(self):
        """input attenuation automatic"""
        return self.ctrl.write("INP:ATT:AUTO ON")

    def UnitDBM(self):
        """set the unit in dBm"""
        return self.ctrl.write("UNIT:POW DBM")

    def getTrace(self,value):
        """ get the trace"""
        s=self.ctrl.ask("TRAC? TRACE1")
        res=s.split(",")
        Data=zeros(value)
        for i in range(0,len(Data)):
            Data[i]=eval(res[i])
        return Data

    def MarkerMax(self,value):
        """ get the marker maximum value"""
        self.ctrl.write("CALC:MARK1:X %s Hz" %value)
        MarkerValue=self.ctrl.ask("CALC:MARK1:Y?")
        return MarkerValue

    def setRefLevel(self,value):
        """set the reference level in dBm"""
        return self.ctrl.write("DISP:TRAC:Y:RLEV %s dBm" %(value))
