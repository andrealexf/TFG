import os

UCBT = 'D:\\py-dss-bdgd2dss\\Cemig-D_4950_2022-12-31_V11_20230920-1643.gdb|layername=UCBT_tab'
UNTRMT = 'D:\\py-dss-bdgd2dss\\Cemig-D_4950_2022-12-31_V11_20230920-1643.gdb|layername=UNTRMT'

ucbt_table = QgsVectorLayer(UCBT,'UCBT_2022','ogr')
untrmt_table = QgsVectorLayer(UNTRMT,'UNTRMT_2022','ogr') 

filter_expression = "\"CTMT\" = 'IJAU11'"

request = QgsFeatureRequest().setFilterExpression(filter_expression)

path = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS"

if not os.path.exists(path):
    os.makedirs(path)

filename = 'brr.json'

with open(os.path.join(path, filename), 'w') as file:
        file.write("{")
        

avenida = set()
arearural = set() 
areaurbana = set() 
boavista = set()
bps = set()
chacaradasmocas = set()
cruzeiro = set()
centro = set() 
estiva = set()
jardimamerica = set()
medicina = set()
moradadosol = set()
morrogrande = set() 
morrochic = set()
nossasenhoradaagonia = set()
pinheirinho = set()
riomanso = set() 
santaluzia = set()
santoantonio = set()
saovicente = set()
santarosa = set()
vilapoddis = set() 
vilarubens = set() 
vilaisabel = set()
varginha= set()
vilabetel = set()

processados = set()
lista1 = set()
lista2 = set()

bairros = {
    "AVENIDA": set(),
    "BOA VISTA": set(),
    "SANTA LUZIA": set(),
    "CHACARA DAS MOCAS": set(),
    "CRUZEIRO": set(),
    "PINHEIRINHO": set(),
    "VILA PODDIS": set(),
    "MORADA DO SOL": set(),
    "AREA RURAL": set(),
    "VILA RUBENS": set(),
    "SANTO ANTONIO": set(),
    "AREA URBANA": set(),
    "VILA ISABEL": set(),
    "ESTIVA": set(),
    "CENTRO": set(),
    "MORRO GRANDE": set(),
    "NOSSA SENHORA DA AGONIA": set(),
    "MORRO CHIC": set(),
    "RIO MANSO": set(),
    "BPS": set(),
    "VARGINHA": set(),
    "JARDIM AMERICA": set(),
    "SAO VICENTE": set(),
    "MEDICINA": set(),
    "SANTA ROSA": set(),
    "VILA BETEL": set()
}

def addTR(brr, tr):
    
    if tr in processados:
        return
        
    if brr in bairros:
        bairros[brr].add(tr)
        processados.add(tr)


count = 0
distTR = set()
distBRR = set()

for coll in untrmt_table.getFeatures(request):
    
    lista1.add(coll['COD_ID'])

for col in ucbt_table.getFeatures(request):
    
    
    addTR(col['BRR'],col['UNI_TR_MT'])
    lista2.add(col['UNI_TR_MT'])

    count += 1
    '''
    if count >= 50:
        break
    '''

trNumber = 0
faltantes = lista1 - lista2

for nome, conjunto in bairros.items():
    print(nome, ":", len(conjunto), "itens")
    trNumber += len(conjunto)

print("")
print("Número de transformadores: ",trNumber)
print("")
print("Itens faltantes:", faltantes)

avenida = ",".join(list(bairros["AVENIDA"]))
boavista = ",".join(list(bairros["BOA VISTA"]))
chacaradasmocas = ",".join(list(bairros["CHACARA DAS MOCAS"]))
cruzeiro = ",".join(list(bairros["CRUZEIRO"]))
pinheirinho = ",".join(list(bairros["PINHEIRINHO"]))
vilapoddis = ",".join(list(bairros["VILA PODDIS"]))
arearural = ",".join(list(bairros["AREA RURAL"]))
vilarubens = ",".join(list(bairros["VILA RUBENS"]))
vilaisabel = ",".join(list(bairros["VILA ISABEL"]))
centro = ",".join(list(bairros["CENTRO"]))
morrochic = ",".join(list(bairros["MORRO CHIC"]))
bps = ",".join(list(bairros["BPS"]))
varginha = ",".join(list(bairros["VARGINHA"]))
jardimamerica = ",".join(list(bairros["JARDIM AMERICA"]))
santarosa = ",".join(list(bairros["SANTA ROSA"]))
falt = ",".join(list(faltantes))

text = ''.join(('\n','        "avenida":',avenida,'\n'
                ,'        "boavista":',boavista,'\n'
                ,'        "chacaradasmocas":',chacaradasmocas,'\n'
                ,'        "cruzeiro":',cruzeiro,'\n'
                ,'        "pinheirinho":',pinheirinho,'\n'
                ,'        "vilapoddis":',vilapoddis,'\n'
                ,'        "arearural":',arearural,'\n'
                ,'        "vilarubens":',vilarubens,'\n'
                ,'        "vilaisabel":',vilaisabel,'\n'
                ,'        "centro":',centro,'\n'
                ,'        "morrochic":',morrochic,'\n'
                ,'        "bps":',bps,'\n'
                ,'        "varginha":',varginha,'\n'
                ,'        "jardimamerica":',jardimamerica,'\n'
                ,'        "santarosa":',santarosa,'\n'
                ,'        "faltantes":',falt,'\n',
                '}'))



with open(os.path.join(path, filename), 'a') as file:
        file.write(text)

