layer = QgsProject.instance().mapLayersByName("UNTRMTJOIN-AREARURAL")[0]

for feature in layer.getFeatures():
    print(feature['JOINBRR'])