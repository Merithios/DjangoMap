import pymongo
import GeoTransformer
#written by Maximilian Langewort

try:
   conn = pymongo.MongoClient('localhost', 27017)
   db = conn.test
   dictionary = db.Eszter_Daten.find()
   i=0
   # For a Feature-Collection
   #Diclist = []

   for item in dictionary:
       if item['location']['type'] == 'Point':
            d = GeoTransformer.dynamicDicTransform(item)
            db.Daten_GeoJ.insert(d)
            #For a Feature-Collection
            #Diclist.append(GeoTransformer.dynamicDicTransform(item))
       else:
           print('no point')






except BaseException as e:
    print(e)
    conn.close()
conn.close()