import streamlit as st
import pickle

# Load Pickle
with open("Movie_Recommend.pkl", "rb") as f:
    dit = pickle.load(f)

# CSS
st.markdown(
    """
    <style>
    .stMain .stMainBlockContainer{
        padding: 4rem 1rem 2rem;
    } 
    .stHeading h1{
        text-align: center;
        color: #B84042;
    }
    .stSelectbox p{
        font-size:30px;
        font-weight:bold;
    }
    </style>
    """,unsafe_allow_html=True
)

# NLP Function
df = dit["DataSet"]
def Movie_Recommender(movie):
    if movie not in df["Series_Title"].values:
        return None
    
    df_movie = df.copy()
    doc = df_movie.loc[df_movie["Series_Title"] == movie, "Docs"].values[0]
    df_movie = df_movie[df_movie["Series_Title"] != movie]

    df_movie["Similarity"] = df_movie["Docs"].apply(lambda x: doc.similarity(x))
    df_movie.sort_values(by="Similarity", ascending=False, inplace=True)

    titles = df_movie["Series_Title"].head().values
    overviews = df_movie["Overview"].head().values  

    return list(zip(titles, overviews))

# Page UI
st.title("Movie Recommendation System")

movie = st.selectbox("Enter Your Movie Name:", options=dit["Movies"], index=None)
btn = st.button("Search")

if btn:
    recommendations = Movie_Recommender(movie)
    if recommendations is None:
        st.error("Select a Movie!")
    else:
        st.title("Similar Recommendations:")
        c = 1
        for title,overview in recommendations:
            st.subheader(f"{c}. {title}")
            st.write(overview)
            c+=1