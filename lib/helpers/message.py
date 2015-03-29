import json
def error(message):
	data = {
		"status": "error",
		"message": message
	}
	return json.dumps(data)

# Return success json
def success(data=None):
	ret_obj = {
		"status": "success"
	}
	if data and isinstance(data, dict):
		ret_obj["data"] = data
	return json.dumps(data)
