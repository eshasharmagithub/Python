from flask import Flask, request, jsonify, render_template
import requests
import base64
import os

app = Flask(__name__)

# Spotify API endpoints
SPOTIFY_API_URL = 'https://api.spotify.com/v1/'
SPOTIFY_SEARCH_ENDPOINT = 'search'

# Replace these with your actual Client ID and Client Secret
CLIENT_ID = '45c4aba804604c75adfe28272ace4df9'
CLIENT_SECRET = 'bcb1ea186416486fa8da12bab239a679'

def get_spotify_access_token():
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    return response.json().get('access_token')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend-songs', methods=['GET'])
def recommend_songs():
    mood = request.args.get('mood')
    if mood not in mood_categories:
        return jsonify({'error': 'Invalid mood'})

    access_token = get_spotify_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    query = f'genre:"{mood}"'
    search_params = {
        'q': query,
        'type': 'track',
        'limit': 10
    }
    response = requests.get(SPOTIFY_API_URL + SPOTIFY_SEARCH_ENDPOINT, params=search_params, headers=headers)
    if response.status_code == 200:
        tracks = response.json().get('tracks', {}).get('items', [])
        recommended_songs = [{'name': track['name'], 'artist': track['artists'][0]['name']} for track in tracks]
        return jsonify({'recommended_songs': recommended_songs})
    else:
        return jsonify({'error': 'Failed to fetch recommended songs'})

if __name__ == '__main__':
    app.run(debug=True)
