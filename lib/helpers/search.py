from operator import itemgetter
from lib.helpers.tables import tb_stops, tb_schedule
import re
from app.global_config import global_config
from decimal import Decimal
from lib.helpers.time import get_time_from_xhd as time

# relevance levels
__level_2_relevance = 15
__level_1_relevance = 10
__country_relevance = 5

def sort_by_relevance(stops, query_elems):
	for stop in stops:
		# set the default relevance as 0
		stop["relevance"] = 0
		for elem in query_elems:
			# Check the level_2 address (district)	
			if(elem == stop["level_2"]):
				stop["relevance"] += __level_2_relevance
				continue
			# Check the level_1 address (state)	
			if(elem == stop["level_1"]):
				stop["relevance"] += __level_1_relevance
				continue
			# Check the country
			if(elem == stop["country"]):
				stop["relevance"] += __country_relevance
				continue

	return sorted(stops, key=itemgetter('relevance'), reverse=True)


# Get the ids of stops given a query
def get_stops_from_query(query):
	query_elems = re.split('\W+', query)

	stop_name = query_elems[0]
	first_letter = stop_name[0]

	# Get the count of matching results
	num_matching = tb_stops.query_count(
		name_part__eq=first_letter,
		name__beginswith=stop_name,
		index='stop_name_index'
	)

	# Check if the count of results is less than the threshold
	if num_matching > global_config["autocomplete"]["max_search"]:
		# total count exceeding
		return None


	if num_matching == 0:
		return None

	# Get a basic result comparing the first word
	result_set = tb_stops.query_2(
		name_part__eq=first_letter,
		name__beginswith=stop_name,
		index='stop_name_index'
	)

	basic_result = list(result_set)
	# Convert to a list of dict with necessary details
	stops_results = []

	# Loop through the result and form a 
	# beautiful list of dicts with
	# only the necessary items
	for item in basic_result:
		stops_results.append(
			{
				"stop_id": item["stop_id"],
				"name": item["name"],
				"level_2": item["level_2"],
				"level_1": item["level_1"],
				"country": item["country"]
			}
		)
		
	sorted_stops = sort_by_relevance(stops_results, query_elems[1:])

	return sorted_stops

def get_buses_between(source_id, dest_id):
	source_schedules = tb_schedule.query_2(
		stop_id__eq=source_id,
		index='stop_id_index'
	)

	dest_schedules = tb_schedule.query_2(
		stop_id__eq=dest_id,
		index='stop_id_index'
	)

	# Convert to list
	source_schedules = list(source_schedules)

	dest_schedules = list(dest_schedules)
	
	if len(source_schedules) == 0 or len(dest_schedules) == 0:
		return None

	schedule_dict = {}
	if len(source_schedules) < len(dest_schedules):
		# Convert source_schedules to dict
		for stop in source_schedules:
			schedule_dict[stop["sch_id"]] = {
				"time": stop["time"]
			}
		dict_time_less = True
		schedule_list = dest_schedules
	else:
		# Convert dest_schedules to dict
		for stop in dest_schedules:
			schedule_dict[stop["sch_id"]] = {
				"time": stop["time"]
			}
		dict_time_less = False
		schedule_list = source_schedules

	timetable = []
	for list_sch in schedule_list:
		sch_id = list_sch["sch_id"]
		dict_sch = schedule_dict.get(sch_id)

		if dict_sch is not None:
			# This sch_id exists in the second table
			if dict_time_less:
				if dict_sch["time"] < list_sch["time"]:
					timetable.append(
						{
							"sch_id": sch_id,
							"time": time(dict_sch["time"])	# Since this is source schedule
						}
					)
			else:
				if dict_sch["time"] > list_sch["time"]:
					timetable.append(
						{
							"sch_id": sch_id,
							"time": time(list_sch["time"])	# Since this is source schedule
						}
					)

	if len(timetable) == 0:
		return None

	print timetable

	return sorted(timetable, key=itemgetter('time'))



