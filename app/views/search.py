from app import application, cm
from flask import request

# Import helpers
from lib.helpers import message as message_helper
from lib.helpers.security import gen_uid, gen_ukey

from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ItemNotFound

import re

base_url = '/search'

@application.route(base_url + '/autocomplete', methods=['GET'])
def autocomplete():
	query = request.args.get('q')
	query_elems = re.split('\W+', query)


	tb_stops = Table('stops', connection=cm.db)
	# Get a basic result comparing the first word
	result_set = tb_stops.query_2(
		name__beginswith=query_elems[0],
		index="stop_name_index",
		reverse=True,
		limit=3
	)

	basic_result = list(result_set)

	ret_val = ""
	for item in basic_result:
		ret_val = ret_val + "<br>" + item["name"]

	return "query elems: " + ret_val