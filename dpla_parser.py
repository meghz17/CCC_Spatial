from __future__ import print_function, unicode_literals

from guess_language import guess_language

import dpla_utils



"""
:Author: Joshua Sheehy

For analysis of Collections in DPLA, includes calls for pulling down from a specific provider and 
helpers for printing in human readable format where appropriate.

Also includes convenience methods for info about a certain results pool (e.g. number of blocks with spatial data)

We receive an array of items and iterate over them.
Each item is a dictionary with results based on the conditions supplied, referred to below as a block of data.

"""
api_key = '47db75710ca371a08a3e35bfc73c8a9b'
conditions = {'sourceResource.collection': dpla_utils.hub_largest_collections["Harvard Library"], 'fields' : 'sourceResource.identifier, sourceResource.title, sourceResource.spatial'}
num_results = 150
result = dpla_utils.dpla_fetch(api_key, num_results, **conditions)


#Accessor functions for fetched data

"""
Access a block of DPLA fetched data from dpla_utils.dpla_fetch call
by its field key (e.g. sourceResource.title)
"""
def get_block_data(data, field_key):
	if(data[field_key] != None):
		return data[field_key]

"""
For a given call, return the number of items containing a sourceResource.spatial 
block followed by the total number of items retrieved
"""
def get_num_spatial_blocks(fetch_result):
	count = 0
	for block in result:
		if("sourceResource.spatial" in block.keys()):
			count+=1
	return count, len(fetch_result)		


def get_item_description(item):
	for field_key in item:
		if(field_key ==  u'sourceResource.title'):
			block = item[field_key]
			return block

def get_descriptions(fetch_result):
	descs = []
	for item in fetch_result:
		descs.append(get_item_description(item))
	return descs

def get_item_coordinates(item):
	for field_key in item:
		if(field_key ==  u'sourceResource.spatial'):
			block = item[field_key]
			block_dict = block[0]
			for key in block_dict:
				if(key == u'coordinates'):
					raw_point = block_dict[key].split(",")
					lat = raw_point[0]
					lon = raw_point[1]
					return [float(lat), float(lon)]
	return []

def guess_item_language(item):
	if(get_item_description(item) != None):
		return guess_language(get_item_description(item))

def get_item_spatial_block(item):
	for key in item.keys():
		if(key == u'sourceResource.spatial'):
			return item[key]

def guess_languages(fetch_result):
	langs = []
	for item in fetch_result:
		langs.append(guess_item_language(item))
	return langs

def get_coordinates(fetch_result):
	coords = []
	for item in fetch_result:
		coords.append(get_item_coordinates(item))
	return coords

def get_spatial_blocks(fetch_result):
	spatials = []
	for item in fetch_result:
		spatials.append(get_item_spatial_block(item)[0])
	return spatials

def get_item(fetch_result, index):
	if(index < len(fetch_result)):
		return fetch_result[index]
	else:
		print("Index out of bounds")

def get_collection_size_by_id(collection):
	if(type(collection) is unicode and any(char.isdigit() for char in collection)):
		conditions = {'sourceResource.collection': collection, "api_key": api_key}
		result = dpla_utils.send_request(dpla_utils.items_url, conditions)
		count = get_block_data(result, "count")
		return count
	else:
		return -1

def get_collection_sizes(collections=dpla_utils.hub_largest_collections):
	output = []
	for key, value in collections.items():
		output.append(get_collection_info_pretty(key, value))
	return '\n'.join(output)

def get_collection_info_pretty(collection_name, collection_id):
	return "%s%s%s%d" % ("Collection: ", collection_name, "\t#Items: ", get_collection_size_by_id(collection_id))

#Printing things nicely

"""
Print out the results of a call to dpla_utils.dpla_fetch
"""
def print_result(array):
	for idx, x in enumerate(array):
		print ("Item number: ", idx)		
		_print_info_blocks(x)

def _print_info_blocks(data):
	for field_key in data:
		_print_block_data(get_block_data(data, field_key))
		print("\n")

def _print_block_data(field):
	if(field != None):
		if(type(field) is str):
			print(field)
		elif(type (field) is unicode):
			print(field.encode('utf-8'))
		elif(type(field) is dict):
			for k, v in field.items():
				print("\t", k, ": ", v)
		elif(type(field) is list):
			if(type(field[0]) is dict):
				for k, v in field[0].items():
					if(type(k) is str and type(v) is str):
						print("\t", k, ": ", v)
					else:
						print("\t", k, ": ", v.encode('utf-8'))
			else:
				_not_supported_block_type(field[0])
		else:
			_not_supported_block_type(field)
	else:
		print(field_key, " is empty.")		
	
def _not_supported_block_type(obj):
	print(obj, " printing is not supported for type ", type(obj))


#Main



# print(get_collection_sizes(), "\n")
# print(get_collection_size_by_id(dpla_utils.hub_largest_collections["Harvard Library"]), "\n")
# if(num_results < 25):
#  	print_result(result)
# print(get_num_spatial_blocks(result))

# print(get_coordinates(result))
# print(guess_languages(result))
# print(get_descriptions(result))
# print(get_spatial_blocks(result))