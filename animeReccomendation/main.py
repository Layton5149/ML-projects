import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.neighbors import NearestNeighbors
import flask
from flask import render_template , url_for

app = flask.Flask(__name__)


originalData = pd.read_csv("dataset/mal_anime.csv")

#select only some colums
data = originalData[["myanimelist_id", "title", "description", "image", "Type", "Genres", "Studios", "Producers", "Rating", "Popularity", "source_url"]]

featureData = data.dropna()
data = data.dropna()

movieNames = []

for i in range( len(data)// 10):
    movieNames.append(data.iloc[i]['title'])

#convert genres, studios, producers to numberics
data['Genres'] = data['Genres'].astype('category').cat.codes
data['Studios'] = data['Studios'].astype('category').cat.codes
data['Producers'] = data['Producers'].astype('category').cat.codes
data['Rating'] = data['Rating'].astype('category').cat.codes


#use k nearest neigbours the data based on genres, studios, producers, rating and popularity

features = data[['Genres', 'Studios', 'Producers', 'Rating']]
nbrs = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(features)

def find_similar_animes(anime_title, n_neighbors=6):
    movieList = []
    # find the index of the anime with the given title
    idx = data.index[data['title'] == anime_title]
    if len(idx) == 0:
        print(f"Anime with title '{anime_title}' not found.")
        return
    idx = idx[0]
    query_vec = features.iloc[idx].values.reshape(1, -1)

    # find neighbors (including itself)
    _, indices = nbrs.kneighbors(query_vec, n_neighbors=n_neighbors)

    print(f"Anime: {data.iloc[idx]['title']}")
    print("Similar animes:")

    for neighbor_idx in indices[0]:
        moveiFeaturesList = []

        if neighbor_idx == idx:
            continue  

        title = featureData.iloc[neighbor_idx]['title']
        image = featureData.iloc[neighbor_idx]['image']
        decription = featureData.iloc[neighbor_idx]['description']
        url_source = featureData.iloc[neighbor_idx]['source_url']
        genres = featureData.iloc[neighbor_idx]['Genres']
        studios = featureData.iloc[neighbor_idx]['Studios']
        producers = featureData.iloc[neighbor_idx]['Producers']

        moveiFeaturesList.append(title)
        moveiFeaturesList.append(image)
        moveiFeaturesList.append(decription)
        moveiFeaturesList.append(url_source)
        moveiFeaturesList.append(genres)
        moveiFeaturesList.append(studios)
        moveiFeaturesList.append(producers)

        movieList.append(moveiFeaturesList)
    
    print (movieList)
    return movieList


@app.route('/')
def home():
    return render_template("index.html")


@app.post('/recommend')
def reccomend():
    # get the anime title from the body of the request
    anime_title = flask.request.json.get('title')
    print(f"Received anime title: {anime_title}")
    return find_similar_animes(anime_title)

find_similar_animes("Naruto")

if __name__ == '__main__':
    app.run(debug=True)
