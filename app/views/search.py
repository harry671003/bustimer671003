from app import application, cm, global_config
from flask import request

# Import helpers
from lib.helpers import message as message_helper

from boto.dynamodb2.exceptions import ItemNotFound

from lib.helpers.search import get_stops_from_query, get_buses_between

base_url = '/search'

@application.route(base_url + '/', methods=['GET', 'POST'])
def search():
	# Get the arguments
	stop_id_source = request.args.get('stop_id_source')
	stop_id_dest = request.args.get('stop_id_dest')
	stop_name_source = request.args.get('stop_name_source')
	stop_name_dest = request.args.get('stop_name_dest')

	if stop_id_source is None:
		# Find the stop_id_source from the name
		if stop_name_source is None:
			return message_helper.error("Please specify a source.")

		stops_source_list = get_stops_from_query(stop_name_source)
		if stops_source_list is None:
			return message_helper.error("Cannot resolve source.")
		stop_id_source = stops_source_list[0]["stop_id"]

	if stop_id_dest is None:
		# Find the stop_id_source from the name
		if stop_name_dest is None:
			return message_helper.error("Please specify a destination.")

		stops_dest_list = get_stops_from_query(stop_name_dest)
		if stops_dest_list is None:
			return message_helper.error("Cannot resolve destination.")
		stop_id_dest = stops_dest_list[0]["stop_id"]

	timetable = get_buses_between(stop_id_source, stop_id_dest)

	if timetable is None:
		return message_helper.error("No buses found")

	return message_helper.success(
		data={
			"timetable": timetable
		}
	)




@application.route(base_url + '/autocomplete', methods=['GET'])
def autocomplete():
	query = request.args.get('q').lower()
	if query == None:
		return message_helper.error("Invalid query parameter")
	
	# Get the list of stops
	sorted_stops = get_stops_from_query(query)

	if sorted_stops is None:
		return message_helper.error("Cannot resolve stop!")
	return message_helper.success(sorted_stops)