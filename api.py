from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS
import yt_dlp
import sqlite3
import os

os.environ["PATH"] += os.pathsep + "/path/to/ffmpeg"

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:5000"])  # Allow frontend requests from localhost:3000

# Your SQLite database path
DB_PATH = 'music_player.db'

# Ensure the 'music' folder exists to save downloaded songs
if not os.path.exists("music"):
    os.makedirs("music")

# Helper function to initialize the database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS playlists (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                  )''')
    c.execute('''CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    artist TEXT,
                    file_path TEXT
                  )''')
    c.execute('''CREATE TABLE IF NOT EXISTS playlist_songs (
                    playlist_id INTEGER,
                    song_id INTEGER,
                    FOREIGN KEY (playlist_id) REFERENCES playlists (id),
                    FOREIGN KEY (song_id) REFERENCES songs (id)
                  )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/songs/<int:song_id>', methods=['GET'])
def get_song_by_id(song_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Fetch the song by ID
        c.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
        song_record = c.fetchone()
        conn.close()

        if not song_record:
            return jsonify({"error": "Song not found"}), 404

        song_id, title, artist, file_path = song_record
        song_data = {
            "id": song_id,
            "title": title,
            "artist": artist if artist else "Unknown",
            "file_path": f"{file_path}"
        }

        return jsonify(song_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get all songs
@app.route('/songs', methods=['GET'])
def get_songs():
    try:
        songs = []
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        for root, dirs, files in os.walk("music"):
            for file in files:
                if file.endswith(".mp3"):
                    song_title = file.replace(".mp3", "")
                    c.execute("SELECT * FROM songs WHERE title = ?", (song_title,))
                    song_record = c.fetchone()

                    if song_record:
                        song_id, title, artist, file_path = song_record
                        songs.append({
                            "id": song_id,
                            "title": title,
                            "artist": artist if artist else "Unknown",
                            "file_path": f"http://localhost:5000/music/{file}"
                        })
        conn.close()
        return jsonify(songs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Create a new playlist
@app.route('/playlists', methods=['POST'])
def create_playlist():
    playlist_name = request.json.get('name')
    if not playlist_name:
        return jsonify({"error": "Playlist name is required"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO playlists (name) VALUES (?)", (playlist_name,))
        playlist_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({"id": playlist_id, "name": playlist_name}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get all playlists
@app.route('/playlists', methods=['GET'])
def get_playlists():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM playlists")
        playlists = c.fetchall()
        conn.close()

        return jsonify([{"id": playlist[0], "name": playlist[1]} for playlist in playlists]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add song to playlist
@app.route('/playlists/<int:playlist_id>/add', methods=['POST'])
def add_song_to_playlist(playlist_id):
    song_id = request.json.get('song_id')
    if not song_id:
        return jsonify({"error": "Song ID is required"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Check if the song exists
        c.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
        song = c.fetchone()
        if not song:
            return jsonify({"error": "Song not found"}), 404

        # Add song to playlist
        c.execute("INSERT INTO playlist_songs (playlist_id, song_id) VALUES (?, ?)", (playlist_id, song_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Song added to playlist"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Remove a song from a playlist
@app.route('/playlists/<int:playlist_id>/remove', methods=['POST'])
def remove_song_from_playlist(playlist_id):
    song_id = request.json.get('song_id')
    if not song_id:
        return jsonify({"error": "Song ID is required"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Check if the song exists
        c.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
        song = c.fetchone()
        if not song:
            return jsonify({"error": "Song not found"}), 404

        # Check if the song is in the playlist
        c.execute("SELECT * FROM playlist_songs WHERE playlist_id = ? AND song_id = ?", (playlist_id, song_id))
        playlist_song = c.fetchone()
        if not playlist_song:
            return jsonify({"error": "Song not in playlist"}), 404

        # Remove the song from the playlist
        c.execute("DELETE FROM playlist_songs WHERE playlist_id = ? AND song_id = ?", (playlist_id, song_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Song removed from playlist"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get single playlist by ID
@app.route('/playlists/<int:playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM playlists WHERE id = ?", (playlist_id,))
        playlist = c.fetchone()

        if not playlist:
            return jsonify({"error": "Playlist not found"}), 404

        # Get all songs in the playlist
        c.execute("""
            SELECT s.id, s.title, s.artist, s.file_path
            FROM songs s
            JOIN playlist_songs ps ON ps.song_id = s.id
            WHERE ps.playlist_id = ?
        """, (playlist_id,))
        songs = c.fetchall()

        conn.close()

        return jsonify({
            "id": playlist[0],
            "name": playlist[1],
            "songs": [{"id": song[0], "title": song[1], "artist": song[2], "file_path": song[3]} for song in songs]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get all playlists without a specific song
@app.route('/playlists/without_song', methods=['GET'])
def get_playlists_without_song():
    song_id = request.args.get('song_id')  # Get song_id from query params
    if not song_id:
        return jsonify({"error": "Song ID is required"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Get all playlists that do not contain the song
        c.execute("""
            SELECT p.id, p.name
            FROM playlists p
            WHERE p.id NOT IN (
                SELECT ps.playlist_id
                FROM playlist_songs ps
                WHERE ps.song_id = ?
            )
        """, (song_id,))

        playlists_without_song = c.fetchall()
        conn.close()

        return jsonify([{"id": playlist[0], "name": playlist[1]} for playlist in playlists_without_song]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# YouTube URL to MP3 conversion
@app.route('/convert', methods=['POST'])
def convert():
    youtube_url = request.json.get('url')

    if not youtube_url:
        return jsonify({"error": "YouTube URL is required"}), 400

    try:
        output_path = "music/%(title)s.%(ext)s"

        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioquality': 1,
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        song_title = yt_dlp.YoutubeDL({'outtmpl': '%(title)s'}).extract_info(youtube_url, download=False)['title']
        file_path = f"http://localhost:5000/music/{song_title}.mp3"

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO songs (title, artist, file_path) VALUES (?, ?, ?)", (song_title, "Unknown", file_path))
        conn.commit()
        conn.close()

        return jsonify({"message": "Conversion and song addition successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Serve music files
@app.route('/music/<filename>')
def serve_music(filename):
    return send_from_directory("music", filename)

if __name__ == '__main__':
    app.run(debug=True)
