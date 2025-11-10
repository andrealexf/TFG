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


diretorio = os.path.dirname(os.path.abspath(__file__))
arquivoBT = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS\IJAU11\CargasBT_DU01_2022124950_IJAU11_--MBS-1--T--.dss"
#arquivoBT = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS\circuitoexemplo.dss" #circuito exemplo
arquivoLS = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS\IJAU11\CurvaCarga_2022124950_IJAU11_--MBS-1--T--.dss"

pv_dir = Path('C://Users//Andre//Downloads//TFG//Desenvolvimento-SegundoSemestre//BRR-PVSyst')

#para o arquivo exemplo:

#os.chdir('C://Users//Andre//Downloads//TFG//Desenvolvimento-SegundoSemestre//QGIS-OPENDSS')
#mydir = os.getcwd()
#DSSText.Command = 'Compile ' + mydir + '/circuitoexemplo.dss'
#arquivoBT = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS\circuitoexemplo.dss"

# --------------------------------------

def norm(b):
    return (b or "").split(".", 1)[0].lower()

def getLoads(transformer, contadorOvervoltage):
    defineBranchName(transformer)
    print(DSSTopology.BranchName)

    global bus1
    global bus2

    loadList = []
    overVoltageList = []
    DSSTopology.ForwardBranch

    while DSSTopology.BranchName != '' and DSSTopology.BranchName.split(".")[0] != "Transformer" and ((DSSTopology.BranchName.split(".", 1)[1]).split("_", 1)[0])[:3] != "smt":  # enquanto line não for smt...

        bus1 = DSSCktElement.BusNames[0]
        bus2 = DSSCktElement.BusNames[1]
        print("")
        voltageBus(bus1,None,contadorOvervoltage)

        if busLoads(bus2):

            m1m2 = busLoads(bus2)
            #print(" ", m1m2) #envia como bus2 mas carga só possui uma bus (na função está como bus1)

            if (m1m2[0].split("_", 1)[1])[:2] != "ip":
                #print(" ", m1m2)
                loadList.append(m1m2)

                load = m1m2[0]
                #voltageBus(bus2, load)

                if voltageBus(bus2, load, contadorOvervoltage):
                    overVoltageList.append(m1m2)


        ramal = DSSTopology.BranchName
        DSSTopology.ForwardBranch

    loadList = list(chain.from_iterable(loadList))
    overVoltageList = list(chain.from_iterable(overVoltageList))
    defineBranchName(ramal)
    print("")
    print("Número de cargas no transformador (excluindo iluminação):", len(loadList), loadList)
    print("OverloadsList:", len(overVoltageList), overVoltageList)
    print("")

    return loadList, overVoltageList

def createGD2(nomeBairro, loadList: list[cargaBT], mult: float = 1.0, limpar: bool = False, addpv = None):

    if addpv:
        txt = nomeBairro + "-mult" + str(mult) + "-pv.dss"

    else:
        txt =  nomeBairro + "-pv.dss"

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

def voltageBus(bus1, load=None, contadorOvervoltage=None):

    if load is not None:  # para cargas

        DSSCircuit.SetActiveElement("Load." + load)
        print("     Carga: ",DSSCircuit.ActiveCktElement.Name)
        pu = DSSCircuit.ActiveBus.puVmagAngle
        pu_round = tupleFormat(pu, casas=4)
        print("     (p.u., ang): ", pu_round)

        if overvoltage(pu_round, contadorOvervoltage):

            return True

    else: #linhas e transformadores

        DSSCircuit.SetActiveBus(bus1)
        print("Linha: ", DSSCircuit.ActiveCktElement.Name)
        pu = DSSCircuit.ActiveBus.puVmagAngle
        pu_round = tupleFormat(pu, casas=4)
        print("(p.u., ang): ", pu_round)
        overvoltage(pu_round, contadorOvervoltage)

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

            for load in loadlist:
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

def overvoltage(tupla, contadorOvervoltage: int):

    if any(valor > 1.05 for valor in tupla[::2]):

        print("Valor maior que 1.045")
        contadorOvervoltage = contador(contadorOvervoltage)
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
    txt = "'" + alvo + "-pv.dss'"

    DSSText.Command = 'clear'
    DSSText.Command = 'Compile ' + mydir + '/Master_DU01_2022124950_IJAU11_--MBS-1--T--.dss'
    DSSText.Command = 'set datapath="C:\\Users\\Andre\\Downloads\\TFG\\Desenvolvimento-SegundoSemestre\\BRR-PVSyst"'
    DSSText.Command = 'redirect '+ txt

    DSSText.Command = 'set datapath="C:\\Users\\Andre\\Downloads\\TFG\\Desenvolvimento-SegundoSemestre\\QGIS-OPENDSS\\IJAU11"'
    DSSText.Command = 'set mode=daily'
    DSSText.Command = 'set stepsize = 0.25h'
    DSSText.Command = 'solve number=52'

def contador(contador: int):

    contador += 1
    return contador

def removePV(overvoltageList: list, transformer: str):
    filename = transformer + "-hc-pv.dss"
    padrao = re.compile(r'PVsystem\.GD\.\s*([^"\s]+)', re.IGNORECASE)
    arquivoHC = pv_dir / filename
    novoHC = "novo-" + filename + ".temp"

    # newline="" ao ler e escrever ajuda a não duplicar/quebrar quebras de linha
    with open(arquivoHC, "r", encoding="utf-8", newline="") as fin, \
         open(novoHC, "w", encoding="utf-8", newline="") as fout:

        pula = 0
        prev_blank = False  #ultima linha em branco?

        for linha in fin:

            if linha.endswith("\r\n"):
                linha = linha[:-2] + "\n"

            m = padrao.search(linha)

            if m:
                alvo = m.group(1).upper()
                for cargaOver in overvoltageList:
                    if alvo == str(cargaOver).upper():
                        pula = 3
                        break

            if pula > 0:
                pula -= 1
                prev_blank = False
                continue

            is_blank = (linha.strip() == "")
            if not is_blank:
                fout.write(linha)
                prev_blank = False

            else:

                if not prev_blank:
                    fout.write(linha)
                    prev_blank = True

    os.replace(novoHC, arquivoHC)

