from app import application, cm
from flask import request, render_template

# Import helpers
from lib.helpers import message as message_helper
from lib.helpers.security import gen_uid, gen_ukey

from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ItemNotFound
from lib.helpers.time import get_xhd_from_time, get_time_from_xhd, get_time_str
from lib.helpers.coords import Coords
from lib.helpers.tables import tb_schedule

from lib.helpers.map import Geocode
import os

from app.models.stops import get_stop

base_url = '/test'

@application.route(base_url + '/add_schedules', methods=['GET'])
def add_sample_schedules():
	try:
		with tb_schedule.batch_write() as batch:
			batch.put_item(data={
				'id': '7',
				'sch_id': '2',
				'stop_id': 'alpy',
				'time': get_xhd_from_time(hour=12, minute=0),
				'cnt': 5,
			})
			batch.put_item(data={
				'id': '8',
				'sch_id': '2',
				'stop_id': 'kykm',
				'time': get_xhd_from_time(hour=12, minute=15),
				'cnt': 5,
			})
			batch.put_item(data={
				'id': '9',
				'sch_id': '2',
				'stop_id': 'ochr',
				'time': get_xhd_from_time(hour=12, minute=30),
				'cnt': 5,
			})
			batch.put_item(data={
				'id': '10',
				'sch_id': '2',
				'stop_id': 'vlkv',
				'time': get_xhd_from_time(hour=12, minute=45),
				'cnt': 5,
			})
			batch.put_item(data={
				'id': '11',
				'sch_id': '2',
				'stop_id': 'kpy',
				'time': get_xhd_from_time(hour=13, minute=0),
				'cnt': 5,
			})
			batch.put_item(data={
				'id': '12',
				'sch_id': '2',
				'stop_id': 'klm',
				'time': get_xhd_from_time(hour=13, minute=15),
				'cnt': 5,
			})



			batch.put_item(data={
				'id': '1',
				'sch_id': '1',
				'stop_id': 'alpy',
				'time': get_xhd_from_time(hour=12, minute=0),
				'cnt': 5,
			})
			batch.put_item(data={
				'id': '2',
				'sch_id': '1',
				'stop_id': 'kykm',
				'time': get_xhd_from_time(hour=12, minute=15),
				'cnt': 5,
			})
			batch.put_item(data={
				'id': '3',
				'sch_id': '1',
				'stop_id': 'ochr',
				'time': get_xhd_from_time(hour=12, minute=30),
				'cnt': 5,
			})
			batch.put_item(data={
				'id': '4',
				'sch_id': '1',
				'stop_id': 'vlkv',
				'time': get_xhd_from_time(hour=12, minute=45),
				'cnt': 5,
			})
			batch.put_item(data={
				'id': '5',
				'sch_id': '1',
				'stop_id': 'kpy',
				'time': get_xhd_from_time(hour=13, minute=0),
				'cnt': 5,
			})
			batch.put_item(data={
				'id': '6',
				'sch_id': '1',
				'stop_id': 'klm',
				'time': get_xhd_from_time(hour=13, minute=15),
				'cnt': 5,
			})
		return message_helper.success()
	except Exception, e:
		return message_helper.error(str(e))

