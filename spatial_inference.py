from __future__ import print_function, unicode_literals
from dpla_parser import *
from geopy.geocoders import Nominatim
import re, json

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


def infer_locations(fetch_result, format_locs=False):
	locations = []
	for item in fetch_result:
		if(not format_locs):
			locations.append(infer_item_location(item))
		else:
			inferred_loc = infer_item_location(item)
			geojson = {}
			if( type(inferred_loc) is list):
				geojson['type'] = 'Point'
				geojson['coordinates'] = inferred_loc

				
				# locations.append(geojson)
			else:
				geojson = inferred_loc
				# locations.append(inferred_loc)

			props = {}
			props['title'] = get_item_description(item).encode('utf-8')
			geojson['properties'] = props

			locations.append(geojson)

	return locations

def dump_to_json(locations_array):
	f = open("file1.txt", 'w')
	json.dump(locations_array, f)


fetch_result = result
dump_to_json(infer_locations(fetch_result, True))