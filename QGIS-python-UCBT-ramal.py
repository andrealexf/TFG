import os

UCBT = 'D:\\py-dss-bdgd2dss\\Cemig-D_4950_2022-12-31_V11_20230920-1643.gdb|layername=UCBT_tab'
#UNTRMT = 'D:\py-dss-bdgd2dss\Cemig-D_4950_2022-12-31_V11_20230920-1643.gdb|layername=UNTRMT
#SSDBT = 'D:\py-dss-bdgd2dss\Cemig-D_4950_2022-12-31_V11_20230920-1643.gdb|layername=SSDBT'

ucbt_table = QgsVectorLayer(UCBT,'UCBT_2022','ogr') #possivel pegar as informações sem adicionar camada
#ucbt_view_table = iface.addVectorLayer(UCBT,'UCBT_2022','ogr')
#untrmt_view_table = iface.addVectorLayer(UNTRMT,'UNTRMT_2022','ogr')
#ssdbt_view_table = iface.addVectorLayer(SSDBT,'SSDBT_2022','ogr')


layer = iface.activeLayer()
filter_expression = "\"CTMT\" = 'IJAU11'"

count = 0
totalZeros = 0
collumnName = 'ENE_'

request = QgsFeatureRequest().setFilterExpression(filter_expression)

path = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS"

if not os.path.exists(path):
    os.makedirs(path)

filename = 'ramal.txt'

def getCat(codigo):
    categorias = {
        "RE1": "Residencial",
        "RE2": "Residencial baixa renda",
        "RE3": "Residencial baixa renda indígena",
        "RE4": "Residencial baixa renda quilombola",
        "RE5": "Residencial baixa renda benefício de prestação continuada da assistência social – BPC",
        "RE6": "Residencial baixa renda multifamiliar",
        "IN": "Industrial",
        "CO1": "Comercial",
        "CO2": "Serviços de transporte, exceto tração elétrica",
        "CO3": "Serviços de comunicações e telecomunicações",
        "CO4": "Associação e entidades filantrópicas",
        "CO5": "Templos religiosos",
        "CO6": "Administração condominial: iluminação e instalações de uso comum",
        "CO7": "Iluminação em rodovias (concessão ou autorização)",
        "CO8": "Semáforos, radares e câmeras de monitoramento de trânsito (concessão ou autorização)",
        "CO9": "Outros serviços e outras atividades",
        "RU1": "Agropecuária rural",
        "RU1A": "Agropecuária rural (poços de captação de água, sem comercialização)",
        "RU1B": "Agropecuária rural (bombeamento de água para irrigação)",
        "RU2": "Agropecuária urbana",
        "RU3": "Residencial rural",
        "RU4": "Cooperativa de eletrificação rural",
        "RU5": "Agroindustrial",
        "RU6": "Serviço público de irrigação rural",
        "RU7": "Escola agrotécnica",
        "RU8": "Aquicultura",
        "PP1": "Poder público federal",
        "PP2": "Poder público estadual ou distrital",
        "PP3": "Poder público municipal",
        "IP": "Iluminação pública",
        "SP1": "Tração elétrica",
        "SP2": "Água, esgoto e saneamento",
        "CPR": "Consumo próprio pela distribuidora",
        "CPRVE": "Consumo próprio pela distribuidora para estação de recarga de veículos elétricos",
        "CSPS": "Concessionária ou Permissionária"
    }
    
    return categorias.get(codigo, "Código não encontrado")

with open(os.path.join(path, filename), 'w') as file:
        file.write("")

for col in ucbt_table.getFeatures(request):
    
    totalEnergy = 0
    zeroCounter = 0
    
    for x in range(12):
        
        x = x+1
        
        if x <= 10:
           
            x = f"{x:02d}"
            
        
        concatName = collumnName + str(x)
        
        if col[concatName] == 0:
            
            zeroCounter += 1
            
        else:
            
            totalEnergy += col[concatName]
        
        
        if zeroCounter == 12:
            
            avgEnergy = 0
            totalZeros += 1
            
        else:
            
            avgEnergy = totalEnergy/(12-zeroCounter)
            
        
    #print(totalEnergy)
    #print(avgEnergy)
    text = ''.join(('Ramal: ', col['RAMAL'],' Média: ',  f'{avgEnergy:.2f}',' Tipo de Carga: ',col['CLAS_SUB'],'/', getCat(col['CLAS_SUB']),'\n'))
    
    print(text)
    
    with open(os.path.join(path, filename), 'a') as file:
        file.write(str(text).strip("'"))
        
    
    count += 1
    '''
    if count >= 3:
        break
    '''
    
print(totalZeros)

zeroPercent = (totalZeros)/count*100
with open(os.path.join(path, filename), 'a') as file:
        file.write(zeroPercent)

