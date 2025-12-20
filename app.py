import streamlit as st
import pickle
import pandas as pd
import requests



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


st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox("Search movies",movies['title'].values)

if st.button("Recommend"):
    names, posters, trailers = recommend(selected_movie_name)

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
    telegram_link = "tg://resolve?domain=Isfjyhehbot"
    st.link_button(
        "🎬 Enjoy Unlimited Movies for FREE on Telegram!",
        telegram_link
    )
