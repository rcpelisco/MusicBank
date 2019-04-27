from web_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.name}')"

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    file = db.relationship('File', backref='song', lazy=True)

    def __repr__(self):
        return f"Song('{self.title}','{self.album}', '{self.artist}', '{self.file}')"

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    extension = db.Column(db.String(255), nullable=False)
    name_on_server = db.Column(db.String(255), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))

    def __repr__(self):
        return f"File('{self.extension}','{self.name_on_server}')"

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    songs = db.relationship('Song', backref='artist', lazy=True)
    albums = db.relationship('Album', backref='artist', lazy=True)

    def __repr__(self):
        return f"Artist('{self.name}', '{self.albums}','{self.songs}')"

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    songs = db.relationship('Song', backref='album', lazy=True)

    def __repr__(self):
        return f"Album('{self.name}','{self.songs}')"
