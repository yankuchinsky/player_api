import random

def create_salt():
	salt = ''
	seq = '0123456789abcdefghijklmnopqrstuvwxyz'
	rng = random.randint(5, 10)
	print(rng)
	i = 0
	while i < rng:
		i += 1
		salt += random.choice(seq)
	return salt
