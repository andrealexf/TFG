from collections import Counter
import os
from ODSS_COM_Interface import getLoads, solvetrf, createGD2, findLoad, DSSCircuit, removePV

if __name__ == "__main__":

    contadorOvervoltage = 0
    overVoltageList = []
    multwhile = 0.41
    '''
    carga = 'carga.txt'

    with open(carga, "r", encoding="utf-8") as f:

        for linha in f:
            print(linha)

    '''
    alvo = "Transformer.trf_167839a".lower()
    alvotrim = (alvo.split(".")[1]).split("a")[0]
    trf_hc = alvotrim + "-hc"

    loadList = ['bt_11266978_m1', 'bt_11266978_m2', 'bt_1050133_m1', 'bt_1050133_m2', 'bt_1050126_m1', 'bt_1050126_m2','bt_1050112_m1', 'bt_1050112_m2', 'bt_10406755_m1', 'bt_10406755_m2', 'bt_1050105_m1', 'bt_1050105_m2','bt_1050098_m1', 'bt_1050098_m2', 'bt_1050091_m1', 'bt_1050091_m2', 'bt_1050077_m1', 'bt_1050077_m2','bt_4892503_m1', 'bt_4892503_m2', 'bt_1050070_m1', 'bt_1050070_m2', 'bt_1050056_m1', 'bt_1050056_m2','bt_1050049_m1', 'bt_1050049_m2', 'bt_1050063_m1', 'bt_1050063_m2', 'bt_3640476_m1', 'bt_3640476_m2','bt_1050084_m1', 'bt_1050084_m2', 'bt_3885504_m1', 'bt_3885504_m2', 'bt_1050042_m1', 'bt_1050042_m2','bt_1050035_m1', 'bt_1050035_m2', 'bt_1050028_m1', 'bt_1050028_m2', 'bt_1050021_m1', 'bt_1050021_m2','bt_1050014_m1', 'bt_1050014_m2', 'bt_1050007_m1', 'bt_1050007_m2', 'bt_1050000_m1', 'bt_1050000_m2','bt_4301661_m1', 'bt_4301661_m2', 'bt_4127207_m1', 'bt_4127207_m2', 'bt_1049993_m1', 'bt_1049993_m2','bt_1049986_m1', 'bt_1049986_m2', 'bt_1049979_m1', 'bt_1049979_m2', 'bt_1049972_m1', 'bt_1049972_m2','bt_11382069_m1', 'bt_11382069_m2', 'bt_10214815_m1', 'bt_10214815_m2', 'bt_1049965_m1','bt_1049965_m2','bt_1049958_m1', 'bt_1049958_m2', 'bt_1049951_m1', 'bt_1049951_m2', 'bt_1049937_m1', 'bt_1049937_m2','bt_1049930_m1', 'bt_1049930_m2', 'bt_1049923_m1', 'bt_1049923_m2', 'bt_1049916_m1', 'bt_1049916_m2','bt_4496954_m1', 'bt_4496954_m2', 'bt_3998960_m1', 'bt_3998960_m2', 'bt_1049909_m1', 'bt_1049909_m2','bt_1049902_m1', 'bt_1049902_m2']
    '''
    loadList,_ = getLoads(alvo, contadorOvervoltage)
    #while len(overVoltageList) != len(loadList):  # percorre os elementos (getLoads) e adiciona PV nas cargas enquanto sua tensão é < 1.05 pu
    '''


    while multwhile <= 0.45:

        if overVoltageList:
            cloadList = Counter(loadList)
            coverVoltage = Counter(overVoltageList)
            cfinal = cloadList - coverVoltage
            cfinal = list(cfinal.elements())

            print("Adicionadas: ", cfinal)
            print("")

            removePV(cfinal,alvotrim) #remove o pv das cargas que não possuem overvoltages
            cargasBTList = findLoad(cfinal) #manda a lista de cargas que não possuem overvoltage para adicionar pv
            createGD2(trf_hc, cargasBTList, multwhile, limpar=False)

        else:
            cargasBTList = findLoad(loadList)
            createGD2(trf_hc, cargasBTList, multwhile, limpar=True)

        solvetrf(trf_hc)
        loadList, overVoltageList = getLoads(alvo, contadorOvervoltage)

        multwhile += 0.01


    kW_BC = DSSCircuit.TotalPower[0]  # in kW
    kvar_BC = DSSCircuit.TotalPower[1]  # in kVAr
    kW_Loss_BC = DSSCircuit.Losses[0] / 1000  # property returns values in W, here stored in kW
    kvar_Loss_BC = DSSCircuit.Losses[1] / 1000  # property returns values in VAr, here stored in kVAr

    print('')
    print("----------")
    print("Total kW delivered to the network: %.3f kW" % kW_BC)
    print("Total kVAr delivered to the network: %.3f kvar" % kvar_BC)
    print("Total active losses: %.3f kW" % kW_Loss_BC)
    print("Percent losses: %.3f" % abs(((kW_Loss_BC / kW_BC) * 100)) + "%")
    print("Total reactive losses: %.3f kVAr" % kvar_Loss_BC)
    print("----------")

    print('fim')
