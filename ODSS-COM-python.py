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
import DSSStartup as dsss


os.chdir('C://Users//Andre//Downloads//TFG//Desenvolvimento-SegundoSemestre//QGIS-OPENDSS//IJAU11')
mydir=os.getcwd()
print(mydir)


DSSStartOK, DSSObj, DSSText = dsss.DSSStartup()
if not DSSStartOK:
    print('Unable to start the OpenDSS Engine')
    import sys
    sys.exit()

DSSCircuit = DSSObj.ActiveCircuit

DSSSolution = DSSCircuit.Solution
DSSActiveBus = DSSCircuit.ActiveBus
DSSCktElement = DSSCircuit.ActiveCktElement
DSSTopology = DSSCircuit.Topology
DSSText = DSSObj.Text
ControlQueue = DSSCircuit.CtrlQueue

DSSObj.AllowForms = 0

DSSText.Command = 'clear'
DSSText.Command = 'Compile ' + mydir + '/Master_DU01_2022124950_IJAU11_--MBS-1--T--.dss'

DSSText.Command = 'Redirect ' + mydir + '/BRR_AREARURAL.dss'

'''
DSSText.Command = 'Redirect ' + mydir + '/BRR_AVENIDA.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_BOAVISTA.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_BPS.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_CENTRO.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_CRUZEIRO.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_ESTIVA.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_MORROCHIC.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_NOSSASENHORADAAGONIA.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_PINHEIRINHO.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_SANTOANTONIO.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_SAOVICENTE.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_UNIFEI.dss'
DSSText.Command = 'Redirect ' + mydir + '/BRR_VILAISABEL.dss'
'''

DSSSolution.Solve()
'''
linha = "smt_2621843"
LineActive = DSSTopology.SetBranchActive(f"Line.{linha}")
assert LineActive, "No line"
'''

alvo = "Line.smt_2621843".lower()   # a sua linha X

ok = DSSTopology.First > 0
found = False
while ok:
    if DSSTopology.BranchName.lower() == alvo:
        found = True
        break
    ok = DSSTopology.Next > 0

if not found:
    raise RuntimeError("Ramo 'Line.X' não encontrado na Topology")
#-----------------------------------------------------------
if DSSTopology.ForwardBranch > 0: #vai para o próximo elemento

    prox_nome = DSSTopology.BranchName
    print("Próximo elemento: ",prox_nome)

else:
    print("Não há ramo")

DSSCircuit.SetActiveBus('981764')
DSSCircuit.SetActiveElement('Line.smt_2621843')
#print(DSSCktElement.Name)

DSSLines = DSSCircuit.Lines

DSSCircuit.SetActiveClass('Transformer')
lineList = []

print(DSSLines.Bus1)
print(DSSCircuit.NextElement)
#print(DSSCircuit.Transformers.Next)
#print(DSSLines.Next)
#i = DSSCircuit.SetActiveBus('981764')

#print(DSSActiveBus.LineList)

Monitors = DSSCircuit.Monitors.AllNames

print (str(len(Monitors)) + ' Monitors')
DSSText.Command = "Plot monitor object=TOTALpower channels=(1 3 5)"

#- Circuit Summary -

kW_BC = DSSCircuit.TotalPower[0] #in kW
kvar_BC = DSSCircuit.TotalPower[1] #in kVAr
kW_Loss_BC = DSSCircuit.Losses[0]/1000 #property returns values in W, here stored in kW
kvar_Loss_BC = DSSCircuit.Losses[1]/1000 #property returns values in VAr, here stored in kVAr
'''
print("----------")
print("Total kW delivered to the network: %.3f kW" %kW_BC)
print("Total kVAr delivered to the network: %.3f kvar" %kvar_BC)
print("Total active losses: %.3f kW" %kW_Loss_BC)
print("Percent losses: %.3f" %abs(((kW_Loss_BC/kW_BC)*100)) + "%")
print("Total reactive losses: %.3f kVAr" %kvar_Loss_BC)
print("----------")
'''