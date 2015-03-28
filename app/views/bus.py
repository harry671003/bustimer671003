from app import application
from app.models.user import User
from flask import request, render_template, url_for, redirect
from flask.ext.login import login_user, logout_user, current_user
from lib.helpers import message as message_helper

from lib.sqs.setup import SQS_Manager
from boto.sqs.message import Message as SQSMessage

import json

base_url = '/bus'

# Route for admin index page
@application.route(base_url  + '/add')
def add_new_bus():
	data = {
		"data" : [
			{
				"lon" : "9.2343",
				"lat" : "90.034",
				"time": "9:45 am"
			},
			{
				"lon" : "9.2343",
				"lat" : "90.034",
				"time": "9:45 am"
			},
			{
				"lon" : "9.2343",
				"lat" : "90.034",
				"time": "9:45 am"
			},
			{
				"lon" : "9.2343",
				"lat" : "90.034",
				"time": "9:45 am"
			},
		]
	}
	# Get the queue
	bus_queue = SQS_Manager.conn.get_queue('bus_queue')
	if bus_queue is None:
		# Queue doesn't exist. So create it
		bus_queue = SQS_Manager.conn.create_queue('bus_queue')
	m = SQSMessage()
	m.set_body(json.dumps(data))
	m.message_attributes = {
		"type": {
			"data_type": "String",
			"string_value": "new_bus_data"
		}	
	}
	bus_queue.write(m)
	return str(bus_queue)

@application.route(base_url  + '/view')
def view_data():
	bus_queue = SQS_Manager.conn.get_queue('bus_queue')
	if bus_queue is None:
		# Queue doesn't exist. So create it
		bus_queue = SQS_Manager.conn.create_queue('bus_queue')
	rs = bus_queue.get_messages(5)
	ret = ""
	for result in rs:
		ret = ret + "<br> " + str(result)
	return ret