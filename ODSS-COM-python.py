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
#MUDAR: OS CHDIR, ARQUIVOBT, ALVO

@dataclass(frozen=True)
class cargaBT:
    load: str
    kw: float
    daily: str
    def getLoad(self): return self.load
    def getKw(self): return self.kw
    def getDaily(self): return self.daily

os.chdir('C://Users//Andre//Downloads//TFG//Desenvolvimento-SegundoSemestre//QGIS-OPENDSS//IJAU11')
#os.chdir('C://Users//Andre//Downloads//TFG//Desenvolvimento-SegundoSemestre//QGIS-OPENDSS')
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
#DSSText.Command = 'Compile ' + mydir + '/circuitoexemplo.dss'


nome_arquivo = "ramal.txt"
diretorio = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(diretorio, nome_arquivo)

arquivoBT = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS\IJAU11\CargasBT_DU01_2022124950_IJAU11_--MBS-1--T--.dss"
#arquivoBT = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS\circuitoexemplo.dss" #circuito exemplo
arquivoLS = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS\IJAU11\CurvaCarga_2022124950_IJAU11_--MBS-1--T--.dss"

# --------------------------------------
def norm(b):
    return (b or "").split(".", 1)[0].lower()

def getLoads(transformer):
    defineBranchName(transformer)
    print(DSSTopology.BranchName)

    global bus1
    global bus2

    loadList = []
    DSSTopology.ForwardBranch

    while DSSTopology.BranchName != '' and DSSTopology.BranchName.split(".")[0] != "Transformer" and ((DSSTopology.BranchName.split(".", 1)[1]).split("_", 1)[0])[:3] != "smt":  # enquanto line não for smt...

        bus1 = DSSCktElement.BusNames[0]
        bus2 = DSSCktElement.BusNames[1]
        print("")
        voltageBus(bus1)

        if busLoads(bus2):

            m1m2 = busLoads(bus2)
            print(" ", m1m2) #envia como bus2 mas carga só possui uma bus (na função está como bus1)

            if (m1m2[0].split("_", 1)[1])[:2] != "ip":
                #print(" ", m1m2)
                loadList.append(m1m2)

                load = m1m2[0]
                #voltageBus(bus2, load)

                if voltageBus(bus2, load):
                    overVoltageList.append(m1m2)


        ramal = DSSTopology.BranchName
        DSSTopology.ForwardBranch

    loadList = list(chain.from_iterable(loadList))

    defineBranchName(ramal)
    print("")
    print("Número de cargas no transformador (excluindo iluminação):", len(loadList), loadList)

    return loadList

def createGD2(nomeBairro, loadList: list[cargaBT], mult: float = 1.0, limpar: bool = False):

    #txt = nomeBairro + "-mult" + str(mult) + "-pv.dss"
    txt = 'trf167839-hc-pv.dss'

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
        kva = math.ceil(pot)

        DSSCircuit.SetActiveElement("load." + (cargas.getLoad()))
        bus = str(DSSCktElement.BusNames).strip("(',')")
        pn = phasesNumber(bus)

        txt = 'New "PVsystem.GD.' + pvname + '" phases=' + pn + ' bus1=' + bus + ' conn=Delta kv=0.22 pf=0.92 pmpp=' + str(pot) + ' kva=' + str(kva) + ' irradiance=0.98' + '\n' + '~ temperature=25 %cutin=0.1 %cutout=0.1 effcurve=Myeff P-TCurve=MyPvsT Daily=PVIrrad_diaria TDaily=MyTemp' + '\n' + '\n'

        with pvdss.open("a", encoding="utf-8") as f:
            f.write(txt)

        PVnumber += 1

    print("Número de painéis fotovoltaicos adicionados: ",PVnumber)

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
        print("     Carga: ",DSSCircuit.ActiveCktElement.Name)
        pu = DSSCircuit.ActiveBus.puVmagAngle
        pu_round = tupleFormat(pu, casas=4)
        print("     (p.u., ang): ", pu_round)

        if overvoltage(pu_round):
            #overVoltageList.append(load)
            return True

    else: #linhas e transformadores

        DSSCircuit.SetActiveBus(bus1)
        print("Linha: ", DSSCircuit.ActiveCktElement.Name)
        pu = DSSCircuit.ActiveBus.puVmagAngle
        pu_round = tupleFormat(pu, casas=4)
        print("(p.u., ang): ", pu_round)
        overvoltage(pu_round)

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
                if loadencontrada.upper() == load.upper():

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

    global contadorOvervoltage

    if any(valor > 1.05 for valor in tupla[::2]):
        print("Valor maior que 1.05")
        contadorOvervoltage += 1
        return True

    else:
        return False

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

