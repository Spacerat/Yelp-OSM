import requests
import xml.etree.ElementTree as ET


def parse_node(node):
	obj = node.attrib.copy()
	obj['tags'] = {tag.attrib['k']: tag.attrib['v'] for tag in node if tag.tag == 'tag'}
	return obj

def parse_way(way):
	obj = way.attrib.copy()
	nds = []
	tags = {}
	for child in way:
		if child.tag == 'nd':
			nds.append(child.attrib['ref'])
		elif child.tag == 'tag':
			tags[child.attrib['k']] = child.attrib['v']
	obj.update({'nds': nds, 'tags': tags})
	return obj

def parse_relation(relation):
	obj = relation.attrib.copy()
	members = []
	tags = {}
	for child in relation:
		if child.tag == 'member':
			if not child.attrib['role']:
				del child.attrib['role']
			members.append(child.attrib.copy())
		elif child.tag == 'tag':
			tags[child.attrib['k']] = child.attrib['v']
	obj.update({'members': members, 'tags': tags})
	return obj

def parse_root(item_iter):
	bounds = {}
	nodes = []
	ways = []
	relations = []
	for child in item_iter:
		if child.tag == 'node':
			nodes.append(parse_node(child))
		elif child.tag == 'way':
			nodes.append(parse_way(child))
		elif child.tag == 'relation':
			nodes.append(parse_relation(child))
		elif child.tag == 'bounds':
			bounds = child.attrib

	return {'nodes': nodes, 'ways': ways, 'relations': relations, 'bounds': bounds}

def request_map_data(lattitude, longitude, box_degrees):
	""" Fire a request at OSM's map api """
    url = "https://api.openstreetmap.org/api/0.6/map"
    minlong = longitude - box_degrees
    minlat = lattitude - box_degrees
    maxlong = longitude + box_degrees
    maxlat = lattitude + box_degrees
    param = ",".join(str(x) for x in [minlong, minlat, maxlong, maxlat])
    return requests.get(url, params=dict(bbox=param), stream=True)

def parse_map_data(data):
	""" Turn a string containing an OSM XML response into python dictionaries and lists """
	return parse_root(ET.fromstring(data))

def search(lattitude=37.786660, longitude=-122.396559, box_degrees=0.001):
	""" Return the OSM map data for a particular box in the world """
	return parse_map_data(request_map_data(lattitude, longitude, box_degrees).content)

if __name__ == '__main__':
	print(search())