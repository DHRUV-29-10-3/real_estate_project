import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Recommender System"
)

st.title("🤖🔍 Recommender System")

st.header("Select location and radius")

location_df = pickle.load(open("recommender_sys/location_data.pkl", "rb"))
cosine_sim1 = pickle.load(open("recommender_sys/cosine_sim1.pkl", "rb"))
cosine_sim2 = pickle.load(open("recommender_sys/cosine_sim2.pkl", "rb"))
cosine_sim3 = pickle.load(open("recommender_sys/cosine_sim3.pkl", "rb"))


def recommend_properties_with_scores(property_name, top_n=247):
    cosine_sim_matrix = 0.5*cosine_sim1 + 0.8*cosine_sim2 + 1*cosine_sim3


    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df.head(5)



locations = st.selectbox("Locations : ", sorted(location_df.columns))

radius = float(st.number_input("Radius in kms : "))

if st.button("🔍 Search") :

    nearby_loc = location_df[location_df[locations] <= radius*1000][locations].to_dict()
    appartments = []
    for i in nearby_loc:
        print(i,nearby_loc[i])
        st.text(str("place : ") + str(i) + " distance : " + str(round(nearby_loc[i]/1000,2)) + ' kms')


st.header("Recommend locations")

selecting_apartments = st.selectbox("Apartments : ", sorted(location_df.index.to_list()))

if st.button("Recommend"):
    st.dataframe(recommend_properties_with_scores(selecting_apartments))

