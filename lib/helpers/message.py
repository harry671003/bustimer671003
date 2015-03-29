from flask import jsonify
def error(message):
	data = {
		"status": "error",
		"message": message
	}
	return jsonify(data)

# Return success json
def success(data=None):
	ret_obj = {
		"status": "success"
	}
	if data and isinstance(data, dict):
		ret_obj["data"] = data
	return jsonify(ret_obj)
