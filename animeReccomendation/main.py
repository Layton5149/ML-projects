import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.neighbors import NearestNeighbors

data = pd.read_csv("dataset/mal_anime.csv")

#select only some colums
data = data[["myanimelist_id", "title", "description", "image", "Type", "Genres", "Studios", "Producers", "Rating", "Popularity", "source_url"]]

print (data.count())

data = data.dropna()


print (data.count())

print(data.dtypes)

print (f"prodcuers unique: {data['Producers'].nunique()}")
print (f"studios unique: {data['Studios'].nunique()}")
print (f"genres unique: {data['Genres'].nunique()}")

#convert genres, studios, producers to numberics
data['Genres'] = data['Genres'].astype('category').cat.codes
data['Studios'] = data['Studios'].astype('category').cat.codes
data['Producers'] = data['Producers'].astype('category').cat.codes
data['Rating'] = data['Rating'].astype('category').cat.codes

print (data.dtypes)


#use k nearest neigbours the data based on genres, studios, producers, rating and popularity

features = data[['Genres', 'Studios', 'Producers', 'Rating']]
nbrs = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(features)

def find_similar_animes(anime_title, n_neighbors=5):
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
        if neighbor_idx == idx:
            continue  # skip itself
        title = data.iloc[neighbor_idx]["title"]
        print(f"- {title}")


find_similar_animes("Attack on Titan")