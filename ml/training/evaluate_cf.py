import pandas as pd
import implicit
import numpy as np
from scipy.sparse import coo_matrix
import pickle

K = 10

# Load train
train = pd.read_csv(
    "ml/data/ml-100k/u1.base",
    sep="\t",
    names=["user", "item", "rating", "timestamp"]
)

# Load test
test = pd.read_csv(
    "ml/data/ml-100k/u1.test",
    sep="\t",
    names=["user", "item", "rating", "timestamp"]
)

# Zero-index IDs
train["user"] -= 1
train["item"] -= 1
test["user"] -= 1
test["item"] -= 1

num_users = train["user"].max() + 1
num_items = train["item"].max() + 1

# Build train matrix
train_matrix = coo_matrix(
    (train["rating"],
     (train["user"], train["item"])),
    shape=(num_users, num_items)
).tocsr()

# Load model
with open("ml/artifacts/cf_model.pkl", "rb") as f:
    model = pickle.load(f)

print("Model loaded")

# Test dictionary
test_items = test.groupby("user")["item"].apply(set).to_dict()

precisions, recalls, ndcgs = [], [], []

for user, true_items in test_items.items():

    recommended, _ = model.recommend(
        user,
        train_matrix[user],
        N=K
    )

    hits = set(recommended) & true_items

    precision = len(hits) / K
    recall = len(hits) / len(true_items)

    dcg = 0
    for i, item in enumerate(recommended):
        if item in true_items:
            dcg += 1 / np.log2(i + 2)

    idcg = sum(1 / np.log2(i + 2)
               for i in range(min(len(true_items), K)))

    ndcg = dcg / idcg if idcg > 0 else 0

    precisions.append(precision)
    recalls.append(recall)
    ndcgs.append(ndcg)

print("\n📊 RESULTS")
print("Precision@10:", np.mean(precisions))
print("Recall@10:", np.mean(recalls))
print("NDCG@10:", np.mean(ndcgs))
