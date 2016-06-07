#written by Maximilian langewort

# Transforms a Feature-List into a Feature-Collection
def finalTransform(Diclist):
    FinalDic = {'type': 'FeatureCollection', 'features': Diclist}
    return FinalDic
#Transforms Dictionarys with a structure like dictionary-->location--coordinates-->[coord1, coord2] into a GeoJSON-Dictionary
def dynamicDicTransform(untransformedDic):
    #Check for Point-Data
    if untransformedDic['location']['type'] == 'Point':
        #create a new dic in GeoJSON with the coordinates from the original dic
        GeoDic = {'type': 'Feature', \
                'geometry': {'type': 'Point', \
                           'coordinates': [untransformedDic['location']['coordinates'][0], untransformedDic['location']['coordinates'][1]]}}
        #remove the ccordinates from the old dic
        del untransformedDic['location']
        #add the old dic as "properties" to the GeoJSON-Dic
        GeoDic.update({'properties': untransformedDic})

    return GeoDic


def fbTransform(FBDic):

    #FBDic.update({'geometry': {'type': 'Point', 'coordinates': [FBDic['location']['latitude'], FBDic['location']['longitude']]}})
    #create a new dic in GeoJSON with the coordinates from the original dic
    GeoDic = {'type': 'Feature',\
              'geometry': {'type': 'Point',\
              'coordinates': [FBDic['location']['latitude'], FBDic['location']['longitude']]}}
    # remove the ccordinates from the old dic
    del FBDic['location']['longitude']
    del FBDic['location']['latitude']
    # add the old dic as "properties" to the GeoJSON-Dic
    GeoDic.update({'properties':FBDic})

    return GeoDic

def fsTransform(FSDic):
    # create a new dic in GeoJSON with the coordinates from the original dic
    GeoDic = {'type': 'Feature', \
              'geometry': {'type': 'Point', \
                           'coordinates': [FSDic['location']['lat'], FSDic['location']['lng']]}}
    # remove the ccordinates from the old dic
    del FSDic['location']['lng']
    del FSDic['location']['lat']
    # add the old dic as "properties" to the GeoJSON-Dic
    GeoDic.update({'properties': FSDic})
    return GeoDic