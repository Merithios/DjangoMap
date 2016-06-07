import json
import pymongo
#written by Maximilian Langewort
collectionname = 'Food'



db = pymongo.MongoClient().fs
datadic= db[collectionname].find()
with open('Data.json', 'w') as fp:
    json.dump(datadic, fp)