@application.route(base_url + '/add_stops', methods=['GET'])
def add_sample_stops():
	# try:
	c = Coords()
	tb_stops = Table('stops', connection=cm.db)
	tb_stops_loc = Table('stops_loc', connection=cm.db)
	with tb_stops.batch_write() as batch:
		batch.put_item(data={
			'stop_id': 'alpy',
			'name_part': 'a',
			'name'	 : 'aleppey',
			'level_2': 'alappuzha',
			'level_1': 'kerala',
			'country': 'india'
		})
		batch.put_item(data={
			'stop_id': 'kykm',
			'name_part': 'k',
			'name'	 : 'kayankulam',
			'level_2': 'alappuzha',
			'level_1': 'kerala',
			'country': 'india'
		})
		batch.put_item(data={
			'stop_id': 'ochr',
			'name_part': 'o',
			'name'	 : 'oachira',
			'level_2': 'kollam',
			'level_1': 'kerala',
			'country': 'india'
		})
		batch.put_item(data={
			'stop_id': 'vlkv',
			'name_part': 'v',
			'name'	 : 'vallikavu',
			'level_2': 'kollam',
			'level_1': 'kerala',
			'country': 'india'
		})
		batch.put_item(data={
			'stop_id': 'kpy',
			'name_part': 'k',
			'name'	 : 'karunagapally',
			'level_2': 'kollam',
			'level_1': 'kerala',
			'country': 'india'
		})
		batch.put_item(data={
			'stop_id': 'klm',
			'name_part': 'k',
			'name'	 : 'kollam',
			'level_2': 'kollam',
			'level_1': 'kerala',
			'country': "india"
		})

	# Adding to location
	with tb_stops_loc.batch_write() as batch:
		batch.put_item(data={
			'stop_id': 'alpy',
			'lat_part': "9",
			'lat': c.integerify(9.5010367),
			'lon': c.integerify(76.3421059),
			'lon_part': '76'
		})
		batch.put_item(data={
			'stop_id': 'kykm',
			'lat_part':"9",
			'lon_part': '76',
			'lat': c.integerify(9.1729609),
			'lon': c.integerify(76.5073299)
			
		})
		batch.put_item(data={
			'stop_id': 'ochr',
			'lat_part':"9",
			'lon_part': '76',
			'lat': c.integerify(9.1272739),
			'lon': c.integerify(76.5065333)
			
		})
		batch.put_item(data={
			'stop_id': 'vlkv',
			'lat': c.integerify(9.0938471),
			'lon': c.integerify(76.4916068),
			'lat_part':"9",
			'lon_part': '76'
		})
		batch.put_item(data={
			'stop_id': 'kpy',
			'lat_part':"9",
			'lon_part': '76',
			'lat': c.integerify(9.0609902),
			'lon': c.integerify(76.5341999)
			
		})
		batch.put_item(data={
			'stop_id': 'klm',
			'lat_part':"8",
			'lon_part': '76',
			'lat': c.integerify(8.8862714),
			'lon': c.integerify(76.5938379)
			
		})
	return message_helper.success()
	# except Exception, e:
	# 	return message_helper.error(str(e))

@application.route(base_url + '/schedule/<schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
	if(schedule_id == "all"):
		# Get all entries
		schedules = tb_schedule.scan()
	else:
		# Get the schedles with sch_id
		schedules = tb_schedule.query_2(
			sch_id__eq=schedule_id,
			index='sch_id_index'
		)
	data = []
	schedules = list(schedules)
	print schedules
	for schedule in schedules:
		time = get_time_from_xhd(schedule["time"])
		time_str = get_time_str(time["hour"], time["minute"], time["second"])
		# Get the stop info
		stop = get_stop(schedule["stop_id"])
		data.append({
			"id": schedule["id"],
			"sch_id": schedule["sch_id"],
			"stop_id": schedule["stop_id"],
			"stop_name": stop["name"],
			"time": time_str,
			"num_contributors": schedule["num_contributors"]
		})
	return render_template("schedules.html", schedules=data)

@application.route(base_url + '/add_coords', methods=['GET'])
def add_coords():
	geocode = Geocode()
	f = open(str(os.path.dirname(__file__)) + "/coords.txt", "r")
	for line in f:
		coords = line.strip('\n').split(",")
		print coords
		print str(geocode.get_place(lat=coords[0],lon=coords[1]))

	return "Done"

@application.route(base_url + '/check', methods=['GET'])
def add_check():
	# with tb_schedule.batch_write() as batch:
	# 	batch.put_item(data={
	# 		'id': '1',
	# 		'sch_id': "1",
	# 		'stop_id': 'alpy',
	# 		'time': 1,
	# 	})
	# 	batch.put_item(data={
	# 		'id': '2',
	# 		'sch_id': "2",
	# 		'stop_id': 'd030c5daf31c844401c44bfb7cc4ba90e082686e',
	# 		'time': 30600,
	# 	})
	# # q = tb_schedule.query_2(
	# # 	stop_id__eq='alpy',
	# # 	time__eq__gt=0,
	# # 	index='stop_id_index'
	# # )
	# # q = list(q)
	# # print q

	# schedule = tb_schedule.query_2(
	# 	sch_id__eq="2",
	# 	index='sch_id_index'
	# # )
	# # schedule = list(schedule)
	# # print "[+]" + str(schedule)
	# # stop = tb_schedule.get_item(id="s_id")
	# x = tb_schedule.query_2(
	# 	sch_id__eq='2',
	# 	index='sch_id_index'
	# )
	# x = list(x)
	# print x
	print get_time_from_xhd(36090)
	return "Done"