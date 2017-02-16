# Looking up long/lat of zip codes (not required if basemap has that info)
import os
import json
from geopy.geocoders.base import Geocoder
from geopy.geocoders import *
from itertools import cycle

# TODO: better error handling (probably)


class CachingLeechGeocoder(Geocoder):
    ''' I designed this to leach off of the available Geocoder providers and cache all results,
    accessing each geocoder in a round-robin fashion we'll hopefully cache all we need and not
    exceed any of the individual websites' api call limits. '''
    coders = [ArcGIS, DataBC, GoogleV3, GeocoderDotUS, OpenMapQuest,
              NaviData, Nominatim, GeocodeFarm, Yandex, Photon]
    cached = {}
    cache = 'leech_geocoder.json'
    current = cycle(coders)

    def __init__(self, **kwargs):
        Geocoder.__init__(self, **kwargs)
        self.cached = json.load(open(self.cache, 'r')) if os.path.exists(self.cache) else {}

    def geocode(self, query, **kwargs):
        result = self.cached.get(query)
        if not result:
            result = next(self.current)().geocode(query, **kwargs)
            self.cached[query] = result
        return result

    def __del__(self):
        json.dump(self.cached, open(self.cache, 'w'))
        Geocoder.__del__(self)
