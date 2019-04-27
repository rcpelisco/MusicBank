from flask import Blueprint, redirect, request, send_file, jsonify
from werkzeug.utils import secure_filename
from web_app import db, app
from web_app.models import Song, File
from web_app.songs.utils import allowed_file
import uuid, os

songs = Blueprint('songs', __name__)

@songs.route('/upload', methods=['POST'])
def upload():
    print(request.form['title'], 
			request.form['artist'], 
			request.form['album'])

    if 'song' not in request.files:
        return redirect(url_for('main.index'))
        
    song = request.files['song']
    
    if song.filename == '':
        return redirect(url_for('main.index'))
        
    form_data = request.form
    file_extension = os.path.splitext(song.filename)[1]
    file_name = str(uuid.uuid1())

    if song and allowed_file(song.filename):
        filename = secure_filename(song.filename)
        song_db = Song(title=form_data['title'], 
            album_id=form_data['album'],
            artist_id=form_data['artist'])
        db.session.add(song_db)
        db.session.commit()

        music_file = File(extension=file_extension, 
			name_on_server = file_name, 
			song_id = song_db.id)
        db.session.add(music_file)
        db.session.commit()


        song.save(os.path.join(app.config['UPLOAD_FOLDER'], 
			file_name + file_extension))
            
    return redirect(request.referrer)

@songs.route('/download/<id>')
def download(id):
    song = Song.query.get(id)
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], song.file[0].name_on_server + song.file[0].extension), 
		as_attachment=True, attachment_filename=song.artist.name + ' - ' + song.title + song.file[0].extension)

@songs.route('/edit/<id>')
def edit(id):
    song = Song.query.get(id)

    return jsonify({ 'id': song.id,'title': song.title })

@songs.route('/update/<id>', methods=['POST'])
def update(id):
    song = Song.query.get(id)
    song.title = request.form['title']
    db.session.commit()

    return redirect(request.referrer)

@songs.route('/delete_song/<id>')
def delete(id):
    song = Song.query.get(id)

    os.remove(os.path.join(app.config['UPLOAD_FOLDER'],
        song.file[0].name_on_server + song.file[0].extension))

    file = File.query.filter_by(song_id=id).first()

    db.session.delete(file)
    db.session.delete(song)

    db.session.commit()
    
    return redirect(request.referrer)
    
