import urllib2
import urllib
import json
import pprint

class OSM:
	def __init__(self):
		self.email = "bussingtime@gmail.com"

	# Reverse geo-coding
	# Convert a lat and long to place name
	def get_place(self, lat, lon):
		url = "http://open.mapquestapi.com/nominatim/v1/reverse.php"
		# params
		params = {
			"lat": lat,
			"lon": lon,
			"format": "json",
			"zoom": "18"
		}

		# Encode the parameters in url
		data = urllib.urlencode(params)

		# Send request to nominatim servers
		request = urllib2.Request(url + "?" + data)

		response = urllib2.urlopen(request)

		# Get the geo coded data
		geocoded = json.loads(response.read())

		place_data = {}

		# Get the original lat and lon
		lat = geocoded.get("lat")
		lon = geocoded.get("lon")
		if lat is not None and lon is not None:
			place_data["lat"] = lat
			place_data["lon"] = lon

		# Get the whole address and store it
		address = geocoded.get("address")
		if address is not None:
			place_data["address"] = address

		# Get the stop name

		# Find the comma location
		display_name = geocoded.get("display_name")
		comma_loc = display_name.find(',')
		if comma_loc == -1:
			place_data["stop_name"] = display_name
		else:
			place_data["stop_name"] = display_name[:comma_loc]

		return place_data


if __name__ == "__main__":
	osm = OSM()
	print osm.get_place(lat="9.0922448", lon="76.4941459")

