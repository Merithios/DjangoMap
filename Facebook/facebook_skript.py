import facebook
import pymongo
from GeoTransformer import fbTransform
#written by Maximilian Langewort
#keys, Query...

secret = ''
#Get Token from: https://developers.facebook.com/tools/explorer
short_token=''
query="Pub3"
app_id = 1234 # must be integer
app_secret = ''
#token = utils.get_application_access_token(app_id, app_secret)


try:
   #Opening a MongoDB-Connection
   conn = pymongo.MongoClient('localhost', 27017)
   db = conn.fb
   # Get a Facebook-Graph-Object
   graph = facebook.GraphAPI(short_token)
   #long_token = graph.extend_access_token(app_id, app_secret)
   #graph = facebook.GraphAPI (long_token['access_token'])
   #Receiving the data from Facebook through sending the request with the graph
   data = graph.request('search',{'q': query, 'type': 'place', 'center': '60.21817,24.812081', 'distance': '10000', 'limit': '1000'})
   #save the data in the MongoDB in a GeoJSON-Format
   for dataitem in data['data']:
      geotransformed_item = fbTransform(dataitem)
      #db[query].insert(dataitem)
      db[query].insert(geotransformed_item)
except BaseException as e:
   print(e)
   conn.close()
conn.close()

