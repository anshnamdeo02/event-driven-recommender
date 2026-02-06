from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

# MovieLens sample titles (first 300 is enough)
movies = [
    "Toy Story (1995)",
    "GoldenEye (1995)",
    "Four Rooms (1995)",
    "Get Shorty (1995)",
    "Copycat (1995)",
    "Shanghai Triad (1995)",
    "Twelve Monkeys (1995)",
    "Babe (1995)",
    "Dead Man Walking (1995)",
    "Richard III (1995)",
]

@router.get("")
def list_items():
    return [
        {"id": i, "title": movies[i % len(movies)]}
        for i in range(1700)
    ]