def solvetrf(alvo):

    #txt = '/trf167839-mult' + str(mult) + '-pv.dss'
    txt = '"trf167839-hc-pv.dss"'

    DSSText.Command = 'set datapath="C:\\Users\\Andre\\Downloads\\TFG\\Desenvolvimento-SegundoSemestre\\BRR-PVSyst"'
    DSSText.Command = 'redirect '+ txt

    DSSText.Command = 'set datapath="C:\\Users\\Andre\\Downloads\\TFG\\Desenvolvimento-SegundoSemestre\\QGIS-OPENDSS\\IJAU11"'
    DSSText.Command = 'set mode=snapshot'
    DSSText.Command = 'solve'

pv_dir = Path('C://Users//Andre//Downloads//TFG//Desenvolvimento-SegundoSemestre//BRR-PVSyst')

brr = os.path.join(diretorio, "brr.json")
with open(brr, "r", encoding="utf-8") as f:
    brr = json.load(f)

bairros = {}
for lista, trafo in brr.items():

    listaTrafo = trafo.split(',')
    bairros[lista] = [int(x) for x in listaTrafo]

mult = {
            0: 1.0,
            1: 1.2,
            2: 1.4,
            3: 1.6,
            4: 1.8,
            5: 2.0
        }

mult2 = {
            0: 1.0,
            1: 1.5,
            2: 2.0
        }
'''
for j in range(1):
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

contadorOvervoltage = 0

alvo="Transformer.trf_167839a".lower() #transformador linha 7067 do isolated: trf_1081464a (). trf_166467a linha 26044 (165 cargas)
#loadList = getLoads(alvo)
loadList = ['bt_11266978_m1', 'bt_11266978_m2', 'bt_1050133_m1', 'bt_1050133_m2', 'bt_1050126_m1', 'bt_1050126_m2', 'bt_1050112_m1', 'bt_1050112_m2', 'bt_10406755_m1', 'bt_10406755_m2', 'bt_1050105_m1', 'bt_1050105_m2', 'bt_1050098_m1', 'bt_1050098_m2', 'bt_1050091_m1', 'bt_1050091_m2', 'bt_1050077_m1', 'bt_1050077_m2', 'bt_4892503_m1', 'bt_4892503_m2', 'bt_1050070_m1', 'bt_1050070_m2', 'bt_1050056_m1', 'bt_1050056_m2', 'bt_1050049_m1', 'bt_1050049_m2', 'bt_1050063_m1', 'bt_1050063_m2', 'bt_3640476_m1', 'bt_3640476_m2', 'bt_1050084_m1', 'bt_1050084_m2', 'bt_3885504_m1', 'bt_3885504_m2', 'bt_1050042_m1', 'bt_1050042_m2', 'bt_1050035_m1', 'bt_1050035_m2', 'bt_1050028_m1', 'bt_1050028_m2', 'bt_1050021_m1', 'bt_1050021_m2', 'bt_1050014_m1', 'bt_1050014_m2', 'bt_1050007_m1', 'bt_1050007_m2', 'bt_1050000_m1', 'bt_1050000_m2', 'bt_4301661_m1', 'bt_4301661_m2', 'bt_4127207_m1', 'bt_4127207_m2', 'bt_1049993_m1', 'bt_1049993_m2', 'bt_1049986_m1', 'bt_1049986_m2', 'bt_1049979_m1', 'bt_1049979_m2', 'bt_1049972_m1', 'bt_1049972_m2', 'bt_11382069_m1', 'bt_11382069_m2', 'bt_10214815_m1', 'bt_10214815_m2', 'bt_1049965_m1', 'bt_1049965_m2', 'bt_1049958_m1', 'bt_1049958_m2', 'bt_1049951_m1', 'bt_1049951_m2', 'bt_1049937_m1', 'bt_1049937_m2', 'bt_1049930_m1', 'bt_1049930_m2', 'bt_1049923_m1', 'bt_1049923_m2', 'bt_1049916_m1', 'bt_1049916_m2', 'bt_4496954_m1', 'bt_4496954_m2', 'bt_3998960_m1', 'bt_3998960_m2', 'bt_1049909_m1', 'bt_1049909_m2', 'bt_1049902_m1', 'bt_1049902_m2']
cargasBTList = findLoad(loadList)
#createGD2("trf167839", cargasBTList,2,limpar=True)#REFAZER PARA O TRANSFORMADOR DO EXEMPLO

overVoltageList = []
rodando = True
multwhile = 1.0

while rodando: #percorre os elementos (getLoads) e adiciona PV nas cargas enquanto sua tensão é < 1.05 pu

    createGD2("trf167839-hc", cargasBTList, 1.5, limpar=True)
    solvetrf(alvo)
    getLoads(alvo)
    overVoltageList = list(chain.from_iterable(overVoltageList))  #novo cargaBTList

    cargasBTList = overVoltageList
    print("Contador OverVoltage: ", contadorOvervoltage)

    if contadorOvervoltage > 200:
        rodando = False

    multwhile += 0.1

print("Número de barras com tensão maior que 1.05 pu: ", contadorOvervoltage)


'''
DSSText.Command = 'Compile ' + mydir + '/trf167839-mult2-pv.dss'
DSSText.Command = 'set mode=snapshot'
DSSText.Command = 'solve'
loadListAPAGAR = getLoads(alvo)
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
