from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import username as db_user, password as db_password
from helpers import create_salt, hashed_password, allowed_file
from functools import wraps
from werkzeug.utils import secure_filename
import os
import jwt
import datetime

UPLOAD_FOLDER = './uploads/songs/'

app = Flask(__name__)
app.config['SECRET_KEY'] = "kugsdifg838hd932923gd737dg3979gd23d7g2kkdbkbkabskdbksdo080898"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:%s@localhost/Player' %(db_user, db_password)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

api = Api(app)
cors = CORS(app, resources={"*": {"origins": "*"}})

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.headers.get('token')
		if(not token):
			return {'Error': 'Token is missing'}, 403
		try:
			jwt.decode(token, app.config['SECRET_KEY'])
		except:
			return {'Error': 'Token is invalid'}, 403
		return f(*args, **kwargs)
	return decorated

class Songs(db.Model):
	__tablename__ = "Songs"
	id = db.Column('id', db.Integer, primary_key=True)
	song_name = db.Column(db.Text)
	def __init__(self, song_name):
		self.song_name = song_name

class Users(db.Model):
	__tablename__ = "Users"
	user_name = db.Column(db.String,  primary_key=True)
	user_password = db.Column(db.String)
	salt = db.Column(db.String)
	def __init__(self, user_name, user_password, salt):
		self.user_name = user_name
		self.user_password = user_password
		self.salt = salt

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
		return {'user': 'update'}

class LoginRoute(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('user_name')
		parser.add_argument('user_password')
		args = parser.parse_args()
		user_name = args.user_name
		user_password = args.user_password
		user = Users.query.get(user_name)
		password = hashed_password(user_password, user.salt)
		if(not user):
			return {'error': 'User is not found'}
		if(password != user.user_password):
			return {'error': 'Wrong password'}
		else:
			date = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
			print(str(date))
			token = jwt.encode({'user': user_name, 'expire': str(date)}, app.config['SECRET_KEY'])
			return {'token': token.decode('UTF-8')}

class CreateUserRoute(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('user_name')
		parser.add_argument('user_password')
		args = parser.parse_args()
		user_name = args.user_name
		user_password = args.user_password
		error = ''
		user = Users.query.get(user_name)
		if user:
			return{'error': 'This username is already exist'}
		if not user_name:
			return{'error': 'Username is empty'}
		if not user_password:
			return{'error': "Password is empty"}
		if not error:
			salt = create_salt()
			user = Users(user_name, hashed_password(user_password, salt), salt)
			db.session.add(user)
			db.session.commit()
			return{'success': 'User successfully created'}

class SongsRoute(Resource):
	def get(self):
		songs = Songs.query.all()
		songs_array = []
		for song in songs:
			songs_array.append({'id': song.id, 'song_name': song.song_name})
		return {'songs': songs_array}
	@token_required
	def post(self):
		if 'file' not in request.files:
			return{'error': 'No file uploaded'}, 403
		file = request.files['file']
		if allowed_file(file.filename):
			filename = secure_filename(file.filename)
			song = Songs(filename)
			file.save(app.config['UPLOAD_FOLDER'] + filename)
			db.session.add(song)
			db.session.commit()
			return {'success': 'File uploaded'}, 200
		else:
			return {'error': 'File type is not allowed'}, 403

class SongRoute(Resource):
	def get(self, song_id):
		song = Songs.query.get(song_id)
		if(song):
			return {'id': song.id, 'song_name': song.song_name}
		else:
			return{'error': 'No song with that id'}

api.add_resource(LoginRoute, '/login')
api.add_resource(CreateUserRoute, '/users')
api.add_resource(SongsRoute, '/songs')
api.add_resource(SongRoute, '/songs/<song_id>')

if __name__ == '__main__':
	app.run(debug=True)