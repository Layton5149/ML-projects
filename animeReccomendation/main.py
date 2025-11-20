import pandas as pd
import numpy as np
import sklearn as sk

data = pd.read_csv("dataset/mal_anime.csv")

#select only some colums
data = data[["myanimelist_id", "title", "description", "image", "Type", "Genres", "Studios", "Producers", "Rating", "Popularity", "source_url"]]

print (data.count())

data = data.dropna()


print (data.count())

print(data.dtypes)

