# Looking up long/lat of zip codes (not required if basemap has that info)
import os
import pickle
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
    cache = 'leech_geocoder.pickle'
    current = cycle(coders)

    def __init__(self, **kwargs):
        Geocoder.__init__(self, **kwargs)
        self.cached = pickle.load(open(self.cache, 'rb')) if os.path.exists(self.cache) else {}

    def geocode(self, query, **kwargs):
        result = self.cached.get(query, None)
        while result is None and self.coders != []:
            try:
                coder = next(self.current)
                result = coder().geocode(query, **kwargs)
                self.cached[query] = result
            except Exception as e:
                self.coders = [c for c in self.coders if c is not coder]
        return result

    def flush(self):
        pickle.dump(self.cached, open(self.cache, 'wb'))

    def __del__(self):
        self.flush()
