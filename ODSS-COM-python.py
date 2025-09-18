'''
!pip install numpy
!pip install pypiwin32
!pip install pandas
!pip install matplotlib
!pip install dss-python
'''

import numpy as np
import matplotlib as mpl
import pandas as pd
import os

os.chdir('C://Users//Andre//Downloads//TFG//Desenvolvimento-SegundoSemestre//QGIS-OPENDSS//IJAU11')
mydir=os.getcwd()
print(mydir)

import DSSStartup as dsss  # DSSStartup is a function for starting up the DSS; must be downloaded and stored in the working folder

# create de DSS object
DSSStartOK, DSSObj, DSSText = dsss.DSSStartup()    # DSSObj is the DSS object
if not DSSStartOK:
    print('Unable to start the OpenDSS Engine')
    import sys
    sys.exit()

DSSCircuit = DSSObj.ActiveCircuit

DSSSolution = DSSCircuit.Solution
ControlQueue = DSSCircuit.CtrlQueue

DSSObj.AllowForms = 0
DSSText = DSSObj.Text

DSSText.Command = 'clear'

DSSText.Command = 'Compile ' + mydir + '/Master_DU01_2022124950_IJAU11_--MBS-1--T--.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_AREARURAL.dss'
DSSSolution.Solve()

DSSActiveBus = DSSCircuit.ActiveBus

DSSCircuit.SetActiveBus('981764')
DSSCircuit.SetActiveElement('Line.smt_2621843')
DSSLines = DSSCircuit.Lines


Monitors = DSSCircuit.Monitors.AllNames
print('List of Monitors')
print ('Total:' +  str(len(Monitors)))
print(Monitors)
#DSSText.Command = "Plot monitor object=TOTALpower channels=(1 3 5)"

#- Circuit Summary -

kW_BC = DSSCircuit.TotalPower[0] #in kW
kvar_BC = DSSCircuit.TotalPower[1] #in kVAr
kW_Loss_BC = DSSCircuit.Losses[0]/1000 #property returns values in W, here stored in kW
kvar_Loss_BC = DSSCircuit.Losses[1]/1000 #property returns values in VAr, here stored in kVAr
print("Total kW delivered to the network: %.3f kW" %kW_BC)
print("Total kVAr delivered to the network: %.3f kvar" %kvar_BC)
print("Total active losses: %.3f kW" %kW_Loss_BC)
print("Percent losses: %.3f" %abs(((kW_Loss_BC/kW_BC)*100)) + "%")
print("Total reactive losses: %.3f kVAr" %kvar_Loss_BC)
