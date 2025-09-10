import os

path = r'C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS\IJAU11'
layer = 'D:\\py-dss-bdgd2dss\\UNTRMTJOINs|layername=UNTRMTJOIN-AREARURAL'
table = QgsVectorLayer(layer,'UNTRTMJOINs','ogr')

untrmtLayer = 'D:\\py-dss-bdgd2dss\\Cemig-D_4950_2022-12-31_V11_20230920-1643.gdb|layername=UNTRMT'
untrmtTable = QgsVectorLayer(untrmtLayer,'UNTRTM','ogr')

filter_expression = "\"CTMT\" = 'IJAU11'"
request = QgsFeatureRequest().setFilterExpression(filter_expression)

filename=''

def createFile(name, brr, tr):

    if not os.path.exists(path):
        os.makedirs(path)

    filename = 'BRR_'+name+'.dss'
    print(filename)

    with open(os.path.join(path, filename), 'w') as file:
        file.write("")
        
    #count = 0
    transformerCount = 0
    print(path)
    print(filename)
    
    codIdBRR = {str(f"{feat['COD_ID']:.0f}") for feat in brr.getFeatures()} #guarda os COD_ID da tabela de bairro
    #print(codIdBRR)

    for feat in tr.getFeatures(request):
    
        if feat['COD_ID'] in codIdBRR:
            
            transformerCount += 1
           
            text = ''.join(('AddBusMarker Bus=', feat['PAC_1'],' code=15 color=Red size=4 !buses=[',feat['PAC_1'],' ', 
                            feat['PAC_2'],']' ,'\n',
                            'New monitor.PMONITOR', feat['COD_ID'] ,' element=transformer.TRF_',
                            feat['COD_ID'] , 'A terminal=1 mode=1 ppolar=no','\n','\n'))

            
            with open(os.path.join(path, filename), 'a') as file:
                file.write(str(text).strip("'"))
                
                
                
    with open(os.path.join(path, filename), 'a') as file:
        file.write('\n')
        file.write('!Numero de transformadores no bairro: '+str(transformerCount))
    
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

for i in range(14):

    layer = 'D:\\py-dss-bdgd2dss\\UNTRMTJOINs|layername=UNTRMTJOIN-'+getBRR(str(i))
    table = QgsVectorLayer(layer,'UNTRTMJOINs','ogr')
    createFile(getBRR(str(i)), table, untrmtTable)
   