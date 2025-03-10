from flask import Flask, request, render_template, jsonify
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pandas as pd
import os
import sys
import json
import matplotlib.pyplot as plt

app = Flask(__name__, template_folder="templates")


feedback_file = "user_feedback.json"
if os.path.exists(feedback_file):
    with open(feedback_file, 'r') as f:
        user_feedback = json.load(f)
else:
    user_feedback = {}


def load_data():
    try:
        kpop_csv_path = "allkpopsongsfordataset.csv"
        allsongs_csv_path = "allsongsfordataset.csv"

        kpop_songs = pd.read_csv(kpop_csv_path)
        all_songs = pd.read_csv(allsongs_csv_path)

        print("Datasets loaded successfully.") 
        return kpop_songs, all_songs
    except Exception as e:
        print("Error loading datasets:", e)
        return None, None

kpop_songs, all_songs = load_data()

def save_feedback():
    with open(feedback_file, 'w') as f:
        json.dump(user_feedback, f)

def get_csv_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.dirname(__file__), filename)

def get_similarities(song_name, data, threshold=0.5):
    print(f"Searching for songs similar to: {song_name}")  

    numeric_features = ['Danceability', 'Energy', 'Tempo', 'Acousticness', 'Instrumentalness', 'Loudness', 'Key']

   
    data_cleaned = data.dropna(subset=['Track Name', 'Artist Name(s)'] + numeric_features)
    data_cleaned[numeric_features] = data_cleaned[numeric_features].apply(pd.to_numeric, errors='coerce')
    data_cleaned = data_cleaned.dropna(subset=numeric_features)

 
    scaler = StandardScaler()
    data_cleaned[numeric_features] = scaler.fit_transform(data_cleaned[numeric_features])

    
    matching_songs = data_cleaned[data_cleaned['Track Name'].str.lower() == song_name.lower()]
    
    if matching_songs.empty:
        print("No matching songs found!")
        return []  

   
    knn = NearestNeighbors(n_neighbors=6, metric='euclidean')
    knn.fit(data_cleaned[numeric_features]) 

   
    song_features = matching_songs[numeric_features].values.reshape(1, -1)  

   
    distances, indices = knn.kneighbors(song_features)
    
    similar_songs = []
    added_songs = set()

    for dist, idx in zip(distances[0], indices[0]):
        song_name2 = data_cleaned.iloc[idx]['Track Name']
        artist_name2 = data_cleaned.iloc[idx]['Artist Name(s)']

        if song_name2.lower() == song_name.lower() or song_name2 in added_songs:
            continue
        
        similarity_score = 1 / (1 + dist)  

        if similarity_score >= threshold:
            similar_songs.append({"song": song_name2, "artist": artist_name2, "similarity": round(similarity_score, 3)})
            added_songs.add(song_name2)

    print(f"Found {len(similar_songs)} similar songs.")  
    return sorted(similar_songs, key=lambda x: x["similarity"], reverse=True)


@app.route("/")
def home():
    print("Rendering index.html...")
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    song_name = request.form.get("song_name")
    genre = request.form.get("genre")
    
    data = kpop_songs if genre == "kpop" else all_songs
    similar_songs = get_similarities(song_name, data)
    
    return render_template("index.html", song_name=song_name, similar_songs=similar_songs)

@app.route("/feedback", methods=["POST"])
def feedback():
    song_name = request.form.get("song_name")
    similar_song = request.form.get("similar_song")
    feedback_value = int(request.form.get("feedback_value"))
    
    feedback_key = f"{song_name}::{similar_song}"
    user_feedback[feedback_key] = feedback_value
    save_feedback()
    
    return jsonify({"status": "success", "message": "Feedback saved!"})

if __name__ == "__main__":
    app.run(debug=True)