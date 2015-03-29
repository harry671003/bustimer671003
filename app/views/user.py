from app import application, cm
from flask import request

# Import helpers
from lib.helpers import message as message_helper
from lib.helpers.security import gen_uid, gen_ukey

from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ItemNotFound

base_url = '/user'

@application.route(base_url + '/login', methods=['POST'])
def login():
	return message_helper.success()

# Register a new device to BusTimer
@application.route(base_url + '/register_device', methods=['POST', 'GET'])
def register_device():
	# Create a new u_id
	uid = gen_uid()
	try:
		user_table = Table('users', connection=cm.db)
		while 1:
			try:
				# Check if the uid exists
				is_existing_id = user_table.get_item(uid=uid)
				# Looks like it exists. So try again
			except ItemNotFound, e:
				# uid doesnot exists
				# Insert the device_id to table
				user_table.put_item(data={
					"uid": uid,
					"ukey": gen_ukey()
				})
				# Break from the loop after inserting the data
				break;

	except Exception, e:
		# If the application is in debug mode
		if application.debug:
			return message_helper.error(str(e))
		else:
			return message_helper.error("Sorry, An error occured")
	return message_helper.success()