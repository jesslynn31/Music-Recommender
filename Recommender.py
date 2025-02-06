from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pandas as pd
import os
import sys
import json
import matplotlib.pyplot as plt



feedback_file = "user_feedback.json"
if os.path.exists(feedback_file):
    with open(feedback_file, 'r') as f:
        user_feedback = json.load(f)
else:
    user_feedback = {}

def save_feedback():
    with open(feedback_file, 'w') as f:
        json.dump(user_feedback, f)

def get_csv_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.dirname(__file__), filename)

def get_similarities(song_name, data, threshold=0.5):
    numeric_features = ['Danceability', 'Energy', 'Tempo', 'Acousticness', 'Instrumentalness', 'Loudness', 'Key']
    data_cleaned = data.dropna(subset=['Track Name', 'Artist Name(s)'] + numeric_features)
    data_cleaned[numeric_features] = data_cleaned[numeric_features].apply(pd.to_numeric, errors='coerce')
    data_cleaned = data_cleaned.dropna(subset=numeric_features)
    
    
    scaler = StandardScaler()
    data_cleaned[numeric_features] = scaler.fit_transform(data_cleaned[numeric_features])

    song_name_normalized = song_name.strip().lower()
    matching_songs = data_cleaned[data_cleaned['Track Name'].str.lower() == song_name_normalized]
    
    if matching_songs.empty:
        return []

    
    knn = NearestNeighbors(n_neighbors=6, metric='euclidean') 
    knn.fit(data_cleaned[numeric_features])
    
    song_features = matching_songs[numeric_features].values
    distances, indices = knn.kneighbors(song_features)
    
    similar_songs = []
    added_songs = set()
    
    for dist, idx in zip(distances[0], indices[0]):
        song_name2 = data_cleaned.iloc[idx]['Track Name']
        artist_name2 = data_cleaned.iloc[idx]['Artist Name(s)']
        
        
        if song_name2.lower() == song_name_normalized or song_name2 in added_songs:
            continue

        feedback_key = f"{song_name}::{song_name2}"
        if feedback_key in user_feedback:
            if user_feedback[feedback_key] == 0:  
                similarity_score *= 0.5  
            elif user_feedback[feedback_key] == 1: 
                similarity_score *= 1.5 
        
        similarity_score = 1 / (1 + dist)  
        if similarity_score >= threshold:
            similar_songs.append((song_name2, artist_name2, similarity_score))
            added_songs.add(song_name2)
    
    return sorted(similar_songs, key=lambda x: x[2], reverse=True)



def visualize_similar_songs(song_name, similar_songs):
    song_names = [song for song, _, _ in similar_songs]
    similarity_scores = [score for _, _, score in similar_songs]

    plt.figure(figsize=(10, 6))
    plt.scatter(song_names, similarity_scores, color='blue')
    plt.title(f"Similar Songs to '{song_name}'")
    plt.xlabel("Song Names")
    plt.ylabel("Similarity Scores")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def my_songs(song_name, artist_name, data_names):
    similar_songs = get_similarities(song_name, data_names, threshold=0.5)
    if similar_songs:
        print("Next = skip current song, go to next song")
        print("Skip = restart, enter a new song to analyze")
        print(f"\nSongs similar to '{song_name}' by {artist_name}:")
        print("-" * 80)
        for song, artist, similarity_score in similar_songs:
            print(f"{song:<40} by {artist:<30} | Similarity: {similarity_score:.3f}")

            feedback = input(f"Do you think '{song}' by {artist} is similar to '{song_name}'? (yes/no/skip/next ): ")
            if feedback == 'yes':
                user_feedback[f"{song_name}::{song}"] = 1  
            elif feedback == 'no':
                user_feedback[f"{song_name}::{song}"] = 0  # Negative feedback
            elif feedback == 'skip':
                break
            elif feedback == 'next':
                continue
        save_feedback()

        user_input2 = input("Would you like to see a scatterplot of similar songs? (yes/no): ").strip().lower()
        if user_input2 == 'yes':
            visualize_similar_songs(song_name, similar_songs)

      
    else:
        print(f"No similar songs found for '{song_name}'.")

kpop_csv_path = get_csv_path("allkpopsongsfordataset.csv")
allsongs_csv_path = get_csv_path("allsongsfordataset.csv")
kpop_songs1 = pd.read_csv(kpop_csv_path)
all_songs = pd.read_csv(allsongs_csv_path)

print("Welcome to the song recommender!")

while True:
    print("\n1 = K-pop\n2 = Other Genres")
    user_input = input("Please pick K-pop or other genres: ")
    if user_input == "1":
        song_name = input("Please enter the song name: ")
        artist_name = input("Please enter the artist name: ")
        my_songs(song_name, artist_name, kpop_songs1)
    elif user_input == "2":
        song_name = input("Please enter the song name: ")
        artist_name = input("Please enter the artist name: ")
        my_songs(song_name, artist_name, all_songs)
    else:
        print("Invalid input. Please enter 1 or 2.")
    again = input("\nDo you want to go again? (yes/no): ").strip().lower()
    if again != "yes":
        print("Goodbye!")
        break