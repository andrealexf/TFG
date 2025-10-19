import os

UCBT = 'D:\\py-dss-bdgd2dss\\Cemig-D_4950_2022-12-31_V11_20230920-1643.gdb|layername=UCBT_tab'
#UNTRMT = 'D:\py-dss-bdgd2dss\Cemig-D_4950_2022-12-31_V11_20230920-1643.gdb|layername=UNTRMT'
#SSDBT = 'D:\py-dss-bdgd2dss\Cemig-D_4950_2022-12-31_V11_20230920-1643.gdb|layername=SSDBT'
#SSDMT = 'D:\py-dss-bdgd2dss\Cemig-D_4950_2022-12-31_V11_20230920-1643.gdb|layername=SSDMT'

ucbt_table = QgsVectorLayer(UCBT,'UCBT_2022','ogr')
#untrtm_table = QgsVectorLayer(UNTRMT,'UNTRTM_2022','ogr')




layer = iface.activeLayer()
filter_expression = "\"UNI_TR_MT\" = '167839'"
request = QgsFeatureRequest().setFilterExpression(filter_expression)

count = 0

path = r"C:\Users\Andre\Downloads\TFG\Desenvolvimento-SegundoSemestre\QGIS-OPENDSS"

if not os.path.exists(path):
    os.makedirs(path)

filename = '167839loads.dss'

with open(os.path.join(path, filename), 'w') as file:
        file.write("")

for col in ucbt_table.getFeatures(request):
    
 
    #text = ''.join(('AddBusMarker Bus=', col['PAC_1'],' code=15 color=Red size=4','\n',
                    #'New monitor.PMONITOR', col['COD_ID'] ,' element=transformer.TRF_', col['COD_ID'] , 'A terminal=1 mode=1 ppolar=no','\n','\n'))
    
    text = ''.join(('AddBusMarker Bus=', col['PAC'],' code=15 color=Red size=4','\n'))
     
    print(text)
    
    with open(os.path.join(path, filename), 'a') as file:
        file.write(str(text).strip("'"))
        
    
    count += 1
    '''
    if count >= 3:
        break
    '''
    


