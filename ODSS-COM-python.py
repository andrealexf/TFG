'''
!pip install numpy
!pip install pypiwin32
!pip install pandas
!pip install matplotlib
!pip install dss-python
'''

from pathlib import Path
import math
import os
import re
import ast
from dataclasses import dataclass
from itertools import chain
import json
import DSSStartup as dsss

@dataclass(frozen=True)
class cargaBT:
    load: str
    kw: float
    daily: str
    def getLoad(self): return self.load
    def getKw(self): return self.kw
    def getDaily(self): return self.daily

os.chdir('C://Users//Andre//Downloads//TFG//Desenvolvimento-SegundoSemestre//QGIS-OPENDSS//IJAU11')
mydir = os.getcwd()
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

'''
DSSText.Command = 'Redirect ' + mydir + '/BRR_AREARURAL.dss'
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

#DSSSolution.Solve()

nome_arquivo = "ramal.txt"
diretorio = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(diretorio, nome_arquivo)

arquivoBT = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS\IJAU11\CargasBT_DU01_2022124950_IJAU11_--MBS-1--T--.dss"
arquivoLS = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS\IJAU11\CurvaCarga_2022124950_IJAU11_--MBS-1--T--.dss"

# --------------------------------------
def norm(b):
    return (b or "").split(".", 1)[0].lower()

def getLoads(transformer):
    defineBranchName(transformer)
    print(DSSTopology.BranchName)
    global bus1
    global bus2
    #loadIpList = []
    loadList = []
    DSSTopology.ForwardBranch


    while DSSTopology.BranchName != '' and DSSTopology.BranchName.split(".")[0] != "Transformer" and ((DSSTopology.BranchName.split(".", 1)[1]).split("_", 1)[0])[:3] != "smt":  # enquanto line não for smt...

        bus1 = DSSCktElement.BusNames[0]
        bus2 = DSSCktElement.BusNames[1]
        print("")
        print(DSSTopology.BranchName)
        #voltageBus(bus1)

        if busLoads(bus2):
            print(" ", busLoads(bus2))
            #loadIpList.append(busLoads(bus2))

            if (busLoads(bus2)[0].split("_", 1)[1])[:2] != "ip":
                #print(" ", busLoads(bus2))
                loadList.append(busLoads(bus2))
                #load = busLoads(bus2)[0]
                #voltageBus(bus2, load)

        ramal = DSSTopology.BranchName
        DSSTopology.ForwardBranch

    loadList = list(chain.from_iterable(loadList))
    defineBranchName(ramal)
    print("")
    # print("Número de cargas no transformador:", alvo, " :", len(loadIpList), loadIpList)
    print("Número de cargas no transformador (excluindo iluminação):", len(loadList), loadList)
    #print("")
    return loadList

'''
def createGD(nomeBairro, loadList: list, mult: float = 1, limpar: bool = False):

    txt = nomeBairro + "-mult" + str(mult) + "-pv.dss"
    # txt = "APAGAR-pv.dss"
    pvdss = pv_dir / txt

    mode = "w" if limpar else "a"

    with pvdss.open(mode, encoding="utf-8") as f:
        f.write("")

    PVnumber = 0
    norepeat = {}

    for i in range(len(loadList)):

        encontrar = ((loadList[i])[0]).split("_")[1]

        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.readlines()

        for linha in conteudo:
            if linha.split(" ", 2)[1] == encontrar:
                ramal = linha.split(" ", 2)[1]
                energia = float(linha.split(" ")[3])

                if energia == 0:
                    continue

                else:
                    pvname = ((loadList[i])[0]).split("_")[1]
                    norepeat[pvname] = norepeat.get(pvname, 0) + 1
                    pvname = pvname if norepeat[pvname] == 1 else f"{pvname}_{norepeat[pvname]}"

                    pot = (energia) / (24 * 30 * 0.17)
                    pot = pot * mult
                    kva = math.ceil(pot)

                    DSSCircuit.SetActiveElement("load." + (loadList[i])[0])
                    bus = str(DSSCktElement.BusNames).strip("(',')")
                    pn = phasesNumber(bus)

                    txt = 'New "PVsystem.GD.BT.' + pvname + '" phases=' + pn + ' bus1=' + bus + ' conn=Delta kv=0.22 pf=0.92 pmpp=' + f"{pot:.2f}" + ' kva=' + f"{kva:.2f}" + ' irradiance=0.98' + '\n' + '~ temperature=25 %cutin=0.1 %cutout=0.1 effcurve=Myeff P-TCurve=MyPvsT Daily=PVIrrad_diaria TDaily=MyTemp' + '\n' + '\n'

                    with pvdss.open("a", encoding="utf-8") as f:
                        f.write(txt)

                    #print('New "PVsystem.GD.BT.' + pvname + '" phases=' + pn + ' bus1=' + bus + ' conn=Delta kv=0.22 pf=0.92 pmpp=' + f"{pot:.2f}" + ' kva=' + f"{kva:.2f}" + ' irradiance=0.98'+'\n')
                    #print('~ temperature=25 %cutin=0.1 %cutout=0.1 effcurve=Myeff P-TCurve=MyPvsT Daily=PVIrrad_diaria TDaily=MyTemp'+"\n")
                    #print('')
                    PVnumber += 1


    print(PVnumber)
