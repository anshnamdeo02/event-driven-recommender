import pickle
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix

# Load CF model
with open("ml/artifacts/cf_model.pkl", "rb") as f:
    cf_model = pickle.load(f)

# Load content similarity
with open("ml/artifacts/content_similarity.pkl","rb") as f:
    similarity = pickle.load(f)


# Load ratings to build user-item matrix
ratings = pd.read_csv(
    "ml/data/ml-100k/u.data",
    sep="\t",
    names=["user","item","rating","timestamp"]
)

# zero-index
ratings["user"] -= 1
ratings["item"] -= 1

num_users = ratings["user"].max()+1
num_items = ratings["item"].max()+1

matrix = coo_matrix(
    (ratings["rating"],
     (ratings["user"], ratings["item"])),
    shape=(num_users, num_items)
).tocsr()


def recommend_for_user(user_id: int, k: int = 10):
    recs, scores = cf_model.recommend(
        user_id,
        matrix[user_id],
        N=k
    )

    return list(map(int, recs))

def hybrid_recommend(user_id: int, k: int = 10, alpha: float = 0.7):

    # --------------------
    # 1️⃣ CF recommendations (with scores)
    # --------------------
    cf_items, cf_scores = cf_model.recommend(
        user_id,
        matrix[user_id],
        N=50
    )

    cf_scores = dict(zip(cf_items, cf_scores))

    max_cf = max(cf_scores.values())
    cf_scores = {i: s / max_cf for i, s in cf_scores.items()}

    # --------------------
    # 2️⃣ Content-based scores
    # --------------------
    user_data = ratings[ratings.user == user_id]
    liked_items = user_data[user_data.rating >= 4]["item"].tolist()

    cb_scores = {}

    for liked in liked_items:
        sims = similarity[liked]

        for item_id, sim in enumerate(sims):
            if item_id == liked:
                continue
            cb_scores[item_id] = cb_scores.get(item_id, 0) + sim

    if cb_scores:
        max_cb = max(cb_scores.values())
        cb_scores = {i: s / max_cb for i, s in cb_scores.items()}

    # --------------------
    # 3️⃣ Hybrid fusion
    # --------------------
    all_items = set(cf_scores) | set(cb_scores)

    hybrid_scores = {}
    for item in all_items:
        hybrid_scores[item] = (
            alpha * cf_scores.get(item, 0) +
            (1 - alpha) * cb_scores.get(item, 0)
        )

    # --------------------
    # 4️⃣ Rank
    # --------------------
    ranked = sorted(
        hybrid_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [int(item) for item, _ in ranked[:k]]
