import spotipy
import csv
import time
from spotipy.oauth2 import SpotifyOAuth


SPOTIPY_CLIENT_ID = 'insert client ID'
SPOTIPY_CLIENT_SECRET = 'insert your spotify client secret'
SPOTIPY_REDIRECT_URI = 'insert your redirect url here'

scope = "user-library-read playlist-modify-private playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))



def playlist_initializer(playlist_id):
    tracks = set()
    try:
        results = sp.playlist_tracks(playlist_id)
        for item in results['items']:
            if item['track'] and item['track']['id']:
                track_id = item['track']['id']
                track_name = item['track']['name']
                print(f"Fetching: {track_name}")  
                tracks.add(track_id)

        while results['next']:
            results = sp.next(results)
            for item in results['items']:
                if item['track'] and item['track']['id']:
                    track_id = item['track']['id']
                    track_name = item['track']['name']
                    print(f"Fetching: {track_name}")  
                    tracks.add(track_id)

    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching playlist {playlist_id}: {e}")
    except Exception as e:
        print(f"Unexpected error for playlist {playlist_id}: {e}")

    return list(tracks)


def create_playlist_and_add_songs():
    all_tracks = []

    try:
        with open('music_database.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  

            for row in reader:
                playlist_id = row[0] 

                
                tracks = playlist_initializer(playlist_id)  
                
                all_tracks.extend(tracks)  

               

    except Exception as e:
        print(f"An error occurred: {e}")

    
    username = sp.current_user()['id']  

    tracks_added = 0
    new_playlist = None

    
    for i in range(0, len(all_tracks), 100):
        batch = all_tracks[i:i + 100]

        
        if tracks_added == 0 and new_playlist is None:
            new_playlist = sp.user_playlist_create(
                user=username,
                name='all_songs_for_dataset', 
                public=False, 
                description='songs for dataset'
            )

       
        sp.playlist_add_items(new_playlist['id'], batch)  
        tracks_added += len(batch)

        if tracks_added >= 10000:
            new_playlist = sp.user_playlist_create(
                user=username,
                name=f'all_songs_for_dataset_{tracks_added // 10000 + 1}',
                public=False,
                description='songs for dataset'
            )
            tracks_added = 0  

    #
    if tracks_added > 0 and new_playlist is not None:
        sp.playlist_add_items(new_playlist['id'], all_tracks[-tracks_added:])
        

if __name__ == "__main__":
    
    create_playlist_and_add_songs()
  
