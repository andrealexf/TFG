import json
import os
from pathlib import Path

from ODSS_COM_Interface import getLoads, createGD2, findLoad, verboseSolve, DSSCircuit

if __name__ == "__main__":

    diretorio = os.path.dirname(os.path.abspath(__file__))
    brr = os.path.join(diretorio, "brr.json")
    with open(brr, "r", encoding="utf-8") as f:
        brr = json.load(f)

    bairros = {}
    for lista, trafo in brr.items():
        listaTrafo = trafo.split(',')
        bairros[lista] = [int(x) for x in listaTrafo]

    mult = {
        0: 0.41,
        1: 0.43,
        2: 0.23,
        3: 0.25,
        4: 2.0,
        5: 2.0
    }

    for j in range(2):
        cargasBTList = []

        for nomeBairro, transformador in bairros.items():

            for i in range(len(bairros[nomeBairro])):

                contadorOverloads = 0
                print(bairros[nomeBairro][i])
                alvo = ("transformer.TRF_"+str(bairros[nomeBairro][i])+"a").lower()
                #print(alvo)
                loadList,_ = getLoads(alvo,contadorOverloads)
                cargasBTList = findLoad(loadList)
                createGD2(nomeBairro, cargasBTList,mult.get(j), limpar=(i == 0), addpv= True)

        txt = "mult" + str(mult.get(j))
        txtVP = (Path(r"C:\\Users\\Andre\\Downloads\\TFG\\Desenvolvimento-SegundoSemestre\\Resultados\\Verbose") / txt).resolve()
        #print(txtVP)
        datapath = str(txtVP)
        #verboseSolve(datapath)

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