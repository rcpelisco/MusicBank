def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in set(['mp3', 'flac', 'm4a'])