'''

def createGD2(nomeBairro, loadList: list[cargaBT], mult: float = 1, limpar: bool = False):

    txt = nomeBairro + "-mult" + str(mult) + "-pv.dss"
    # txt = "APAGAR-pv.dss"
    pvdss = pv_dir / txt

    mode = "w" if limpar else "a"

    with pvdss.open(mode, encoding="utf-8") as f:
        f.write("")

    PVnumber = 0

    for cargas in loadList:

        pot = float(cargas.getKw()) * mult

        pvname = cargas.getLoad()
        ene = loadShapeSum(pot , cargas.getDaily())
        pot = ene / (0.17*24)
        kva = math.ceil(ene)

        DSSCircuit.SetActiveElement("load." + (cargas.getLoad()))
        bus = str(DSSCktElement.BusNames).strip("(',')")
        pn = phasesNumber(bus)

        txt = 'New "PVsystem.GD.' + pvname + '" phases=' + pn + ' bus1=' + bus + ' conn=Delta kv=0.22 pf=0.92 pmpp=' + str(pot) + ' kva=' + str(kva) + ' irradiance=0.98' + '\n' + '~ temperature=25 %cutin=0.1 %cutout=0.1 effcurve=Myeff P-TCurve=MyPvsT Daily=PVIrrad_diaria TDaily=MyTemp' + '\n' + '\n'

        with pvdss.open("a", encoding="utf-8") as f:
            f.write(txt)

        PVnumber += 1

    print(PVnumber)

def loadShapeSum(pot: float, tipo: str) -> float:

    padrao = re.compile(
        r'Loadshape.\s*([^"]+)'
        r'.*?mult\s*=(.*)$'
        , re.IGNORECASE)

    ene = 0

    with open(arquivoLS, "r", encoding="utf-8") as f:

        for linha in f:
            m = padrao.search(linha)

            if not m:
                continue

            tipencontrada, curva = m.group(1), m.group(2).strip()

            if tipencontrada == tipo:
                loadshapeTuple = ast.literal_eval(curva)
                ene = pot * sum(loadshapeTuple)

    return ene

def busLoads(bus_base: str):  # cargas conectadas à barra
    alvo = norm(bus_base)
    allLoadList = []

    loads = DSSCircuit.Loads
    i = loads.First

    while i > 0:
        if alvo in [norm(b) for b in DSSCktElement.BusNames]:
            allLoadList.append(DSSCktElement.Name.split(".", 1)[1])  # só o nome depois do ponto

        i = loads.Next

    return allLoadList

def voltageBus(bus1, load=None):

    if load is not None:  # para cargas

        DSSCircuit.SetActiveElement("Load." + load)
        #print("     Carga: ",DSSCircuit.ActiveCktElement.Name)
        pu = DSSCircuit.ActiveBus.puVmagAngle
        pu_round = tupleFormat(pu, casas=4)
        #print("     (p.u., ang): ", pu_round)
        #overvoltage(pu_round)

    else: #linhas e transformadores

        DSSCircuit.SetActiveBus(bus1)
        #print("Linha: ", DSSCircuit.ActiveCktElement.Name)
        pu = DSSCircuit.ActiveBus.puVmagAngle
        pu_round = tupleFormat(pu, casas=4)
        #print("(p.u., ang): ", pu_round)
        #overvoltage(pu_round)

def findLoad(loadlist: list) -> list[cargaBT]: #obtem kw e o tipo de curva da carga

    cargasBTList = []
    padrao = re.compile(
        r'Load.\s*([^"]+)'
        r'.*?kw\s*=\s*([^ ]+)'
        r'.*?daily\s*=\s*"([^"]*)"'
        , re.IGNORECASE)

    with open(arquivoBT, "r", encoding="utf-8") as f:

        for linha in f:
            m = padrao.search(linha)

            if not m:
                continue

            loadencontrada, kw, daily = m.group(1), m.group(2), m.group(3).strip()

            for load in loadList:
                if loadencontrada == load.upper():

                    cargasBTList.append(cargaBT(load = loadencontrada, kw = kw, daily = daily))

    return cargasBTList

def phasesNumber(bus: str) -> str:
    phases = bus.count(".")

    switch = {
        2: 1,
        3: 1,
        4: 3
    }
    return str(switch.get(phases))

def tupleFormat(tupla, casas=4):

    return tuple(round(x, casas) for x in tupla)

def overvoltage(tupla):
    encontrados = []

    for i, valor in enumerate(tupla):
        if i % 2 == 0 and valor > 1.02:
            print("Valor maior que 1.02")

def verboseSolve(datapath):
    DSSText.Command = 'set datapath="' + datapath + '"'
    DSSText.Command = 'set mode=daily'
    DSSText.Command = 'set number=24'
    DSSText.Command = 'set DemandInterval=true'
    DSSText.Command = 'set overloadreport=true'
    DSSText.Command = 'set voltexceptionreport=true'
    DSSText.Command = 'set DIVerbose=true'
    DSSText.Command = 'solve'
    DSSText.Command = 'closeDI'

    DSSText.Command = 'clear'
    DSSText.Command = 'Compile ' + mydir + '/Master_DU01_2022124950_IJAU11_--MBS-1--T--.dss'

def defineBranchName(alvo: str) -> bool:
    ok = DSSTopology.First > 0
    while ok:
        if DSSTopology.BranchName.lower() == alvo.lower():
            DSSCircuit.SetActiveElement(DSSTopology.BranchName)
            return True
        ok = DSSTopology.Next > 0

    return False


pv_dir = Path('C://Users//Andre//Downloads//TFG//Desenvolvimento-SegundoSemestre//BRR-PVSyst')

brr = os.path.join(diretorio, "brr.json")
with open(brr, "r", encoding="utf-8") as f:
    brr = json.load(f)

bairros = {}
for lista, trafo in brr.items():

    listaTrafo = trafo.split(',')
    bairros[lista] = [int(x) for x in listaTrafo]

mult = {
            0: 1.2,
            1: 1.4,
            2: 1.6,
            3: 1.8,
            4: 1.8,
            5: 2.0
        }

for j in range(4):
    cargasBTList = []

    for nomeBairro, transformador in bairros.items():

        for i in range(len(bairros[nomeBairro])):

            print(bairros[nomeBairro][i])
            alvo = ("transformer.TRF_"+str(bairros[nomeBairro][i])+"a").lower()
            #print(alvo)
            loadList = getLoads(alvo)
            cargasBTList = findLoad(loadList)
            createGD2(nomeBairro, cargasBTList,mult.get(j), limpar=(i == 0))

    txt = "mult" + str(mult.get(j))
    txtVP = (Path(r"C:\\Users\\Andre\\Downloads\\TFG\\Desenvolvimento-SegundoSemestre\\Resultados\\Verbose") / txt).resolve()
    #print(txtVP)
    datapath = str(txtVP)
    #verboseSolve(datapath)


'''
#agora = ['Transformer.trf_1081464a']
alvo="Transformer.trf_165914a".lower() #transformador linha 7067 do isolated: trf_1081464a (). trf_166467a linha 26044 (165 cargas)
loadList = getLoads(alvo)  # obtem as cargas conectadas a um transformador
#createGD(loadList)

