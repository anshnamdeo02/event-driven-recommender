import pickle
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix

from backend.app.services.realtime_boost import get_recent_boosts


# =========================
# 1️⃣ LOAD MODELS
# =========================

with open("ml/artifacts/cf_model.pkl", "rb") as f:
    cf_model = pickle.load(f)

with open("ml/artifacts/content_similarity.pkl", "rb") as f:
    similarity = pickle.load(f)


# =========================
# 2️⃣ LOAD RATINGS DATA
# =========================

ratings = pd.read_csv(
    "ml/data/ml-100k/u.data",
    sep="\t",
    names=["user", "item", "rating", "timestamp"]
)

ratings["user"] -= 1
ratings["item"] -= 1

num_users = ratings["user"].max() + 1
num_items = ratings["item"].max() + 1

matrix = coo_matrix(
    (ratings["rating"],
     (ratings["user"], ratings["item"])),
    shape=(num_users, num_items)
).tocsr()


# =========================
# 🔑 HELPER: MAP UUID → INDEX
# =========================

def map_user(user_id):
    """
    Convert UUID/string user_id into valid matrix index
    """
    if isinstance(user_id, str):
        return abs(hash(user_id)) % matrix.shape[0]
    return int(user_id) % matrix.shape[0]


# =========================
# 3️⃣ CF ONLY RECOMMENDER
# =========================

def recommend_for_user(user_id, k: int = 10):

    user_index = map_user(user_id)

    recs, _ = cf_model.recommend(
        user_index,
        matrix[user_index],
        N=k
    )

    return list(map(int, recs))


# =========================
# 4️⃣ HYBRID + REALTIME
# =========================

def hybrid_recommend(
    user_id,
    k: int = 10,
    alpha: float = 0.7
):

    user_index = map_user(user_id)

    # --------------------
    # CF SCORES
    # --------------------
    cf_items, cf_scores = cf_model.recommend(
        user_index,
        matrix[user_index],
        N=50
    )

    cf_scores = dict(zip(cf_items, cf_scores))

    if cf_scores:
        max_cf = max(cf_scores.values())
        if max_cf > 0:
            cf_scores = {i: s / max_cf for i, s in cf_scores.items()}

    # --------------------
    # CONTENT SCORES
    # --------------------
    user_data = ratings[ratings.user == user_index]

    liked_items = user_data[user_data.rating >= 4]["item"].tolist()

    cb_scores = {}

    for liked in liked_items:
        sims = similarity[liked]

        for item_id, sim in enumerate(sims):
            if item_id == liked:
                continue

            cb_scores[item_id] = (
                cb_scores.get(item_id, 0) + float(sim)
            )

    if cb_scores:
        max_cb = max(cb_scores.values())
        if max_cb > 0:
            cb_scores = {i: s / max_cb for i, s in cb_scores.items()}

    # --------------------
    # FUSION
    # --------------------
    all_items = set(cf_scores) | set(cb_scores)

    hybrid_scores = {}

    for item in all_items:
        hybrid_scores[item] = (
            alpha * cf_scores.get(item, 0) +
            (1 - alpha) * cb_scores.get(item, 0)
        )

    # --------------------
    # REAL-TIME BOOSTS
    # --------------------
    boosts = get_recent_boosts(user_id)

    for item, boost in boosts.items():
        hybrid_scores[item] = (
            hybrid_scores.get(item, 0) + 0.1 * boost
        )

    # --------------------
    # RANK
    # --------------------
    ranked = sorted(
        hybrid_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [int(item) for item, _ in ranked[:k]]
