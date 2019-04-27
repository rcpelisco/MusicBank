from flask import Blueprint, render_template
from web_app.models import Song, Artist

main = Blueprint('main', __name__)

@main.route('/')
def index():
    songs = Song.query.all()
    artists = Artist.query.all()
    return render_template('index.html', songs=songs, artists=artists)
