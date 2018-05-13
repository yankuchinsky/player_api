from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from config import username as db_user, password as db_password
import hashlib

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:%s@localhost/Player' %(db_user, db_password)
db = SQLAlchemy(app)

api = Api(app)

class Songs(db.Model):
	__tablename__ = "Songs"
	id = db.Column('id', db.Integer, primary_key=True)
	song_name = db.Column(db.Text)

	def __init__(self, song_name):
		self.song_name = song_name

class LoginRoute(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name')
		parser.add_argument('password')
		args = parser.parse_args()
		
		return {'data': 'null'}

class UserRoute(Resource):
	def get(self, user_id):
		return {'username': 'user'}
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('user_name')
		parser.add_argument('user_password')
		args = parser.parse_args()
		user_name = args.user_name
		user_password = args.user_password
		salt = rand(10)
		#crypt_password = crypt.crypt(user_password, '$6$' + salt + '$')
		print(hashlib.sha256(user_password.encode('utf8')).hexdigest())
		return {'user': 'update'}

class CreateUser(Resouse):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('user_name')
		parser.add_argument('user_password')
		args = parser.parse_args()
		user_name = args.user_name
		user_password = args.user_password
		hashed_password = hashlib.sha256(user_password.encode('utf8')).hexdigest()
		#crypt_password = crypt.crypt(user_password, '$6$' + salt + '$')
		print()
		return{'okey': 'okey'}
class SongsRoute(Resource):
	def get(self):
		songs = Songs.query.all()
		songs_array = []
		for song in songs:
			songs_array.append({'id': song.id, 'song_name': song.song_name})
		return {'songs': songs_array}
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('song_name')
		args = parser.parse_args()
		song_name = args.song_name
		song = Songs(song_name)
		db.session.add(song)
		db.session.commit()
		return {'song_name': 'okey'}

class SongRoute(Resource):
	def get(self, song_id):
		song = Songs.query.get(song_id)
		if(song):
			return {'id': song.id, 'song_name': song.song_name}
		else:
			return{'error': 'No song with that id'}

api.add_resource(UserRoute, '/login')
api.add_resource(SongsRoute, '/songs')
api.add_resource(SongRoute, '/songs/<song_id>')

if __name__ == '__main__':
	app.run(debug=True)