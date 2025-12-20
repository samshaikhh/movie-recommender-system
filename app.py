import streamlit as st
import pickle
import pandas as pd
import requests
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    /* Center content */
    section.main > div {
        padding-top: 2rem;
    }

    /* Selectbox & button */
    div[data-baseweb="select"] > div {
        background-color: #1c1f26;
        color: white;
    }

    button[kind="primary"] {
        background-color: #E50914;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }

    button[kind="primary"]:hover {
        background-color: #b20710;
    }

    /* Movie poster hover effect */
    img {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    img:hover {
        transform: scale(1.05);
        box-shadow: 0px 10px 30px rgba(229,9,20,0.6);
    }

    /* Movie title */
    h5 {
        color: #ffffff;
        font-weight: 600;
    }

    /* Telegram section */
    .telegram-box {
        background-color: #1c1f26;
        padding: 20px;
        border-radius: 12px;
        margin-top: 30px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)




def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4ba10b19e27e128814cbc0b98281f1b4&language=en-US",
            timeout=5
        )
        data = response.json()
        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    except:
        pass

    return "https://via.placeholder.com/300x450?text=No+Image"



def fetch_trailer(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=4ba10b19e27e128814cbc0b98281f1b4&language=en-US",
            timeout=5
        )
        data = response.json()

        for video in data.get("results", []):
            if (
                video["site"] == "YouTube"
                and video["type"] == "Trailer"
                and video["official"]
            ):
                return f"https://www.youtube.com/watch?v={video['key']}"

    except:
        pass

    return "https://www.youtube.com"



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:5]

    recommended_movies = []
    recommended_movie_posters = []
    recommended_movie_trailers = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_trailers.append(fetch_trailer(movie_id))

    return recommended_movies, recommended_movie_posters, recommended_movie_trailers



movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


st.markdown(
    "<h1 style='color:#E50914; text-align:center;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True
)

selected_movie_name = st.selectbox("Search movies",movies['title'].values)

if st.button("Recommend"):
    names, posters, trailers = recommend(selected_movie_name)
    st.markdown(
    """
    <h3 style="
        color: #E50914;
        font-weight: bold;
        text-align: center;
        letter-spacing: 0.5px;
        margin-bottom: 30px;
    ">
    ❤️ Loved a recommendation? Click on the movie image to dive straight into its trailer!
    </h3>
    """,
    unsafe_allow_html=True
)



    cols = st.columns(4)

    for i in range(4):
        with cols[i]:
            st.markdown(
                f"<h5 style='text-align:center; min-height:60px'>{names[i]}</h5>",
                unsafe_allow_html=True
            )

            # Clickable poster  YouTube trailer
            st.markdown(
                f"""
                <a href="{trailers[i]}" target="_blank">
                    <img src="{posters[i]}" style="width:100%; border-radius:10px;">
                </a>
                """,
                unsafe_allow_html=True
            )

    # Telegram button
    telegram_link1 = "tg://resolve?domain=Isfjyhehbot"
    telegram_link2 = "tg://resolve?domain=M4MoviezzBot"
    st.markdown(
    """
    <div class="telegram-box">
        <h2 style="color:#E50914;">🍿 Start Streaming Now</h2>
        <p>Redirects to our Telegram bot where you can search, watch, or download movies.</p>
    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown(
    """
    <style>
    /* Link button styling */
    a[data-testid="stLinkButton"] > button {
        padding: 16px 30px;
        font-size: 18px;
        margin-top: 20px;
        margin-bottom: 30px;
        border-radius: 12px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    
    st.write("Select a Telegram bot to unlock unlimited movies for streaming or download.")

    st.link_button(
    "🎬 BOT 1!",
    telegram_link1
)
    st.link_button(
    "🎬 BOT 2!",
    telegram_link2
)
    st.write('Website where you can download without subscription')
    st.link_button(
        "🎬 Moviesmode!",
        'https://moviesmod.cards/'
    )

    st.link_button(
        '🎬 Vegamovies!',
        'https://vega-r.com/hollywood-movies/'
    )



