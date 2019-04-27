from flask import Blueprint, render_template
from web_app.models import Song, Artist

main = Blueprint('main', __name__)

@main.route('/')
def index():
    songs = Song.query.all()
    artists = Artist.query.all()
    return render_template('index.html', songs=songs, artists=artists)

@main.route('/search/<key_word>')
def search_song(key_word):
    songs = Song.query.all()
    songString = ''
    for song in songs:
        songString += str.lower(song.title)

    value = search(songString, key_word) 
    print(value)
    return value

NO_OF_CHARS = 256
  
def badCharHeuristic(string, size): 
    ''' 
    The preprocessing function for 
    Boyer Moore's bad character heuristic 
    '''
  
    badChar = [-1]*NO_OF_CHARS 
  
    for i in range(size): 
        badChar[ord(string[i])] = i; 
  
    return badChar 

def search(text, keyword): 
    ''' 
    A pattern searching function that uses Bad Character 
    Heuristic of Boyer Moore Algorithm 
    '''
    keyword_length = len(keyword) 
    text_length = len(text) 
  
    badChar = badCharHeuristic(keyword, keyword_length)
    position = 0
    shift = 0
    while(shift <= text_length-keyword_length): 
        j = keyword_length-1
  
        while j>=0 and keyword[j] == text[shift+j]: 
            j -= 1
  
        if j<0: 
            position = shift
            shift += (keyword_length-badChar[ord(text[shift+keyword_length])] if shift+keyword_length<text_length else 1) 
        else: 
            shift += max(1, j-badChar[ord(text[shift+j])])

    value = text + '\n'

    for i in range(position):
        value += ' '

    value += keyword
    
    return value

 