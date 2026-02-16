import numpy as np
import pandas as pd
from backend.app.services.ml_service import hybrid_recommend

ratings = pd.read_csv(
    "ml/data/ml-100k/u.data",
    sep="\t",
    names=["user", "item", "rating", "timestamp"]
)

ratings["user"] -= 1
ratings["item"] -= 1


def precision_at_k(k=10):
    users = ratings["user"].unique()[:50]  # sample users
    precisions = []

    for u in users:
        gt_items = set(
            ratings[
                (ratings.user == u) & (ratings.rating >= 4)
            ]["item"].tolist()
        )

        if not gt_items:
            continue

        recs = set(hybrid_recommend(int(u), k))

        hits = len(recs & gt_items)
        precisions.append(hits / k)

    print(f"Precision@{k} =", np.mean(precisions))


if __name__ == "__main__":
    precision_at_k(10)
