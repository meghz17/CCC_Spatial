from __future__ import print_function, unicode_literals
from dpla_parser import *
from geopy.geocoders import Nominatim
import re

"""
Given a fetched item from the dpla, infer the location to place on a map.
If coordinates are provided by DPLA, will return only the coordinates.

Otherwise, some sort of inference should take place.
The naive approach is to simply return a polygon bounding the (likely vauge) area given.
"""
def infer_item_location(item): 
	if(get_item_spatial_block(item) != None):
		spatial_block = get_item_spatial_block(item)[0]

		if('coordinates' in spatial_block.keys()):
			return get_item_coordinates(item)

		geolocator = Nominatim()
		
		key = None
		if('city' in spatial_block.keys()):
			key = 'city'

		elif('region' in spatial_block.keys()):
			key = 'region'

		elif('county' in spatial_block.keys()):
			key = 'county'

		elif('state' in spatial_block.keys()):
			key = 'state'

		elif('country' in spatial_block.keys()):
			key = 'country'

		elif('name' in spatial_block.keys()):
			key = 'name'

		else:
			return []

		words = re.split(',', spatial_block[key])
		split_key = words[0]
		location = geolocator.geocode(split_key, exactly_one=True, timeout=60, geometry='geojson')
		if(location == None):
			print("Location could not be determined from block " + str(spatial_block))
			return []
		else:	
			return location.raw.get('geojson')

	else:
		print("Empty spatial block")
		return []


def infer_locations(fetch_result):
	locations = []
	for item in fetch_result:
		locations.append(infer_item_location(item))
	return locations