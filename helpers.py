import random
import hashlib

def create_salt():
	salt = ''
	seq = '0123456789abcdefghijklmnopqrstuvwxyz'
	rng = random.randint(5, 10)
	i = 0
	while i < rng:
		i += 1
		salt += random.choice(seq)
	return salt

def hashed_password(password, salt):
	hashed_password = hashlib.sha256((salt + password).encode('utf8')).hexdigest()
	return hashed_password

def allowed_file(filename):
	ALLOWED_EXTENSIONS = set(['mp3'])
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

