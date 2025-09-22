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

#--------------------------------------

def defineBranchName(alvo: str) -> bool:

    ok = DSSTopology.First > 0
    while ok:
        if DSSTopology.BranchName.lower() == alvo.lower():
            DSSCircuit.SetActiveElement(DSSTopology.BranchName)
            return True
        ok = DSSTopology.Next > 0

    return False

def getLoads(transformer):
    defineBranchName(transformer)
    global bus1
    global bus2
    teste = []
    loadList = []

    while ((DSSTopology.BranchName.split(".", 1)[1]).split("_", 1)[0])[:3] != "smt":  # enquanto line não for smt...

        bus1 = DSSCktElement.BusNames[0]
        bus2 = DSSCktElement.BusNames[1]
        print(DSSTopology.BranchName)
        if busLoads(bus2):
            print(" ", busLoads(bus2))
            teste.append(busLoads(bus2))

            if (busLoads(bus2)[0].split("_", 1)[1])[:2] != "ip":
                loadList.append(busLoads(bus2))

        ramal = DSSTopology.BranchName
        DSSTopology.ForwardBranch

    defineBranchName(ramal)
    print("Número de cargas no transformador:", alvo, " :", len(teste), teste)
    print("Número de cargas no transformador (excluindo iluminação):", len(loadList), loadList)
    return bus1, bus2

def busLoads(bus_base: str): #cargas conectadas à barra
    alvo = norm(bus_base)
    allLoadList = []

    loads = DSSCircuit.Loads
    i = loads.First

    while i > 0:
        if alvo in [norm(b) for b in DSSCktElement.BusNames]:
            allLoadList.append(DSSCktElement.Name.split(".", 1)[1])  # só o nome depois do ponto

        i = loads.Next

    return allLoadList

def norm(b):
    return (b or "").split(".", 1)[0].lower()

alvo = "transformer.TRF_1081464A".lower()
getLoads(alvo)#obtem as cargas conectadas a um transformador

print("")
print("Active Element:",DSSCktElement.Name)
print("Branch Name:",DSSTopology.BranchName)
print("")
print("Nome da ultima linha: ", DSSTopology.BranchName,'\n', "Bus2: ", bus2,'\n', "Quantidade de cargas conectadas: ", len(busLoads(bus2)), busLoads(bus2))


#Monitors = DSSCircuit.Monitors.AllNames
#print (str(len(Monitors)) + ' Monitors')

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