from flask import Blueprint, render_template, request, jsonify
from web_app import db
from web_app.models import Artist

artists = Blueprint('artists', __name__)

@artists.route('/')
def index():
    artists = Artist.query.all()
    return render_template('artists.html', artists=artists)

@artists.route('/create', methods=['POST'])
def create():
    artist = Artist(name=request.form['artist_name'])
    db.session.add(artist)
    db.session.commit()
    return jsonify({ 'id': artist.id, 'name': artist.name })
