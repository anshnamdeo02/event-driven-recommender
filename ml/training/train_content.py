import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# MovieLens column names
cols = [
    "movie_id","title","release_date","video_release","url",
    "unknown","Action","Adventure","Animation","Children",
    "Comedy","Crime","Documentary","Drama","Fantasy",
    "Film-Noir","Horror","Musical","Mystery","Romance",
    "Sci-Fi","Thriller","War","Western"
]

# Load movie metadata
items = pd.read_csv(
    "ml/data/ml-100k/u.item",
    sep="|",
    encoding="latin-1",
    names=cols
)

# Genre features
genre_cols = cols[5:]
genre_matrix = items[genre_cols].values

# Cosine similarity
similarity = cosine_similarity(genre_matrix)

# Save artifact
with open("ml/artifacts/content_similarity.pkl","wb") as f:
    pickle.dump(similarity,f)

print("✅ Content similarity model saved")
