import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
import os

api_key = os.getenv('key')

load_dotenv()

def get_poster(id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    dist = similarity[movie_index]
    movies_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[-1])[1:6]
    recs = []
    rec_posters =[]
    for mov in movies_list:
        id = movies.iloc[mov[0]].movie_id
        rec_posters.append(get_poster(id))
        recs.append(movies.iloc[mov[0]].title)
    return recs, rec_posters

movie_dict = pickle.load(open("movie_dict.pkl", 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open("similarity.pkl", 'rb'))

st.title('Movie Recommender')

selected = st.selectbox(
    "Find Your Movie",
    movies['title'].values
)

if st.button("Recommend"):
    recs, rec_posters = recommend(selected)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recs[0])
        st.image(rec_posters[0])
    with col2:
        st.text(recs[1])
        st.image(rec_posters[1])
    with col3:
        st.text(recs[2])
        st.image(rec_posters[2])
    with col4:
        st.text(recs[3])
        st.image(rec_posters[3])
    with col5:
        st.text(recs[4])
        st.image(rec_posters[4])

