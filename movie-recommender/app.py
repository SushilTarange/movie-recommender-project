import streamlit as st
import pandas as pd
from recommender import recommend_movies, load_movies

st.set_page_config(
    page_title="CineMatch | Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #10121b 0%, #1a1830 55%, #111827 100%); }
.block-container { padding-top: 2rem; max-width: 1200px; }
.hero { padding: 1.5rem 0 1rem 0; }
.hero h1 { font-size: 2.7rem; margin-bottom: .3rem; }
.hero p { color: #b9bfd3; font-size: 1.05rem; }
.movie-card { background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.12);
              border-radius: 16px; padding: 1rem; margin-bottom: .8rem; min-height: 210px; }
.movie-title { font-size: 1.22rem; font-weight: 700; margin-bottom: .35rem; }
.movie-meta { color: #c7cbe0; font-size: .9rem; margin-bottom: .65rem; }
.movie-desc { color: #e5e7eb; }
.reason { color: #a7f3d0; font-size: .88rem; margin-top: .65rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🎬 CineMatch</h1>
  <p>Your preferences. Simple rules. Movie recommendations made for you.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🎯 Your preferences")
    genre = st.selectbox("Preferred genre", [
        "Any", "Action", "Adventure", "Animation", "Comedy", "Crime",
        "Drama", "Horror", "Music", "Romance", "Sci-Fi", "Sport",
        "Thriller", "Mystery"
    ])
    language = st.selectbox("Language", ["Any", "English", "Hindi"])
    mood = st.selectbox("Current mood", [
        "Any", "Adventurous", "Dark", "Emotional", "Funny",
        "Inspirational", "Romantic", "Suspenseful"
    ])
    min_rating = st.slider("Minimum rating", min_value=0.0, max_value=9.0,
                           value=7.0, step=0.5)
    result_count = st.slider("Number of recommendations", 3, 15, 8)
    submitted = st.button("✨ Recommend movies", type="primary", use_container_width=True)
    st.caption("Recommendations are generated using predefined rules, not machine learning.")

all_movies = load_movies()
c1, c2, c3 = st.columns(3)
c1.metric("Movies in dataset", len(all_movies))
c2.metric("Languages", all_movies["language"].nunique())
c3.metric("Recommendation method", "Rule-based")

if "has_recommended" not in st.session_state:
    st.session_state.has_recommended = False

if submitted:
    st.session_state.results = recommend_movies(
        genre=genre,
        language=language,
        mood=mood,
        min_rating=min_rating,
        limit=result_count
    )
    st.session_state.has_recommended = True
    st.session_state.current_preferences = {
        "genre": genre, "language": language, "mood": mood,
        "min_rating": min_rating
    }

st.divider()

if not st.session_state.has_recommended:
    st.subheader("Find your next movie")
    st.write("Choose your preferences in the sidebar, then click **Recommend movies**.")
    st.info("Try: Sci-Fi + English + Adventurous, or Comedy + Hindi + Funny.")
    st.subheader("How the recommendation works")
    st.markdown("""
    1. Read movie details from `movies.csv`.
    2. Apply the selected genre, language, mood, and minimum-rating rules.
    3. Rank matching movies by preference score and rating.
    4. Explain why each movie matched your preferences.
    """)
else:
    results = st.session_state.results
    prefs = st.session_state.current_preferences
    st.subheader("🍿 Your recommendations")
    st.caption(
        f"Preferences: {prefs['genre']} · {prefs['language']} · "
        f"{prefs['mood']} · Minimum rating {prefs['min_rating']:.1f}"
    )
    if not results:
        st.warning("No exact matches found. Try selecting 'Any' for one preference or lowering the minimum rating.")
    else:
        st.success(f"Found {len(results)} matching movie(s).")
        for start in range(0, len(results), 2):
            cols = st.columns(2)
            for col, movie in zip(cols, results[start:start + 2]):
                with col:
                    st.markdown(f"""
                    <div class="movie-card">
                      <div class="movie-title">🎞️ {movie['title']}</div>
                      <div class="movie-meta">⭐ {movie['rating']:.1f}/10 &nbsp; · &nbsp; {movie['language']}</div>
                      <div class="movie-meta"><b>Genres:</b> {movie['genres']}</div>
                      <div class="movie-desc">{movie['description']}</div>
                      <div class="reason">✓ Why recommended: {movie['reason']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        export = pd.DataFrame(results)
        st.download_button(
            "⬇️ Download recommendations as CSV",
            data=export.to_csv(index=False).encode("utf-8"),
            file_name="my_movie_recommendations.csv",
            mime="text/csv"
        )

with st.expander("View dataset"):
    st.dataframe(all_movies, use_container_width=True, hide_index=True)

st.divider()
st.caption("AI Practical Mini-Project · Rule-Based Movie Recommendation System · Python + Pandas + Streamlit")
