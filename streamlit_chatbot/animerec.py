import streamlit as st
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sample anime dataset (expanded for better fallback recommendations)
anime_data = pd.DataFrame({
    "title": [
        "Attack on Titan", "Demon Slayer", "Jujutsu Kaisen", "My Teen Romantic Comedy",
        "Naruto", "One Piece", "Fullmetal Alchemist: Brotherhood", "Death Note"
    ],
    "description": [
        "Humans fight giant Titans in a post-apocalyptic world with intense action and mystery.",
        "A boy becomes a demon slayer to save his sister and avenge his family in a supernatural setting.",
        "A high schooler battles curses after becoming a vessel for a powerful spirit, filled with action and horror.",
        "A loner navigates high school relationships with witty dialogue and romance.",
        "A young ninja dreams of becoming the strongest leader in his village, with action and adventure.",
        "A pirate crew searches for the ultimate treasure in a vast, adventurous world.",
        "Two brothers use alchemy to restore their bodies in a richly detailed fantasy world.",
        "A student uses a supernatural notebook to eliminate criminals, sparking a psychological thriller."
    ],
    "image_url": [
        "https://via.placeholder.com/150",  # Replace with actual image URLs or use Jikan API
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150",
        "https://via.placeholder.com/150"
    ],
    "info": [
        "Epic action series with intense battles and deep lore.",
        "Visually stunning demon-hunting adventure with emotional depth.",
        "Dark fantasy with supernatural battles and complex characters.",
        "Slice-of-life comedy with witty dialogue and romance.",
        "Coming-of-age ninja saga with action and teamwork.",
        "Epic pirate adventure with humor and heart.",
        "Emotional fantasy epic with intricate world-building.",
        "Dark psychological thriller with moral dilemmas."
    ],
    "age_rating": ["TV-MA", "TV-14", "TV-MA", "TV-14", "TV-PG", "TV-14", "TV-14", "TV-14"],
    "release_year": [2013, 2019, 2020, 2013, 2002, 1999, 2009, 2006],
    "crunchyroll_rating": [4.8, 4.7, 4.9, 4.5, 4.6, 4.8, 4.9, 4.7],  # Placeholder: Replace with real data
    "genres": [
        "Action, Drama, Fantasy",
        "Action, Supernatural",
        "Action, Horror, Supernatural",
        "Comedy, Romance, Slice of Life",
        "Action, Adventure, Shounen",
        "Action, Adventure, Comedy",
        "Action, Fantasy, Drama",
        "Mystery, Psychological, Thriller"
    ],
    "watch_url": [
        "https://www.crunchyroll.com/attack-on-titan",
        "https://www.crunchyroll.com/demon-slayer-kimetsu-no-yaiba",
        "https://www.crunchyroll.com/jujutsu-kaisen",
        "https://www.crunchyroll.com/my-teen-romantic-comedy-yahari",
        "https://www.crunchyroll.com/naruto",
        "https://www.crunchyroll.com/one-piece",
        "https://www.crunchyroll.com/fullmetal-alchemist-brotherhood",
        "https://www.crunchyroll.com/death-note"
    ]
})

# Optional: Fetch anime data from Jikan API (MyAnimeList)
def fetch_anime_from_jikan(query):
    try:
        response = requests.get(f"https://api.jikan.moe/v4/anime?q={query}&limit=3")
        response.raise_for_status()
        data = response.json()
        anime_list = []
        for item in data["data"]:
            anime_list.append({
                "title": item["title"],
                "description": item["synopsis"] or "No description available.",
                "image_url": item["images"]["jpg"]["image_url"],
                "info": item["synopsis"][:200] + "..." if item["synopsis"] else "No info available.",
                "age_rating": item.get("rating", "TV-14"),
                "release_year": item["year"] or 2000,
                "crunchyroll_rating": 4.0,  # Placeholder: Jikan doesn't provide Crunchyroll ratings
                "genres": ", ".join([genre["name"] for genre in item["genres"]]),
                "watch_url": "https://www.crunchyroll.com"  # Placeholder: Replace with actual streaming link
            })
        return pd.DataFrame(anime_list)
    except Exception as e:
        st.warning(f"Error fetching from Jikan API: {str(e)}. Using local dataset.")
        return anime_data

