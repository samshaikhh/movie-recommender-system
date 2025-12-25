import streamlit as st
import pickle
import pandas as pd
import requests
import base64
st.set_page_config(page_title="GeniusX",page_icon='🎬')

st.title('🎬 Movie Recommender System')

def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        /* Background image */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}

        /* Headings */
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6 {{
            color: white;
        }}

        /* Streamlit button */
        div.stButton > button {{
            color: white;
            background-color: red;
            border-radius: 8px;
            font-weight: bold;
            border: none;
        }}

        div.stButton > button:hover {{
            background-color: darkred;
        }}

        /* Mobile screens */
        @media only screen and (max-width: 768px) {{
            .stApp {{
                background-size: cover;
                background-position: center;
                background-attachment: scroll;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("image.jpeg")





# fetch poster
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

def details(movie_id):
    director = "Not Available"
    main_actor = 'Not Available'
    release_date = "No Available"
    try:
        movie_response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4ba10b19e27e128814cbc0b98281f1b4&language=en-US",timeout=5).json()

        release_date = movie_response.get("release_date","Not Available")
        credits_response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=4ba10b19e27e128814cbc0b98281f1b4",timeout=5).json()

        for person in credits_response.get('crew',[]):
            if person.get('job')=='Director':
                director = person.get('name')
                break

        # main character    
        cast_list = credits_response.get('cast',[])
        if cast_list:
            main_actor = cast_list[0].get('name','Not Available')


    except Exception as e:
        pass
    return main_actor , director , release_date     


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[0:12]
    
    recommended_details = []
    recommended_movies = []
    recommended_movie_posters = []
    recommended_movie_trailers = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_details.append(details(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_trailers.append(fetch_trailer(movie_id))

    return  recommended_details,  recommended_movies, recommended_movie_posters, recommended_movie_trailers



movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

search = st.subheader('✨ Explore Top Movie Recommendations')
selected_movie_name = st.selectbox("",movies['title'].values)

if st.button("Recommend"):
    details_list, names, posters, trailers = recommend(selected_movie_name)

    i = 0
    while i < 12:
        cols = st.columns(4)

        for col in cols:
            if i < 12:
                with col:
                    # Movie Title
                    st.markdown(
                        f"<h5 style='text-align:center; min-height:60px'>{names[i]}</h5>",
                        unsafe_allow_html=True
                    )

                    # Poster → Trailer
                    st.markdown(
                        f"""
                        <a href="{trailers[i]}" target="_blank">
                            <img src="{posters[i]}" style="width:100%; border-radius:10px;">
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

                    # Movie Details
                    with st.expander("🎬 Movie Details"):
                        main_actor ,director, release_date = details_list[i]
                        st.markdown(f"""
                        🎬 <b>Title:</b> {names[i]}<br>
                        🦸🏼 <b>Character:</b> {main_actor}<br>
                        🎬 <b>Director:</b> {director}<br>
                        📅 <b>Release Date:</b> {release_date}<br>
                        """, unsafe_allow_html=True)


                i += 1



# Telegram button
telegram_link1 = "tg://resolve?domain=Isfjyhehbot"
telegram_link2 = "tg://resolve?domain=M4MoviezzBot"

st.title('🍿 Start Streaming Now')

st.subheader('Redirects to our Telegram bot where you can search, watch, or download movies')


st.markdown("""<i>Select a Telegram bot to unlock unlimited movies for streaming or download</i>""",unsafe_allow_html=True)

st.link_button(
    "🎬 BOT 1!",
    telegram_link1
)
st.link_button(
    "🎬 BOT 2!",
    telegram_link2
)
st.markdown('''<i>Website where you can download movies without subscription</i>''',unsafe_allow_html=True)
st.link_button(
        "🎬 Moviesmode!",
        'https://moviesmod.cards/'
    )

st.link_button(
        '🎬 Vegamovies!',
        'https://vega-r.com/hollywood-movies/'
    )


