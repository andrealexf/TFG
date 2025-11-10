import re
import os


path = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\BRR-PVSyst"

padrao = re.compile(r'.*?pmpp\s*=([^ ]+)', re.IGNORECASE)
bairros = ["arearural","avenida","boavista","bps","centro","chacaradasmocas","cruzeiro","jardimamerica","morrochic","pinheirinho","santarosa","varginha","vilaisabel","vilapoddis","vilarubens"]

nome_arquivo = "pmppcertos.txt"
diretorio = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(diretorio, nome_arquivo)


#ler 1 arquivo
pmpplist = []
arc = path + rf"\trf_167839-hc-pv.dss"
with open(arc, "r", encoding="utf-8") as f:
    for last, linha in enumerate(f, start=1):
        m = padrao.search(linha)

        if not m:
            continue

        pmppencontrado = m.group(1).strip()
        # print(pmppencontrado)
        pmpplist.append(float(pmppencontrado))
        pass

print(sum(pmpplist))



'''
with open(arquivo, "w", encoding="utf-8") as f:
    f.write('')

pmpptotal1 = []
pmpptotal2 = []

for i in range(2*len(bairros)):

    nomebairro = str(bairros[int(i/2)])
    #arc = path + rf"\{nomebairro}-mult1.0-pv.dss"

    pmpplist = []

    if i%2 == 0:
        arc = path + rf"\{nomebairro}-mult1.0-pv.dss"

    else:
        arc = path + rf"\{nomebairro}-pv.dss"

    with open(arc, "r", encoding="utf-8") as f:
        for last, linha in enumerate(f, start=1):
            m = padrao.search(linha)

            if not m:
                continue

            pmppencontrado = m.group(1).strip()
            # print(pmppencontrado)
            pmpplist.append(float(pmppencontrado))
            pass

    print("")


    if i%2 == 0:
        txt = ('\n' +nomebairro + '\n' + "     - pmpptotal1 = " + str(f'{sum(pmpplist):.2f}') + " número de unidades = " + str((int(last / 3)))+ '\n')
        pmpptotal1.append(sum(pmpplist))

    else:
        txt = ("     - pmpptotal2 = " + str(f'{sum(pmpplist):.2f}') + " número de unidades = " + str((int(last / 3)))+ '\n')
        pmpptotal2.append(sum(pmpplist))

    with open(arquivo, "a", encoding="utf-8") as f:
        f.write(txt)


re1 = '\n' + "pmppptotaltotal1 = " + str(sum(pmpptotal1))
re2 = '\n' + "pmppptotaltotal2 = " + str(sum(pmpptotal2))

with open(arquivo, "a", encoding="utf-8") as f:
    f.write("")
    f.write(str(re1))
    f.write(str(re2))


pmpptotal = []
for i in range(len(bairros)):

    nomebairro = str(bairros[i])
    arc = path + rf"\{nomebairro}-mult0.1-pv.dss"
    pmpplist = []

    with open(arc, "r", encoding="utf-8") as f:
        for last, linha in enumerate(f, start=1):
            m = padrao.search(linha)

            if not m:
                continue

            pmppencontrado = m.group(1).strip()
            # print(pmppencontrado)
            pmpplist.append(float(pmppencontrado))
            pass

    print(nomebairro,"soma pmpp = ",round(sum(pmpplist),2))
    pmpptotal.append(sum(pmpplist))

print("Total: ", round(sum(pmpptotal),2))
print("Porcenagem: ", round(sum(pmpptotal)*100/6582.13,2))
'''