# Function to get anime recommendations using TF-IDF and cosine similarity
def get_anime_recommendations(description):
    # Combine local dataset with Jikan API results (optional)
    search_data = fetch_anime_from_jikan(description)
    combined_data = pd.concat([anime_data, search_data], ignore_index=True).drop_duplicates(subset=["title"])

    # TF-IDF vectorization for descriptions
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(combined_data["description"].fillna(""))
    user_tfidf = vectorizer.transform([description])

    # Calculate cosine similarity
    similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
    top_indices = np.argsort(similarities)[-3:][::-1]  # Get top 3 matches
    recommended_titles = combined_data.iloc[top_indices]["title"].tolist()
    
    return recommended_titles if recommended_titles else combined_data["title"].head(3).tolist()

# Initialize session state for favorites and to-watch list
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "to_watch" not in st.session_state:
    st.session_state.to_watch = []

# Streamlit app layout
st.title("🎬 Anime Recommendation System 🍿")
st.markdown("Discover anime tailored to your preferences!")

# Sidebar for favorites and to-watch list
st.sidebar.header("Your Favorites")
if st.session_state.favorites:
    for title in st.session_state.favorites:
        st.sidebar.write(f"- {title}")
else:
    st.sidebar.write("No favorites yet.")

st.sidebar.header("Your To-Watch List")
if st.session_state.to_watch:
    for title in st.session_state.to_watch:
        st.sidebar.write(f"- {title}")
else:
    st.sidebar.write("No anime in your to-watch list yet.")

# User input for anime description
st.header("Describe Your Anime Preferences")
user_description = st.text_area("Enter a description of the anime you want (e.g., 'action-packed fantasy with strong female lead'):")
if st.button("Get Recommendations"):
    if user_description:
        with st.spinner("Generating recommendations..."):
            recommended_titles = get_anime_recommendations(user_description)
            st.session_state.recommendations = recommended_titles
    else:
        st.error("Please enter a description to get recommendations.")

# Display trending anime below the search bar
st.header("Popular/Trending Anime")
trending_anime = anime_data.sample(3)  # Replace with actual trending data (e.g., Jikan API /top/anime)
cols = st.columns(3)
for idx, anime in trending_anime.iterrows():
    with cols[idx % 3]:
        st.image(anime["image_url"], width=100)
        st.write(f"**{anime['title']}**")
        st.write(f"Rating: {anime['crunchyroll_rating']}/5")

# Display recommendations
if "recommendations" in st.session_state and st.session_state.recommendations:
    st.header("Recommended Anime")
    for title in st.session_state.recommendations:
        if title in anime_data["title"].values:
            anime = anime_data[anime_data["title"] == title].iloc[0]
            st.subheader(anime["title"])
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(anime["image_url"], width=150)
            with col2:
                st.write(f"**Info**: {anime['info']}")
                st.write(f"**Age Rating**: {anime['age_rating']}")
                st.write(f"**Release Year**: {anime['release_year']}")
                st.write(f"**Crunchyroll Rating**: {anime['crunchyroll_rating']}/5")
                st.write(f"**Genres**: {anime['genres']}")
                if st.button(f"Watch {anime['title']} on Crunchyroll", key=f"watch_{title}"):
                    st.markdown(f"[Click here to watch]({anime['watch_url']})")
                if st.button(f"Favorite {anime['title']}", key=f"fav_{title}"):
                    if title not in st.session_state.favorites:
                        st.session_state.favorites.append(title)
                        st.success(f"{title} added to favorites!")
                if st.button(f"Add {anime['title']} to To-Watch List", key=f"watchlist_{title}"):
                    if title not in st.session_state.to_watch:
                        st.session_state.to_watch.append(title)
                        st.success(f"{title} added to to-watch list!")