# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:25:50 2013

@author: Administrateur
"""
from __future__ import division
import time
from numpy import *
import visa
from pylab import *
#Chargement des classes du matériel employé
from Stirrer import *
from SignalGenerator import *
from Spectrum import *


###############################################
##########  Testing Parameters   ##############
###############################################

#Fréquences####################################
f0=2.4e9 #Start frequency
f1=2.5e9 #Stop frequency

#Spectrum analyser####################################

#Frequencies
Nf=1001 #number of frequencies
f=linspace(f0,f1,Nf) #list of frequencies
fcenter=0.5*(f0+f1)   #center frequency
fspan=f1-f0   #span
RBW=1000e3       #RBW width
VBW=1000e3       #VBW width
SwpPt=Nf        #number of points

#Stirrer######################################
N=100 # number of stirrer positions
Angles=linspace(360/N,360,N) #list of positions angles

#Level#######################################
#Output power level
P0=-10 #power level
cablelosses=-0.95 #Cable losses


###############################################
###### Instrument init. ##########
###############################################
print '_______________\nInitialisations\n'

print 'Stirrer init.'
stirrer=Stirrer('/com2',1)
print u'Back to 0°'
stirrer.reset()

print '\nSignal generator init.'
gene=RS_SMF100A()
gene.reset()
gene.off() #RF OFF
gene.setPower(P0-cablelosses)
gene.setFreq(f0)

print '\nSpectrum init.'
spectrum=FSV30()
spectrum.reset()
spectrum.SweepPoint(SwpPt)   #Réglage du nombre de pts
spectrum.UnitDBM()            #Réglage en de l'unité en dBm
spectrum.centerFreq(int(fcenter))
spectrum.SPAN(fspan)
spectrum.RBW(RBW)

####################################################
################# Measurement ######################
####################################################

PowIn=zeros((len(Angles),len(f))) #Power in Matrix
PowMeas=zeros((len(Angles),len(f))) #Measured Power Matrix
Measurement=zeros((1,4))
for i in range(0,len(Angles)): #loop over the stirrer positions
    print '\nRotation Brasseur'
    stirrer.setPosition(int(Angles[i]))
    print 'OK\n'
    print'Stabilisation Brasseur'
    time.sleep(5)
    print'OK\n'
    gene.on()
    for j in range(0,len(f)): #loop over the frequencies
        gene.setFreq(f[j])
        gene.setPower(P0-cablelosses)
        time.sleep(0.02)
        Level = spectrum.getTrace(SwpPt)
        max(Level)           #
        PowIn[i,j]=P0
        PowMeas[i,j]=max(Level)
        Measurement=vstack((Measurement,array([Angles[i],f[j],PowIn[i,j],PowMeas[i,j]])))
        print 'N = %3d, f = %2.2f MHz, Pin = %2.2f dBm, Pmeas= %2.2f dBm' %(i+1,f[j]/1e6,P0,PowMeas[i,j])
    gene.off()

V=54.5 #volume of the chamber in m^3
PowMeasAvg=(10**(PowMeas/10)/1000).mean(axis=0) #average measured power over the stirrer positions
Q=V*16*pi**2/(3e8/f)**3*PowMeasAvg/(10**(P0/10)/1000 ) #quality factor

Q=transpose(array([f,Q]))

savetxt('Qcal.txt',Q) #saving the calibration

savez('Q.npz',f=f,PowMeas=PowMeas) #raw values

ioff()
plot(Q[:,0],Q[:,1])
xlabel('f en Hz')
ylabel('Q')
grid('on')
savefig('Qcal.pdf',bbox_inches="tight")
#savefig('Qcal.png',bbox_inches="tight")
close()