DSSText.Command = 'set datapath ="C://Users//Andre//Downloads//TFG//Desenvolvimento-SegundoSemestre//Resultados//Verbose//"'
DSSText.Command = 'set mode=daily'
DSSText.Command = 'set number=24'
DSSText.Command = 'set DemandInterval=true'
DSSText.Command = 'set overloadreport=true'
DSSText.Command = 'set voltexceptionreport=true'
DSSText.Command = 'set DIVerbose=true'
DSSText.Command = 'solve'
DSSText.Command = 'closeDI'
'''

'''
print("")
print("Active Element:",DSSCktElement.Name)
print("Branch Name:",DSSTopology.BranchName)
print("")
print("Nome da ultima linha: ", DSSTopology.BranchName,'\n', "Bus2: ", bus2,'\n', "Quantidade de cargas conectadas: ", len(busLoads(bus2)), busLoads(bus2))
'''

kW_BC = DSSCircuit.TotalPower[0]  # in kW
kvar_BC = DSSCircuit.TotalPower[1]  # in kVAr
kW_Loss_BC = DSSCircuit.Losses[0] / 1000  # property returns values in W, here stored in kW
kvar_Loss_BC = DSSCircuit.Losses[1] / 1000  # property returns values in VAr, here stored in kVAr

print('')
print("----------")
print("Total kW delivered to the network: %.3f kW" %kW_BC)
print("Total kVAr delivered to the network: %.3f kvar" %kvar_BC)
print("Total active losses: %.3f kW" %kW_Loss_BC)
print("Percent losses: %.3f" %abs(((kW_Loss_BC/kW_BC)*100)) + "%")
print("Total reactive losses: %.3f kVAr" %kvar_Loss_BC)
print("----------")

print('fim')
