from app import application, cm
from flask import request, Response, render_template
from flask.ext.login import LoginManager
from lib.helpers.login import login_required
import json
from lib.helpers import message as message_helper
# Get the connection manager
from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table

# Base Url for this app 
base_url = '/config'

# setup the db
@application.route(base_url + '/setupdb', methods=['GET'])
@login_required(1)
def setup_db():
	# Create the users table
	try:
		# Check if Users table exist
		cm.db.describe_table('users')
	except Exception, e:
		# Users table doesn't exist. So create it
		users = Table.create('users', schema=[
				HashKey('uid'), # defaults to STRING data_type
			], throughput={
				'read': 1,
				'write': 1,
			}, connection=cm.db
		)

	# Create the bus table
	try:
		# Check if Bus table exist
		cm.db.describe_table('bus')
	except Exception, e:
		# bus table doesn't exist. So create it
		users = Table.create('bus', schema=[
				HashKey('bus_id'), # defaults to STRING data_type
			], throughput={
				'read': 1,
				'write': 1,
			}, connection=cm.db
		)
	
	# Create the bus-stops table
	try:
		cm.db.delete_table('schedule')
		cm.db.describe_table('schedule')
	except Exception, e:
		users = Table.create('schedule', schema=[
				HashKey('id'), # defaults to STRING data_type
			], throughput={
				'read': 1,
				'write': 1,
			}, 
			global_indexes= [
				GlobalAllIndex('sch_id_index', parts=[
					HashKey('sch_id'),
					RangeKey('stop_id')
				]),
				GlobalAllIndex('stop_id_index', parts=[
					HashKey('stop_id'),
				]),
				# GlobalAllIndex('time_index', parts=[
				# 	HashKey('stop_id'),
				# 	RangeKey('time', data_type="N")
				# ]),
			],
			connection=cm.db
		)

	# Create the stops table
	try:
		cm.db.describe_table('stops')
	except Exception, e:
		tb_stops = Table.create('stops', schema=[
				HashKey('stop_id', data_type="S"),
			], throughput={
				'read': 1,
				'write': 1,
			}, 
			global_indexes= [
				GlobalAllIndex('stop_name_index', parts=[
					HashKey('name_part', data_type="S"),
					RangeKey('name', data_type="S"),
				]),
				GlobalAllIndex('stop_level2_index', parts=[
					HashKey('level_2', data_type="S"),
				]),
				GlobalAllIndex('stop_level1_index', parts=[
					HashKey('level_1', data_type="S"),
				]),
				GlobalAllIndex('stop_country_index', parts=[
					HashKey('country', data_type="S"),
				]),
			],
			connection=cm.db
		)

	# Create the stops_loc table
	try:
		cm.db.describe_table('stops_loc')
	except Exception, e:
		tb_stops = Table.create('stops_loc', schema=[
				HashKey('stop_id', data_type="S"),
			], throughput={
				'read': 1,
				'write': 1,
			}, 
			global_indexes= [
				GlobalAllIndex('lat_index', parts=[
					HashKey('lat_part', data_type="S"),
					RangeKey('lat', data_type="N"),
				])
			],
			connection=cm.db
		)

	# Create the test table
	try:
		cm.db.describe_table('test')
	except Exception, e:
		users = Table.create('test', schema=[
				HashKey('id'), # defaults to STRING data_type
			], throughput={
				'read': 1,
				'write': 1,
			},
			connection=cm.db
		)

	# Create the settings table
	# This table contains all settings
	try:
		cm.db.describe_table('settings')
	except Exception, e:
		users = Table.create('settings', schema=[
				HashKey('name'), # defaults to STRING data_type
			], throughput={
				'read': 1,
				'write': 1,
			},
			connection=cm.db
		)

	# Initialize settings
	# -------------------
	# 1. user_auto_inc
	settings = Table('settings', connection=cm.db)

	return "Done!"

@application.route(base_url + '/showdb/<table_name>', methods=['GET'])
@login_required(1)
def show_db(table_name):
	table_data = []
	if table_name == "all_tables":
		tables = cm.db.list_tables()
		for table in tables["TableNames"]:
			table_data.append(cm.db.describe_table(table))
	else:
		table_data.append(cm.db.describe_table(table_name))
	return message_helper.success({
		"data": table_data
	})

@application.route(base_url + '/flush_schedules', methods=['GET'])
@login_required(1)
def flush_sched():
	# cm.db.delete_table("stops")
	# cm.db.delete_table("stops_loc")
	cm.db.delete_table("schedule")
	return "Done!"

@application.route(base_url + '/flush_stops', methods=['GET'])
@login_required(1)
def flush_stops():
	cm.db.delete_table("stops")
	cm.db.delete_table("stops_loc")
	return "Done!"



