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

# Recommendation Sessions
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
# Index Sessions
if "index" not in st.session_state:
    st.session_state.index = 0

# Output Function
def show_recommendations():
    if st.session_state.recommendations:
        ind = st.session_state.index
        recommendations = st.session_state.recommendations

        with recommend_box.container():
            st.title("Similar Recommendations:")
            st.subheader(f"{ind+1}. {recommendations[ind][0]}")
            st.write(recommendations[ind][1])

            prev,nxt,b = st.columns([0.6,0.6,2])
            # Previous Button
            if prev.button("Previous", key=f"prev_{ind}") and st.session_state.index > 0:
                st.session_state.index -= 1
                show_recommendations()
            # Next Button
            if nxt.button("Next", key=f"next_{ind}") and st.session_state.index < len(recommendations)-1:
                st.session_state.index += 1
                show_recommendations()

# Page UI
st.title("Movie Recommendation System")

movie = st.selectbox("Enter Your Movie Name:", options=dit["Movies"], index=None)
btn = st.button("Search")

if btn:
    recommendations = Movie_Recommender(movie)
    if recommendations is None:
        st.error("Select a Movie!")
    else:
        st.session_state.recommendations = recommendations
        st.session_state.index = 0

# Function Call
recommend_box = st.empty()
show_recommendations()