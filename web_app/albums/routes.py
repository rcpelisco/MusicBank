from flask import Blueprint, jsonify, request
from web_app import db
from web_app.models import Album, Artist

albums = Blueprint('albums', __name__)

@albums.route('/')
def index():
    return 'albums'

@albums.route('/create', methods=['POST'])
def create():
    album = Album(name=request.form['album_name'],
        artist_id=request.form['artist_id'])
    db.session.add(album)
    db.session.commit()
    return jsonify({ 'id': album.id, 'name': album.name })

@albums.route('/get_from_artist/<id>')
def get_from_artist(id):
    artist = Artist.query.get(id)
    albums = []
    for album in artist.albums:
        albums.append({ 'value': album.id, 'text': album.name })
    return jsonify(albums)
