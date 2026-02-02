import pandas as pd
from backend.app.db.session import SessionLocal
from backend.app.models.item import Item

db = SessionLocal()

cols = [
    "movie_id","title","release_date","video_release","url",
    "unknown","Action","Adventure","Animation","Children",
    "Comedy","Crime","Documentary","Drama","Fantasy",
    "Film-Noir","Horror","Musical","Mystery","Romance",
    "Sci-Fi","Thriller","War","Western"
]

df = pd.read_csv(
    "ml/data/ml-100k/u.item",
    sep="|",
    encoding="latin-1",
    names=cols
)

for _, row in df.iterrows():

    exists = db.query(Item).filter_by(id=row.movie_id).first()
    if exists:
        continue

    item = Item(
        id=int(row.movie_id),
        title=row.title
    )

    db.add(item)

db.commit()
db.close()

print("✅ Items seeded successfully")
