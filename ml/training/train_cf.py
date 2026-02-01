import pandas as pd
import implicit
from scipy.sparse import coo_matrix
import pickle

# Load ratings
ratings = pd.read_csv(
    "ml/data/ml-100k/u.data",
    sep="\t",
    names=["user", "item", "rating", "timestamp"]
)

print("Ratings loaded:", ratings.shape)

# Convert to sparse matrix
matrix = coo_matrix(
    (ratings["rating"],
     (ratings["user"], ratings["item"]))
)

print("Sparse matrix built")

# Train ALS
model = implicit.als.AlternatingLeastSquares(
    factors=20,
    regularization=0.1,
    iterations=20
)

model.fit(matrix)

print("Model trained")

# Save model
with open("ml/artifacts/cf_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ CF model saved to ml/artifacts/")
