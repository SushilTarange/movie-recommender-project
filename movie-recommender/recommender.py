import pandas as pd

DATA_FILE = "movies.csv"

def load_movies():
    """Load movie records from the local CSV dataset."""
    return pd.read_csv(DATA_FILE)

def recommend_movies(genre="Any", language="Any", mood="Any",
                     min_rating=0.0, limit=10):
    """
    Rule-based recommendation:
    - Selected genre must match one of a movie's genres.
    - Selected language must match exactly.
    - Selected mood must match one of a movie's moods.
    - Rating must be at least the selected minimum.
    Matches are ranked by number of preference matches, then rating.
    """
    movies = load_movies()
    results = []

    for _, movie in movies.iterrows():
        movie_genres = [item.strip() for item in str(movie["genres"]).split("|")]
        movie_moods = [item.strip() for item in str(movie["moods"]).split("|")]

        if float(movie["rating"]) < float(min_rating):
            continue
        if language != "Any" and movie["language"] != language:
            continue
        if genre != "Any" and genre not in movie_genres:
            continue
        if mood != "Any" and mood not in movie_moods:
            continue

        score = 0
        reasons = []
        if genre != "Any" and genre in movie_genres:
            score += 2
            reasons.append(f"matches your {genre} genre")
        if language != "Any" and movie["language"] == language:
            score += 1
            reasons.append(f"is available in {language}")
        if mood != "Any" and mood in movie_moods:
            score += 2
            reasons.append(f"fits your {mood.lower()} mood")
        if float(movie["rating"]) >= 8.0:
            score += 1
            reasons.append("has a rating of 8.0 or above")

        results.append({
            "title": movie["title"],
            "genres": movie["genres"].replace("|", ", "),
            "language": movie["language"],
            "moods": movie["moods"].replace("|", ", "),
            "rating": float(movie["rating"]),
            "description": movie["description"],
            "score": score,
            "reason": "; ".join(reasons) if reasons else "matches your general preferences"
        })

    results.sort(key=lambda item: (item["score"], item["rating"]), reverse=True)
    return results[:limit]

if __name__ == "__main__":
    print("Sample recommendations for Sci-Fi + English + Adventurous:")
    for movie in recommend_movies("Sci-Fi", "English", "Adventurous", 7.0):
        print(f'- {movie["title"]} ({movie["rating"]}) — {movie["reason"]}')
