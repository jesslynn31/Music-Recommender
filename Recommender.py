from flask import Flask, redirect, request, render_template, jsonify, url_for, session
from authlib.integrations.flask_client import OAuth
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pandas as pd
from dotenv import load_dotenv
import os
import sys
import json
import matplotlib.pyplot as plt

app = Flask(__name__, template_folder="templates")


load_dotenv("info.env")

app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True  
app.config['SESSION_KEY_PREFIX'] = 'oauth_'

app.secret_key = os.urandom(24)  
oauth = OAuth(app)

oidc = oauth.register(
    name='oidc',
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    server_metadata_url=os.getenv("COGNITO_AUTHORITY") + "/.well-known/openid-configuration",
    client_kwargs={'scope': 'phone openid email'}
)

feedback_file = "user_feedback.json"
if os.path.exists(feedback_file):
    with open(feedback_file, 'r') as f:
        user_feedback = json.load(f)
else:
    user_feedback = {}


def load_data():
    try:
        allsongs_csv_path = "allsongsfordataset.csv"

        all_songs = pd.read_csv(allsongs_csv_path)

        print("Dataset loaded successfully.") 
        return all_songs
    except Exception as e:
        print("Error loading datasets:", e)
        return None, None

all_songs = load_data()

def save_feedback():
    with open(feedback_file, 'w') as f:
        json.dump(user_feedback, f)

def get_csv_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.dirname(__file__), filename)

def get_similarities(song_name, data, selected_features=None, threshold=0.5):
    print(f"Searching for songs similar to: {song_name}")  

    numeric_features = ['Danceability', 'Energy', 'Tempo', 'Acousticness', 'Instrumentalness', 'Loudness', 'Key']

    if selected_features is None:
        selected_features = numeric_features
    else:
        selected_features = [feature for feature in selected_features if feature in numeric_features]
    
    if not selected_features:
        print("No valid features selected!")
        return []

   
    data_cleaned = data.dropna(subset=['Track Name', 'Artist Name(s)'] + selected_features)
    data_cleaned[selected_features] = data_cleaned[selected_features].apply(pd.to_numeric, errors='coerce')
    data_cleaned = data_cleaned.dropna(subset=selected_features)

 
    scaler = StandardScaler()
    data_cleaned[selected_features] = scaler.fit_transform(data_cleaned[selected_features])

    
    matching_songs = data_cleaned[data_cleaned['Track Name'].str.lower() == song_name.lower()]
    
    if matching_songs.empty:
        print("No matching songs found!")
        return []  

   
    knn = NearestNeighbors(n_neighbors=6, metric='euclidean')
    knn.fit(data_cleaned[selected_features]) 

   
    song_features = matching_songs[selected_features].iloc[0].values.reshape(1, -1)


   
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



@app.route('/')
def index():
    return render_template(
        "index.html",
        cognito_domain=os.getenv("COGNITO_DOMAIN"),
        client_id=os.getenv("CLIENT_ID"),
        redirect_uri=os.getenv("REDIRECT_URI")
    )
    


@app.route('/login')
def login():
    return oauth.oidc.authorize_redirect(redirect_uri='http://localhost:5000/callback')

@app.route('/callback')
def callback():
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    session['user'] = user
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/get_suggestions', methods=['GET'])
def get_suggestions():
    song_name = request.args.get('song_name', '').lower().strip()
    
    mask = (
        all_songs['Track Name']
        .str.lower()
        .fillna('')
        .str.contains(song_name, regex=False, na=False)
    )
    
  
    matched_songs = all_songs[mask][['Track Name', 'Artist Name(s)']].drop_duplicates().head(10)
    
    suggestions = [
        f"{row['Track Name']} by {row['Artist Name(s)']}" 
        for _, row in matched_songs.iterrows()
    ]
    
    return jsonify({'suggestions': suggestions})

@app.route("/recommend", methods=["POST"])
def recommend():
    song_name = request.form.get("song_name")
    selected_features = json.loads(request.form.get("selected_features", "[]"))
    
    similar_songs = get_similarities(song_name, all_songs, selected_features)
    
    return render_template("index.html", 
                         song_name=song_name,
                         similar_songs=similar_songs)

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