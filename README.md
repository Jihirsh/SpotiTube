# Spotify to YouTube Music Playlist Converter

This script allows users to convert a **Spotify playlist** into a **YouTube Music playlist** automatically. It retrieves tracks from a given Spotify playlist and searches for them on YouTube Music, creating a new playlist and adding the matching tracks.

---

## 🚀 Features
✔ Fetches songs from any **public** Spotify playlist.
✔ Searches for equivalent songs on **YouTube Music**.
✔ Creates a **new YouTube Music playlist** with matching tracks.
✔ **Automatic OAuth token refresh** for YouTube Music authentication.
✔ **Error handling & debugging** for smooth operation.

---

## 📌 Prerequisites
Ensure you have **Python 3.x** installed. Then, install the required dependencies:

```sh
pip install spotipy ytmusicapi python-dotenv requests
```

---

## 🔑 Setup

### 1️⃣ **Create a `.env` file** (to store credentials)

Create a `.env` file in the same directory as the script and add your **Spotify & YouTube Music API credentials**:

```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
```

> **Note:** Get your **Spotify API credentials** from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
>
> Get your **YouTube API credentials** from [Google Cloud Console](https://console.cloud.google.com/apis/credentials).

---

### 2️⃣ **Authenticate with YouTube Music (OAuth2.0)**
You must authenticate YouTube Music using `ytmusicapi`. Run the following command:

```sh
yt-musicapi oauth
```

Then it will ask for your YouTube client id and YouTube client secret and it will redirect to browser window (Make sure the gmail account you are authenticating with is granted access to use the application in Google console).

This will generate an **oauth.json** file, which contains authentication tokens. The script will use this file for YouTube Music API access.

> **oauth.json format:**
```json
{
    "access_token": "YOUR_ACCESS_TOKEN",
    "expires_at": 1712345678,
    "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

**Ensure `oauth.json` is in the same directory as the script!**

---

### 3️⃣ **Run the script**
Execute the script and provide a **Spotify playlist URL** when prompted:

```sh
python script.py
```

Example input:
```
Enter a public Spotify playlist URL: https://open.spotify.com/playlist/3K3ybjT0FZwbOFpr4qv5hA
```

**The script will:**
✅ Extract tracks from the Spotify playlist.
✅ Search for equivalent songs on YouTube Music.
✅ Create a new **YouTube Music playlist** and add the found songs.
✅ Provide the **YouTube Music playlist link** upon completion.

---

## 🛠 Troubleshooting
**Q: I get an authentication error for YouTube Music.**
👉 Ensure `oauth.json` is in the same directory as the script.
👉 Try re-authenticating using:
```sh
yt-musicapi oauth --client-id your_youtube_client_id --client-secret your_youtube_client_secret
```

**Q: Some songs are missing in the YouTube Music playlist.**
👉 The script searches YouTube Music by song title and artist. If an exact match isn’t found, it skips the track.

**Q: I get a `spotipy.SpotifyException: No token provided`.**
👉 Double-check your `.env` file and ensure your Spotify API keys are correct.

---

## 🎯 Conclusion
This script simplifies **Spotify to YouTube Music playlist conversion** using API automation. It is especially useful if you’re migrating from **Spotify to YouTube Music** or want to share playlists across platforms. 🚀

