import requests
import os

# User Input: Playlist URL and ARL token
#DEEPLINK = input("Enter Deezer Playlist Link: ")
#ARL = input("Enter your Deezer ARL token: ")
DEEPLINK = "https://www.deezer.com/en/playlist/13706149821"
ARL = "3e320989c11d3574793d622ed74b28611de268e677123b3f8fea573dc4a1c67f6da95d96b3c083e7c604808767200b6bb80fe7fb08ff0eb99f8c97db4bd478239ccae2fa9954cda269e9ff06283fe2cf520435f7a67aad6ccc945e6047dc52c0"

# Extract Playlist ID from URL
def extract_playlist_id(url):
    parts = url.split("/")
    return parts[-1] if parts[-1].isdigit() else None

# Fetch Playlist Data
def get_playlist_tracks(playlist_id, arl):
    url = f"https://api.deezer.com/playlist/{playlist_id}"
    cookies = {"arl": arl}
    response = requests.get(url, cookies=cookies)
    
    if response.status_code == 200:
        data = response.json()
        tracks = data.get("tracks", {}).get("data", [])
        return [(track["id"], track["title"], track["artist"]["name"]) for track in tracks]
    else:
        print("Failed to fetch playlist data.")
        return []

# Fetch Encrypted Track URL
def get_track_url(track_id, arl):
    url = f"https://api.deezer.com/track/{track_id}"
    cookies = {"arl": arl}
    response = requests.get(url, cookies=cookies)

    if response.status_code == 200:
        track_data = response.json()
        return track_data.get("link")  # This needs decryption to get the actual MP3 URL
    return None

# Download Encrypted File
def download_track(track_id, track_name, artist, arl, music_folder):
    track_url = get_track_url(track_id, arl)
    
    if track_url:
        response = requests.get(track_url, stream=True)
        filename = os.path.join(music_folder, f"{artist} - {track_name} (encrypted).mp3")
        
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to get track URL for {track_name}.")

# Main Execution
playlist_id = extract_playlist_id(DEEPLINK)
if playlist_id:
    print(f"Fetching tracks from Playlist ID: {playlist_id}")
    tracks = get_playlist_tracks(playlist_id, ARL)
    
    if tracks:
        # Create Music folder if it doesn't exist
        music_folder = os.path.join(os.getcwd(), "Music")
        os.makedirs(music_folder, exist_ok=True)

        for track_id, track_name, artist in tracks:
            print(f"Downloading: {artist} - {track_name}")
            download_track(track_id, track_name, artist, ARL, music_folder)
    else:
        print("No tracks found.")
else:
    print("Invalid playlist URL.")
