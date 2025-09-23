'''
!pip install numpy
!pip install pypiwin32
!pip install pandas
!pip install matplotlib
!pip install dss-python
'''
import math

import numpy as np
import matplotlib as mpl
import math
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

nome_arquivo = "ramal.txt"

diretorio = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(diretorio, nome_arquivo)

with open(arquivo, "r", encoding="utf-8") as f:
    conteudo = f.readlines()


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
    loadIpList = []
    loadList = []

    while ((DSSTopology.BranchName.split(".", 1)[1]).split("_", 1)[0])[:3] != "smt":  # enquanto line não for smt...

        bus1 = DSSCktElement.BusNames[0]
        bus2 = DSSCktElement.BusNames[1]
        #print(DSSTopology.BranchName)
        if busLoads(bus2):
            #print(" ", busLoads(bus2))
            loadIpList.append(busLoads(bus2))

            if (busLoads(bus2)[0].split("_", 1)[1])[:2] != "ip":
                loadList.append(busLoads(bus2))

        ramal = DSSTopology.BranchName
        DSSTopology.ForwardBranch

    defineBranchName(ramal)
    #print("Número de cargas no transformador:", alvo, " :", len(loadIpList), loadIpList)
    #print("Número de cargas no transformador (excluindo iluminação):", len(loadList), loadList)
    return loadList

def createGD(loadList: list):

    for i in range(len(loadList)):

        encontrar = ((loadList[i])[0]).split("_")[1]

        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.readlines()

        for linha in conteudo:
            if linha.split(" ", 2)[1] == encontrar:

                ramal = linha.split(" ", 2)[1]
                energia = float(linha.split(" ")[3])
                pot = energia/(24*30*0.17)
                kva = math.ceil(pot)

                print("Nome do ramal: ", ramal, " -- Média de Energia: ", energia)
                DSSCircuit.SetActiveElement("load."+(loadList[i])[0])
                bus = str(DSSCktElement.BusNames).strip("(',')")
                print('New "PVsystem.GD.BT.'+ramal+'" phases=1 bus1='+bus+' conn=Delta kv=0.22 pf=0.92 pmpp='+f"{pot:.2f}"+' kva='+f"{kva:.2f}"+' irradiance=0.98')
                print('~ temperature=25 %cutin=0.1 %cutout=0.1 effcurve=Myeff P-TCurve=MyPvsT Daily=PVIrrad_diaria TDaily=MyTemp')

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
loadList = getLoads(alvo)#obtem as cargas conectadas a um transformador
createGD(loadList)

'''
print("")
print("Active Element:",DSSCktElement.Name)
print("Branch Name:",DSSTopology.BranchName)
print("")
print("Nome da ultima linha: ", DSSTopology.BranchName,'\n', "Bus2: ", bus2,'\n', "Quantidade de cargas conectadas: ", len(busLoads(bus2)), busLoads(bus2))
'''

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

print('fim')