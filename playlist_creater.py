import requests
import os
from dotenv import load_dotenv
import csv


load_dotenv(dotenv_path="spotifyac.env")

ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def get_playlist_tracks(playlist_id):
    tracks = set()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    while url:
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            print(f"Failed to fetch playlist {playlist_id}: {res.json()}")
            break

        data = res.json()
        for item in data["items"]:
            if item['track'] and item['track']['id']:
                track_id = item['track']['id']
                track_name = item['track']['name']
                print(f"Fetching: {track_name}")
                tracks.add(track_id)

        url = data.get('next')

    return list(tracks)


def get_current_user_id():
    url = "https://api.spotify.com/v1/me"
    res = requests.get(url, headers=HEADERS)
    return res.json()["id"]


def create_playlist(user_id, name, description):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    payload = {
        "name": name,
        "description": description,
        "public": False
    }
    res = requests.post(url, json=payload, headers=HEADERS)
    return res.json()


def add_tracks_to_playlist(playlist_id, track_ids):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    uris = [f"spotify:track:{tid}" for tid in track_ids]
    payload = {
        "uris": uris
    }
    res = requests.post(url, json=payload, headers=HEADERS)
    return res.json()


def create_playlist_and_add_songs():
    all_tracks = []

    try:
        with open('music_database.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  

            for row in reader:
                playlist_id = row[0]
                tracks = get_playlist_tracks(playlist_id)
                all_tracks.extend(tracks)

    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    user_id = get_current_user_id()
    print(f"Your Spotify user ID: {user_id}")

    unique_tracks = list(set(all_tracks))
    chunks = [unique_tracks[i:i+100] for i in range(0, len(unique_tracks), 100)]
    playlist_count = 1
    created_playlist = None

    for i, chunk in enumerate(chunks):
        if i % 100 == 0:
            playlist_name = f"all_songs_for_dataset_{playlist_count}"
            created_playlist = create_playlist(user_id, playlist_name, "songs for dataset")
            playlist_count += 1

        add_tracks_to_playlist(created_playlist['id'], chunk)

    print("All songs added!")


if __name__ == "__main__":
    create_playlist_and_add_songs()