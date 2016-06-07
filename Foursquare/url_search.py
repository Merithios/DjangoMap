from urllib.request import urlopen

import json
#written by Maximilian Langewort

def make_request(url):
    """
    Makes a new HTTP request to the given URL

    :param url: The URL to request
    :returns: JSON response
    """

    #Opens a connection to our Search-URL
    response = urlopen(url)
    #Read the data out of the URL; response_data has the datatype Bytes!
    response_data = response.read()
    #Convert response_data to a string
    r_decoded = response_data.decode("utf-8")
    #Convert the data to a JSON-Format
    data_json = json.loads(r_decoded)
    #Close the connection
    response.close()
    print(data_json)
    #return the data
    return data_json