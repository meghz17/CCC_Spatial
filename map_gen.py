from __future__ import print_function
from pygmaps_ng import *
import dpla_parser, spatial_inference



def get_result_chunks(fetch_result, chunk_size = 250):
	# return (fetch_result[i:i+chunk_size] for i in xrange(0, len(fetch_result), chunk_size))
	return [fetch_result[i:i + chunk_size] for i in range(0, len(fetch_result), chunk_size)]

def build_dataset(geometry_list, id="data1", title="untitled dataset", key_color="FF0080"):

	dataset = DataSet(id, title, key_color)

	for idx, geo_data in enumerate(geometry_list):
		if(geo_data != [] and geo_data != None):
			if(type(geo_data) is list):

				if(len(geo_data) == 2):
					# print("Point")
					dataset.add_marker(geo_data, color="000000", text=title_list[idx].encode('utf-8'))	
				
				else:
					# print("Bounding Box")
					dataset.add_marker([float(geo_data[0]), float(geo_data[2])], color="FF0000")
					dataset.add_marker([float(geo_data[1]), float(geo_data[3])], color="FF0000")
					dataset.add_marker([float(geo_data[0]), float(geo_data[3])], color="FF0000")
					dataset.add_marker([float(geo_data[1]), float(geo_data[2])], color="FF0000")

			else:
				if(geo_data.get('type') == 'Polygon'):
					# print("Polygon")
					#for some ungodly reason we have long, lat values and we need lat, long.
					for point_list in geo_data.get('coordinates'):
						for point in point_list:
							point.reverse()
					wrap= []
					wrap.append(geo_data.get('coordinates'))
					dataset.add_polygon(wrap, fillColor="#00FF00", fillOpacity="0.6")
				
				elif(geo_data.get('type') == 'MultiPolygon'):
					# print("MultiPolygon")
					for poly in geo_data['coordinates']:
						for point in poly:
							point.reverse()
						wrap = []
						wrap.append(poly)
						dataset.add_polygon(wrap, threshold=.5)
				
				else:
					print("unknown geometry type" + str(geo_data.get('type')))

				
		else:
			print("Empty geo_data for item index: " + str(idx))

	return dataset



fetch_result = dpla_parser.result
# geometry_list = spatial_inference.infer_locations(fetch_result)
# title_list = dpla_parser.get_descriptions(fetch_result)

mymap = Map()
app1 = App('test1', title="Test #1")
mymap.apps.append(app1)


result_chunks = get_result_chunks(fetch_result, 100)
for idx, chunk in enumerate(result_chunks):
	geometry_list = spatial_inference.infer_locations(chunk)
	title_list = dpla_parser.get_descriptions(chunk)
	mydataset = build_dataset(geometry_list, id=idx, title="Chunk" + str(idx))
	app1.datasets.append(mydataset)

# mydataset = build_dataset(geometry_list)
# app1.datasets.append(mydataset)
mymap.build_page(center=[25,-4], zoom=3, outfile="Harvard_Library.html")