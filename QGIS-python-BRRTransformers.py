import os

path = r'C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS\IJAU11'
layer = 'D:\\py-dss-bdgd2dss\\UNTRMTJOINs|layername=UNTRMTJOIN-AREARURAL'
table = QgsVectorLayer(layer,'UNTRTMJOINs','ogr')

filename=''

def createFile(name, tab):

    if not os.path.exists(path):
        os.makedirs(path)

    filename = 'BRR_'+name+'.dss'
    print(filename)

    with open(os.path.join(path, filename), 'w') as file:
        file.write("")
    
    
    count = 0
    print(path)
    print(filename)
    
    vist = set()
    
    for feat in tab.getFeatures():
        
        pac2 = feat['PAC_2']
        
        if pac2 in vist:
            continue 
        
        vist.add(pac2)
    
        text = ''.join(('AddBusMarker Bus=', pac2,' code=15 color=Red size=4','\n',
                        'New monitor.PMONITOR', str(f"{feat['COD_ID']:.0f}") ,' element=transformer.TRF_',
                        str(f"{feat['COD_ID']:.0f}") , 'A terminal=1 mode=1 ppolar=no','\n','\n'))
        print(text)
        with open(os.path.join(path, filename), 'a') as file:
            file.write(str(text).strip("'"))
    
        count += 1
        '''
        if count >= 3:
            break
        '''

def getBRR(brr):
        bairro = {
            "0": "AREARURAL",
            "1": "AVENIDA",
            "2": "BOAVISTA",
            "3": "BPS",
            "4": "CENTRO",
            "5": "CRUZEIRO",
            "6": "ESTIVA",
            "7": "MORROCHIC",
            "8": "NOSSASENHORADAAGONIA",
            "9": "PINHEIRINHO",
            "10": "SANTOANTONIO",
            "11": "SAOVICENTE",
            "12": "UNIFEI",
            "13": "VILAISABEL",
            "14": "VILARUBENS"
        }
    
        return bairro.get(brr, "Bairro não encontrado")

for i in range(1):

    layer = 'D:\\py-dss-bdgd2dss\\UNTRMTJOINs|layername=UNTRMTJOIN-'+getBRR(str(i))
    table = QgsVectorLayer(layer,'UNTRTMJOINs','ogr')
    createFile(getBRR(str(i)), table)
   