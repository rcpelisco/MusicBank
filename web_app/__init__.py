from flask import Flask
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, send, emit
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os

ALLOWED_EXTENSIONS = set(['mp3', 'flac', 'm4a'])
FILE_DESTINATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
	'static', 'uploads')

app = Flask(__name__)

app.config['ALLOWED_FILE_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = FILE_DESTINATION
app.config['SECRET_KEY'] = '6c88248707fc142f0253bd0b33b84bc8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/music_bank'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from web_app.albums.routes import albums
from web_app.artists.routes import artists
from web_app.main.routes import main
from web_app.songs.routes import songs
from web_app.users.routes import users

app.register_blueprint(albums, url_prefix='/albums')
app.register_blueprint(artists, url_prefix='/artists')
app.register_blueprint(main, url_prefix='/')
app.register_blueprint(songs, url_prefix='/songs')
app.register_blueprint(users, url_prefix='/users')

with app.app_context():
    db.create_all()
    db.session.commit()
    