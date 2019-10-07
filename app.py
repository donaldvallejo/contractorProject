# sudo lsof -iTCP -sTCP:LISTEN -n -P
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/cars')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
cars = db.cars
comments = db.comments

app = Flask(__name__)

@app.route('/')
def playlists_index():
  """Show all cars"""
  return render_template('playlists_index.html', cars=cars.find())

@app.route('/playlists/new')
def playlists_new():
  """Create Playlists"""
  return render_template('playlists_new.html', car = {}, title='New Cars')

@app.route('/playlists', methods=['POST'])
def playlists_submit():
  """Submit playlists to database"""
  playlist = {
    'Make': request.form.get('Make'),
    'Model': request.form.get('Model'),
    'Description': request.form.get('Description'),
    'Color': request.form.get('Color'),
    'Price': request.form.get('Price'),
    'Image': request.form.get('Image'),
    'created_at': datetime.now()
  }

  playlist_id = playlists.insert_one(playlist).inserted_id
  print("Check to see if Data is even happening \n", playlist_id, playlist)
  return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """Show a single playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)})
    return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)

@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """Show the edit form for a playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')

@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
  """Submit an edited playlists"""
  updated_playlist = {
      'Make': request.form.get('Make'),
      'Model': request.form.get('Model'),
      'Description': request.form.get('Description'),
      'Color': request.form.get('Color'),
      'Price': request.form.get('Price'),
      'Image': request.form.get('Image'),
  }
  playlists.update_one(
    {'_id': ObjectId(playlist_id)},
    {'$set': updated_playlist})
  return redirect(url_for('playlists_show', playlist_id=playlist_id))

@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """Delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))

@app.route('/playlists/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'playlist_id': ObjectId(request.form.get('playlist_id'))
    }
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))

@app.route('/playlists/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('playlists_show', playlist_id=comment.get('playlist_id')))

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))