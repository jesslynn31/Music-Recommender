
**Introduction**
HarmoniFind is a personal passion project built out of my love for music and recommendation systems. 
This web application uses the K-Nearest Neighbors (KNN) algorithm to help users discover new music by identifying songs 
that are most similar to a selected track based on various Spotify audio features—such as tempo, loudness, melody, and more.



Below is the main project page: 
![image](https://github.com/user-attachments/assets/11431922-a3cd-425c-a5b5-547adb7e282a)




**How It Works**

Enter the name of a song into the search bar. (A script will come up with suggestions for the song name)

Select one or more musical features (e.g., tempo, danceability, energy) by clicking on them.

Selected features are highlighted in a darker pink color.

Click Submit to receive a list of recommended songs that are similar to your input, based on the chosen attributes.


![image](https://github.com/user-attachments/assets/d6463309-b038-40d7-b1c1-69532608a089)
![image](https://github.com/user-attachments/assets/4265e51a-d51a-4bd1-b710-ebca847e7c38)


The similar songs pop up in the recommended song box below: 

![image](https://github.com/user-attachments/assets/4b7f53cc-221d-4047-ac33-82082b7c7ccd)


**User Authentication:**

HarmoniFind now includes a functional login and registration system. While user accounts are currently limited in functionality, authentication features are in place:

Users can register with a username, email, and password.

User credentials are stored securely using PostgreSQL.

Passwords are hashed and never stored in plain text, ensuring secure handling of sensitive data.

The user interface of HarmoniFind is styled using a free, open-source HTML/CSS theme from FreeFrontend.com. 
This theme provided a clean and modern layout that was adapted to fit the functionality of the application.
Colors were altered a bit to fit HarmoniFind's pink theme. 


Future updates will include more personalized features tied to user accounts, such as saved preferences, similarity votes, or custom playlists.

![image](https://github.com/user-attachments/assets/f593adbf-4e4d-4fa5-a695-dc4935d5e02e)



**Purpose**
The purpose of HarmoniFind is simple. It is to match users with similar songs and help 
them explore the world of music easier, one algorithm run at a time. 

