from flask import Flask, render_template, jsonify
import requests
import pandas as pd
import base64
import json
from database import add_stat, get_stats
from flask import Flask, render_template
from database import create_tables

app = Flask(__name__)
create_tables()

# Replace these with your own Spotify Developer credentials
client_id = ""
client_secret = ""

def get_spotify_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_header = {
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    response = requests.post(auth_url, data=auth_data, headers=auth_header)
    return response.json()['access_token']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data')
def fetch_data():
    token = get_spotify_token()
    headers = {'Authorization': f"Bearer {token}"}
    
    # Replace this with the Spotify artist_id you want to fetch data for
    artist_id = "2gAXwURDNLBpiwlrgcl9HM"
    
    # Fetch data from Spotify API
    artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
    artist_response = requests.get(artist_url, headers=headers)
    artist_data = artist_response.json()
    
    # Process and aggregate data
    followers = artist_data['followers']['total']
    popularity = artist_data['popularity']
    
    # Fetch listeners data
    top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    top_tracks_response = requests.get(top_tracks_url, headers=headers)
    top_tracks_data = top_tracks_response.json()
    
    listeners = sum(track['popularity'] for track in top_tracks_data['tracks'])
    
    # Get the latest track's data and calculate the percentage difference
    latest_track = top_tracks_data['tracks'][0]
    previous_track = top_tracks_data['tracks'][1]
    latest_track_popularity = latest_track['popularity']
    latest_track_listeners = latest_track['popularity']
    popularity_diff = ((latest_track_popularity - previous_track['popularity']) / previous_track['popularity']) * 100
    listeners_diff = ((latest_track_listeners - previous_track['popularity']) / previous_track['popularity']) * 100

    # Save data to the database
    add_stat(artist_id, followers, popularity, listeners)

    # Fetch historical data from the database
    stats = get_stats(artist_id)
    
    data = {
    "stats": stats,
    "latest_track_popularity": latest_track_popularity,
    "latest_track_listeners": latest_track_listeners,
    "popularity_diff": popularity_diff,
    "listeners_diff": listeners_diff
}
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)
