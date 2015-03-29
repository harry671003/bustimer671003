from app import application,cm
from app.models.user import User
from flask import request, render_template, url_for, redirect
from flask.ext.login import login_user, logout_user, current_user
from lib.helpers import message as message_helper

from lib.sqs.setup import SQS_Manager
from boto.sqs.message import Message as SQSMessage
from boto.dynamodb2.table import Table
from hashlib import sha1
from datetime import datetime
import json

base_url = '/bus'

# Route for adding a new bus
@application.route(base_url  + '/add', methods=['POST'])
def add_new_bus():
	try:
		data = request.get_data()
		# Store for verification
		test_table = Table('test', connection=cm.db)
		test_table.put_item(data={
			"id": "web-server" + sha1(str(datetime.now())).hexdigest(),
			"data": data
		})

		# Store the data
		# Get the queue
		bus_queue = SQS_Manager.conn.get_queue('bus_queue')
		if bus_queue is None:
			# Queue doesn't exist. So create it
			bus_queue = SQS_Manager.conn.create_queue('bus_queue')
		m = SQSMessage()
		m.set_body(json.dumps(data))
		print json.dumps(data)
		m.message_attributes = {
			"type": {
				"data_type": "String",
				"string_value": "new_bus_data"
			}	
		}
		bus_queue.write(m)
		return message_helper.success()
	except Exception, e:
		return message_helper.error(str(e))