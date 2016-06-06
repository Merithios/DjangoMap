#Disclaimer: THE SAMPLE CODE ON https://github.com/Merithios IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL PAGERDUTY OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) SUSTAINED BY YOU OR A THIRD PARTY, HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT ARISING IN ANY WAY OUT OF THE USE OF THIS SAMPLE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#written by Maximilian Langewort

from django.shortcuts import render
import pymongo
import json
from bson import json_util
# Create your views here.
def mapping(request):
    #Connecting to MongoDB
    db_tw = pymongo.MongoClient().Twitter
    db_fb = pymongo.MongoClient().fb
    #Getting Variables from the Html/Javascript
    html_dic = request.GET

    # Intersect-Button got clicked
    if len(html_dic.keys()) > 1 and html_dic['transactionType'] == 'intersect':

        #Transform the format of the received Object, that it can be used by Python/MongoDB
        geoJ = request.GET["geoJson_Data"].replace('\'','\"')
        geoJ = '['+geoJ+']'
        #transforms the Data-String to a dictionary
        testdic= json.loads(geoJ)
        #Get the matching data from the databases: line 1 check if exists, line 2 intersect the Db-Data with line 3 received Data from Html/JS, line 4 only return coordinates
        #  \ is for continuing a statement in a new line in Python, so it's not part of the MongoDB-Statement
        Data_ptr_tw = db_tw.TwitterPubs.find({'coordinates.coordinates': {'$exists': 'true'}, \
                                          'coordinates.coordinates': {'$geoIntersects': \
                                                                          {'$geometry': testdic[0]['geometry']}}}, \
                                         {'coordinates.coordinates': 1, '_id': 0})

        Data_ptr_fb = db_fb.FacebookPubs.find({'geo.coordinates': {'$exists': 'true'}, \
                                       'geo.coordinates': {'$geoIntersects': \
                                                               {'$geometry': testdic[0]['geometry']}}}, \
                                      {'geo.coordinates': 1, '_id': 0})
    #Near-button clicked
    elif len(html_dic.keys()) > 1 and html_dic['transactionType'] == 'near':
        # Transform the format of the received Object, that it can be used by Python/MongoDB
        geoJ = request.GET["geoJson_Data"].replace('\'', '\"')
        geoJ = '[' + geoJ + ']'
        limit = request.GET["limit"]
        minDis = request.GET["minDis"]
        maxDis = request.GET["maxDis"]
        # transforms the Data-String to a dictionary
        testdic = json.loads(geoJ)
        # maxDis of 0 would not bring a solution, so check and adjust the statement
        #  \ is for continuing a statement in a new line in Python, so it's not part of the MongoDB-Statement
        if maxDis != '0':
            Data_ptr_tw = db_tw.TwitterPubs.find({'coordinates.coordinates': {'$exists': 'true'}, \
                                              'coordinates': {'$near': \
                                              {'$geometry': testdic[0]['geometry'],'$minDistance': float(minDis), \
                                               '$maxDistance': float(maxDis)}}}, \
                                                 {'coordinates.coordinates': 1, '_id': 0}).limit(int(limit))

            Data_ptr_fb = db_fb.FacebookPubs.find({'geo.coordinates': {'$exists': 'true'}, \
                                          'geo': {'$near': \
                                          {'$geometry': testdic[0]['geometry'],
                                          '$minDistance': float(minDis), '$maxDistance': float(maxDis)}}}, \
                                         {'geo.coordinates': 1, '_id': 0}).limit(int(limit))
        else:

            Data_ptr_tw = db_tw.TwitterPubs.find({'coordinates.coordinates': {'$exists': 'true'}, \
                                                  'coordinates': {'$near': \
                                                  {'$geometry': testdic[0]['geometry'],
                                                  '$minDistance': float(minDis)}}}, \
                                                 {'coordinates.coordinates': 1, '_id': 0}).limit(int(limit))


            Data_ptr_fb = db_fb.FacebookPubs.find({'geo.coordinates': {'$exists': 'true'}, \
                                   'geo': {'$near': \
                                               {'$geometry': testdic[0]['geometry'],
                                                '$minDistance': float(minDis)}}}, \
                                  {'geo.coordinates': 1, '_id': 0}).limit(int(limit))
    else:

        #Reading the Data out of the MongoDB without a Button clicked
        Data_ptr_tw = db_tw.TwitterPubs.find({'coordinates.coordinates': { '$exists': 'true'}}, {'coordinates.coordinates': 1, '_id': 0})
        Data_ptr_fb = db_fb.FacebookPubs.find({}, {'geo.coordinates': 1, '_id': 0})

    docs_tw = []
    #Transformation of the single documents to a JSON-List
    for doc in Data_ptr_tw:
        doc_j = json.dumps(doc, default=json_util.default)
        docs_tw.append(doc_j)

    docs_fb =[]
    for doc in Data_ptr_fb:
            doc_j = json.dumps(doc, default=json_util.default)
            docs_fb.append(doc_j)


# Shows the header.html and sends the JSON-List as 'mdb_data'
    return render(request, 'mapsite/header.html', {'mdb_Data': docs_tw, 'mdb_Data_2': docs_fb})



