# CineMatch — Rule-Based Movie Recommendation System

## Project overview
CineMatch is a beginner-friendly AI practical mini-project. It recommends movies by applying explicit IF–THEN-style rules to user preferences. It does not train a machine-learning model.

## Features
- 30-record movie CSV dataset
- Genre, language, mood and minimum-rating filters
- Rule-based matching and ranking
- Explanation of why a movie was recommended
- Empty-result guidance
- Download recommendations as CSV
- Interactive Streamlit web interface

## Requirements
- Python 3.10 or newer recommended
- Streamlit
- Pandas

## Setup on Windows
Open a terminal in this folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install streamlit pandas
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Project files
- `app.py` — user interface
- `recommender.py` — rule engine and ranking
- `movies.csv` — local movie knowledge base
- `README.md` — documentation

## Example tests
1. Genre = Sci-Fi, Language = English, Mood = Adventurous, Rating = 7.0
2. Genre = Comedy, Language = Hindi, Mood = Funny, Rating = 6.0
3. Genre = Romance, Language = Hindi, Mood = Romantic, Rating = 7.0
4. Genre = Horror, Language = English, Mood = Funny, Rating = 7.0 (should return no exact matches; try broadening preferences)

## Rule logic
- If the minimum rating is not met, skip the movie.
- If a chosen language does not match, skip the movie.
- If a chosen genre is not among the movie's genres, skip the movie.
- If a chosen mood is not among the movie's moods, skip the movie.
- Award points for matching preferences and a high rating; sort by score and rating.

## Limitations
- The dataset is small and manually prepared for demonstration.
- Recommendations depend on the written rules and dataset labels.
- No personalization from user history and no machine learning are used.
