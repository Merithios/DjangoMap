from url_search import make_request
import time
import pymongo
#written by Maximilian langewort

def search(lat, lng, distance, query):
    """
    Searches the Foursquare API (Max Limit = 50)

    :param lat: Latitude of the request
    :param lng: Longitude of the request
    :param distance: Distance to search (meters)
    :returns: List of retrieved venues
    """

    #Building the Search-URL for our request
    url= 'https://api.foursquare.com/v2/venues/explore?ll='
    url+= str(lat) + ','
    url+= str(lng) + '&radius='
    url+= str(distance) + '&limit=500&client_id=10TDZPZ0W5SXPGLAO305X4RS5FCECNTCYZZI4T3MVEG1DLLY&client_secret=DVPP4K3SCLXH2LZSAF1NJXRREBIN2XGWAECPXXTA00UG03JL&v='
    url+= time.strftime("%Y%m%d") + '&query='
    url+= query

    #url= 'https://api.foursquare.com/v2/venues/explore?ll=60.22,24.81&radius=5000&limit=500&client_id=10TDZPZ0W5SXPGLAO305X4RS5FCECNTCYZZI4T3MVEG1DLLY&client_secret=DVPP4K3SCLXH2LZSAF1NJXRREBIN2XGWAECPXXTA00UG03JL&v=20160406&id=4d4b7105d754a06374d81259'
    #url = 'https://api.foursquare.com/v2/venues/explore?ll=51.54,9.91&radius=100000&limit=500&client_id=10TDZPZ0W5SXPGLAO305X4RS5FCECNTCYZZI4T3MVEG1DLLY&client_secret=DVPP4K3SCLXH2LZSAF1NJXRREBIN2XGWAECPXXTA00UG03JL&v=20160406&id=4d4b7105d754a06374d81259'


    try:

        # Getting the Data from Foursquare
        data = make_request(url)
        #Opening MongoDB-Connection
        conn=pymongo.MongoClient('localhost', 27017)
        #Taking the Database "fs" (Foursquare)
        db=conn.fs
        #Going along the data-tree to the valuable entries
        for item in data['response']['groups']:
            #Going through all hits
            for dataitem in item['items']:
                #venue has all the relevant data of one hit
                 venue = dataitem['venue']
                 #loc is just to clarify the next Statement
                 loc = venue["location"]
                 #Check if the Entry allready exists. Parameters are the Name and a small area around the original data for errors in the measurement
                 #ToDo: Doing everything in an insert + upsert statement
                 exist =db[query].find({"$and":[{"location.lat": {'$gt': loc["lat"]-0.001}},{"location.lng": {'$lt': loc["lng"]+0.001}},{"name":venue["name"]}]})
                 #If the place isn't in the database, it will be added
                 if exist.count() is 0:

                     l= [loc['lng'], loc['lat']]

                     db[query].insert(venue)
                     #db[query+'_koords'].insert({"geometry": {"type":"Point", "coordinates":[loc["lng"],loc["lat"]]}})

                     #db[query + 'points'].insert(p)
    #Check for Errors
    #ToDo: More explicit recognition of errors
    except BaseException as e:
        print(e)
        conn.close()
    #close the connection to the database
    conn.close()
    return
