import dpla_utils

"""
:Author: Joshua Sheehy

For analysis of Collections in DPLA, includes calls for pulling down from a specific provider and 
helpers for printing in human readable format where appropriate.

Also includes convenience methods for info about a certain results pool (e.g. number of blocks with spatial data)

"""
api_key = '47db75710ca371a08a3e35bfc73c8a9b'
conditions = {'sourceResource.collection': dpla_utils.hub_largest_collections["Harvard Library"],  'fields' : 'sourceResource.title, sourceResource.spatial, provider.name'}
num_results = 10
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
Access a particular spatial field value.
"""
def get_spatial_value(field, key):
	if(field[key] != None):
		return field[key]

"""
Retrieve key-value pair of spatial attributes and its value, if any
"""
def get_spatial_pair(field, key):
	if(field[key] != None):
		return key, field[key]

"""
For a given call, return the number of items containing a sourceResource.spatial 
block followed by the total number of items retrieved
"""
def get_num_spatial_blocks(result):
	count = 0
	for block in result:
		if("sourceResource.spatial" in block.keys()):
			count+=1
	return count, len(result)		


"""
Get the total number of items attached to a provider.
A provider is not the same as a collection, since a provider can contribute things not held 
by the provider.

Note: makes a zero item call since count is stored outside the docs field.

"""
def get_provider_size(provider):
	if type(provider) is str:
		conditions = {'provider.name': provider, "api_key": api_key, "page_size": 0}
		result = dpla_utils.send_request(dpla_utils.items_url, conditions)
		count = get_block_data(result, "count")
		return count
	else:
		return "Invalid provider name"

"""
Retrieve the sizes of an array of providers. 
Defaults to the providers in hub_largest_collections
"""
def get_providers_info(providers= dpla_utils.hub_largest_collections):
	output = []
	for key in providers.keys():
		output.append(get_provider_info_pretty(key))
	return '\n'.join(output)

"""
Format a call to get_provider_size for printing.
"""
def get_provider_info_pretty(provider):
	return "%s%s%s%d" % ("Provider: ", provider, "\t#Items: ", get_provider_size(provider))



def get_collection_size_by_id(collection):
	if(type(collection) is str and any(char.isdigit() for char in collection)):
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
		elif(type(field) is dict):
			for k, v in field.items():
				print("\t", k, ": ", v)
		elif(type(field) is list):
			if(type(field[0]) is dict):
				for k, v in field[0].items():
					print("\t", k, ": ", v)
			else:
				_not_supported_block_type(field[0])
		else:
			_not_supported_block_type(field)
	else:
		print(field_key, " is empty.")		
	
def _not_supported_block_type(obj):
	print(obj, " printing is not supported for type ", type(obj))


#Main



print(get_collection_sizes(), "\n")
print(get_collection_size_by_id(dpla_utils.hub_largest_collections["Harvard Library"]), "\n")
if(num_results < 25):
	print_result(result)
print(get_num_spatial_blocks(result))
