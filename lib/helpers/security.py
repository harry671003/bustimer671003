import random
import string
import hashlib
import uuid

def generate_random_string(length):
	if(length > 512):
		return None

	# Generate the random string
	random_string = ''
	for i in range(0, length):
		random_string += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)

	return random_string

# Generate a new users ID
# Generate a 256 bit uid
def generate_new_user_id():
	return hashlib.sha256(
		str(uuid.uuid4()) + generate_random_string(40)
	).hexdigest()

# Generate a new users key
# Generate a 512 bit key
def generate_new_user_key():
	return hashlib.sha512(
		generate_random_string(40) + str(uuid.uuid4())
	).hexdigest()

gen_rand_str = generate_random_string
gen_uid = generate_new_user_id
gen_ukey = generate_new_user_key