# import urllib, urllib2
#
# url = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=995155810e42a128f1b7cf906df3c441&user_id=29267249%40N04&format=json&nojsoncallback=1'
# values = {'isbn' : '9780131185838',
#           'catalogId' : '10001',
#           'schoolStoreId' : '15828',
#           'search' : 'Search' }
#
#
# data = urllib.urlencode(values)
# req = urllib2.Request(url, data)
# response = urllib2.urlopen(req)
# print response.geturl()
# print response.info()
# the_page = response.read()

# import json
# j = json.loads(the_page)
# print j['photos']

import uuid

token = uuid.uuid4().hex

