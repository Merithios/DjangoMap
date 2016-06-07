import pymongo
#written by Maximilian Langewort
try:
   conn = pymongo.MongoClient('localhost', 27017)
   facebook = conn.fb
   foursquare = conn.fs

   fs_data=foursquare['Pub'].find()
   fb_data=facebook['Pub'].find()
   # Compares the data from Facebook with the data from Foursquare through the names and the coordinates
   for fs_item in fs_data:
       for fb_item in fb_data:
           if (fs_item['location']['lat'] > (fb_item['location']['latitude']-0.0005) \
                       and fs_item['location']['lat'] < (fb_item['location']['latitude']+0.0005)\
                       and fs_item['location']['lng'] > (fb_item['location']['longitude']-0.0005) \
                       and fs_item['location']['lng'] < (fb_item['location']['longitude'] + 0.0005))\
                       or fb_item['name'] == fs_item['name']:
               print(fb_item['name'])


except BaseException as e:
   print(e)
   conn.close()


conn.close()