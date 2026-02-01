import pickle
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix

K = 10

# Load CF model
with open("ml/artifacts/cf_model.pkl","rb") as f:
    cf_model = pickle.load(f)

# Load content similarity
with open("ml/artifacts/content_similarity.pkl","rb") as f:
    similarity = pickle.load(f)

# Load ratings
ratings = pd.read_csv(
    "ml/data/ml-100k/u.data",
    sep="\t",
    names=["user","item","rating","timestamp"]
)

ratings["user"] -= 1
ratings["item"] -= 1

num_users = ratings["user"].max()+1
num_items = ratings["item"].max()+1

matrix = coo_matrix(
    (ratings["rating"],
     (ratings["user"],ratings["item"])),
    shape=(num_users,num_items)
).tocsr()

user_id = 10  # demo user

# CF recommendations
cf_items,_ = cf_model.recommend(
    user_id,
    matrix[user_id],
    N=K
)

# Find items user liked
liked = ratings[
    (ratings.user==user_id) &
    (ratings.rating>=4)
]["item"].tolist()

# Content-based suggestions
cb_candidates = set()
for item in liked:
    similar = np.argsort(similarity[item])[-5:]
    cb_candidates.update(similar)

# Merge
hybrid = list(dict.fromkeys(
    list(cf_items) + list(cb_candidates)
))[:K]

print("CF recs:",cf_items)
print("Hybrid recs:",hybrid)
