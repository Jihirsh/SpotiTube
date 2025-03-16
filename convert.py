import os
import re
import spotipy
import json
import time
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic, OAuthCredentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OAUTH_FILE = "oauth.json"

# Get credentials from environment variables
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")

# Initialize Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Initialize YouTube Music API
ytmusic = YTMusic("oauth.json", oauth_credentials=OAuthCredentials(client_id=YOUTUBE_CLIENT_ID, client_secret=YOUTUBE_CLIENT_SECRET))  # You need to authenticate with YouTube Music


def extract_playlist_id(playlist_url):
    """Extracts the Playlist ID from a Spotify URL."""
    match = re.search(r"playlist/([a-zA-Z0-9]+)", playlist_url)
    return match.group(1) if match else None

def get_spotify_playlist_tracks(playlist_url):
    """Fetches all tracks from a given Spotify playlist."""
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print("Invalid Spotify playlist link!")
        return None, []

    playlist_info = sp.playlist(playlist_id)
    playlist_name = playlist_info["name"]  # Get playlist name

    results = sp.playlist_tracks(playlist_id)
    tracks = []
    
    for item in results["items"]:
        track = item["track"]
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        tracks.append(f"{track_name} - {artist_name}")
    
    return playlist_name, tracks

def search_on_ytmusic(track_name):
    """Searches for a song on YouTube Music and returns the first video ID."""
    search_results = ytmusic.search(track_name, filter="songs")
    if not search_results:
        return None
    return search_results[0]['videoId']

def create_ytmusic_playlist(playlist_name, description="Converted from Spotify"):
    """Creates a new playlist on YouTube Music and returns its playlist ID."""
    playlist_id = ytmusic.create_playlist(playlist_name, description)
    return playlist_id

def add_songs_to_ytmusic_playlist(playlist_id, songs):
    """Adds songs to an existing YouTube Music playlist."""
    video_ids = [search_on_ytmusic(song) for song in songs if search_on_ytmusic(song)]
    if not video_ids:
        print("No songs found on YouTube Music.")
        return
    
    ytmusic.add_playlist_items(playlist_id, video_ids)
    print(f"Added {len(video_ids)} songs to YouTube Music playlist!")

def convert_playlist(spotify_playlist_url):
    """Converts a Spotify playlist into a YouTube Music playlist."""
    playlist_name, songs = get_spotify_playlist_tracks(spotify_playlist_url)
    
    if not songs:
        print("No tracks found or invalid playlist.")
        return
    
    print(f"Converting '{playlist_name}' to YouTube Music...")

    # Create a new playlist on YouTube Music
    yt_playlist_id = create_ytmusic_playlist(playlist_name)
    print(f"YouTube Music Playlist Created: https://music.youtube.com/playlist?list={yt_playlist_id}")

    # Add songs to the new playlist
    add_songs_to_ytmusic_playlist(yt_playlist_id, songs)

def refresh_access_token():
    """Refreshes YouTube Music access token using the refresh token."""
    print("🔄 Access token expired. Refreshing...")

    tokens = load_oauth()
    refresh_token = tokens.get("refresh_token")

    if not refresh_token:
        print("❌ No refresh token found! Reauthenticate YouTube Music.")
        exit()

    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": YOUTUBE_CLIENT_ID,
        "client_secret": YOUTUBE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        new_tokens = response.json()
        tokens["access_token"] = new_tokens["access_token"]
        tokens["expires_at"] = time.time() + new_tokens["expires_in"]
        save_oauth(tokens)
        print("✅ Access token refreshed successfully!")
        return new_tokens["access_token"]
    else:
        print(f"❌ Failed to refresh token: {response.json()}")
        exit()

def get_access_token():
    """Gets a valid access token, refreshing if necessary."""
    tokens = load_oauth()
    if time.time() >= tokens["expires_at"]:  # Token expired
        return refresh_access_token()
    else:
        print("✅ Valid access token found!")
        return tokens["access_token"]

def load_oauth():
    """Loads OAuth tokens from oauth.json."""
    if not os.path.exists(OAUTH_FILE):
        print("❌ oauth.json file not found! Authenticate first.")
        exit()
    
    with open(OAUTH_FILE, "r") as f:
        return json.load(f)

def save_oauth(tokens):
    """Saves updated tokens to oauth.json."""
    with open(OAUTH_FILE, "w") as f:
        json.dump(tokens, f, indent=4)
        
# Example usage
if __name__ == "__main__":
    get_access_token()
    playlist_url = input("Enter a public Spotify playlist URL: ")
    convert_playlist(playlist_url)