# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:25:50 2013

@author: emmanuel.amador@edf.fr
"""
from __future__ import division
import time
from numpy import *
import visa
import os
import scipy
from pylab import *


from Stirrer import *
from Spectrum import *

Qcal=loadtxt('Qcal.txt')
Q=Qcal[:,1]
name=raw_input('Entrer le  du materiel sous test?')#Creation du répertoire de travail
if (os.path.isdir('Resultats_'+name)==False):#Test si le repertoire existe deja
    os.mkdir('Resultats_'+name)

os.chdir('Resultats_'+name)


V=54.5 #volume of the chamber

###############################################
##########  Testing Parameters   ##############
###############################################

#Frequency range####################################
f=Qcal[:,0] #loaded from the calibration file
Nf=len(f) #number of frequency
f0=f[0]
f1=f[Nf]

#Brasseur######################################
N=50 # number of stirrer positions
Angles=linspace(360/N,360,N) # list of stirrer angular positions

#DSpectrum analyser parameters####################################
fcenter=0.5*(f1+f0)  #center frequency
fspan=f1-f0     #span
RBW=1e6         #Filter width
VBW=1e6         #Video filter width
SWP=40          #Sweep time
SwpPt=Nf        #Number of frequencies
Tmes=1          #Dwell time

###############################################
###### Instrument init. ##########
###############################################
print '_______________\nInitialisations\n'

print 'Stirrer init.'
stirrer=Stirrer('/com2',1)
print u'Back to 0°'
stirrer.reset()


print '\nSpectrum init.'
spectrum=FSV30()
spectrum.reset()
spectrum.SweepPoint(SwpPt)   #Réglage du nombre de pts
spectrum.UnitDBM()            #Réglage en de l'unité en dBm
spectrum.centerFreq(fcenter)
spectrum.SPAN(fspan)
spectrum.RBW(RBW)

peaksindx=[66,122]    #list of indexes of the center frequencies of every channel
criterion=-55         #stop criterion: value in dBm of the value that states that an emmission is measured.


####################################################
################# Measurement ######################
####################################################
PowMeas=zeros(len(Angles)) #Pow measured matrix
Measurement=zeros((N,2))
SauvTrace=zeros((N,SwpPt))
for i in range(0,len(Angles)): #boucle sur les positions du brasseur
    brasseur.setPosition(int(Angles[i]))
    time.sleep(3)
    spectrum.readwrite()
    spectrum.MaxHold()
    time.sleep(Tmes)
    Level = spectrum.getTrace(SwpPt)    #Aquisition du signal mesuré
    while (min(Level[peaksindx])<criterion):
        Level = spectrum.getTrace(SwpPt)
        time.sleep(Tmes)
    Level = Spectre.getTrace(SwpPt)
    MaxLevel=max(Level)           #Recherche du maximum
    MaxIdx =Level.argmax()             #Recherche de l'index du max
    MaxFreq=f[MaxIdx]  #Recherche de la frequence du max
    Measurement[i,:]=array([MaxFreq,MaxLevel)#Matrice de sauvegarde des données
    SauvTrace[i,:]= Level
    Powtotal=(V*16*pi**2/(3e8/f)**3*(10**(SauvTrace[0:i,:]/10)/1000).mean(axis=0)/Q)
    print 'N = %3d, f = %2.2f MHz, Pmeas= %2.2f dBm, total power radiated = %2.2f mW/MHz' %(i+1,MaxFreq/1e6,MaxLevel,1000*Powtotal.max())

#Post-treatment
PowMaxAvg=(10**(SauvTrace/10)/1000).mean(axis=0)
Pt=(V*16*pi**2/(3e8/Frequence)**3*PowMaxAvg/Q)
savez(name+".npz",Angles=Angles,f=f,Measure=Measure,SauvTrace=SauvTrace,Q=Q,Pt=Pt)

ioff()
plot(f/1e6,Pt)
grid()
xlabel("f/MHz")
ylabel("P/W")
title("Total radiated power")
savefig(name+".pdf",bbox_inches="tight")
savefig(name+".png",bbox_inches="tight")
close()
