import os

layer = 'D:\\py-dss-bdgd2dss\\UNTRMTJOINs|layername=UNTRMTJOIN-AREARURAL'
table = QgsVectorLayer(layer,'UNTRTMJOINs','ogr')

for i in range(15):

    count = 0
    def getBRR(brr):
        bairro = {
            "0": "UNTRMTJOIN-AREARURAL",
            "1": "UNTRMTJOIN-AVENIDA",
            "2": "UNTRMTJOIN-BOAVISTA",
            "3": "UNTRMTJOIN-BPS",
            "4": "UNTRMTJOIN-CENTRO",
            "5": "UNTRMTJOIN-CRUZEIRO",
            "6": "UNTRMTJOIN-ESTIVA",
            "7": "UNTRMTJOIN-MORROCHIC",
            "8": "UNTRMTJOIN-NOSSASENHORADAAGONIA",
            "9": "UNTRMTJOIN-PINHEIRINHO",
            "10": "UNTRMTJOIN-SANTOANTONIO",
            "11": "UNTRMTJOIN-SAOVICENTE",
            "12": "UNTRMTJOIN-UNIFEI",
            "13": "UNTRMTJOIN-VILAISABEL",
            "14": "UNTRMTJOIN-VILARUBENS"
        }
    
        return bairro.get(brr, "Bairro não encontrado")
    
    '''
    name = "UNTRMTJOINs — "+getBRR(str(i))
    layer = QgsProject.instance().mapLayersByName(name)[0]
    '''
    
    layer = 'D:\\py-dss-bdgd2dss\\UNTRMTJOINs|layername='+getBRR(str(i))
    table = QgsVectorLayer(layer,'UNTRTMJOINs','ogr')
    
    for feat in table.getFeatures():
    
        print(feat['JOINBRR'])
    
    
        count += 1
    
        if count >= 3:
            break
    
