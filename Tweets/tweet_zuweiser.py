#written by Maximilian Langewort

#Script just connects the OIDs of FB/FS-Pubs with tweets nearby
import json
import pymongo

twitterdb = pymongo.MongoClient().Twitter
FBdb = pymongo.MongoClient().fb
FSdb = pymongo.MongoClient().fs

FB_Pubs = FBdb.Pub3.find()
FS_Pubs = FSdb.Bar.find()

for Pub in FB_Pubs:

    ret=twitterdb.Pubs_search.find_and_modify(query={"coordinates":{
      "$near": {
         "$geometry": {
            "type": "Point" ,
            "coordinates": [ Pub['geo']['coordinates'][0] ,Pub['geo']['coordinates'][1]  ]
         },
         "$maxDistance": 10,
         "$minDistance": 0
    }
    }}, update={"$set": {'FB_id': Pub['_id']}}, upsert=False, full_response= True)
    #FBdb.close()
    #print(ret)

updateTest = twitterdb.Pubs_search.find()
count =0
for entry in updateTest:
    if'FB_id' in entry.keys():
        count = count +1
for Pub in FS_Pubs:

    ret=twitterdb.Pubs_search.find_and_modify(query={"coordinates":{
      "$near": {
         "$geometry": {
            "type": "Point" ,
            "coordinates": [ Pub['location']['lng'] ,Pub['location']['lat']  ]
         },
         "$maxDistance": 10,
         "$minDistance": 0
    }
    }}, update={"$set": {'FS_id': Pub['_id']}}, upsert=False, full_response= True)
    #FSdb.close()
    #print(ret)
count = 0
updateTest = twitterdb.Pubs_search.find()
for entry in updateTest:
    if 'FS_id' in entry.keys():
        count = count + 1
tes=2
#twitterdb.close()