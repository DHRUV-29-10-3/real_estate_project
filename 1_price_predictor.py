import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Price Prediction Module"
)

st.title("🔮 Price Prediction App")

with open('prediction_sys/df.pkl', 'rb') as f:
    df = pickle.load(f)

with open('prediction_sys/pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)


st.header('Enter your inputs')

#1) property_type
property_type = st.selectbox("Property type : ", df['property_type'].unique().tolist())

#2) sector
sector = st.selectbox("Sector :", sorted(df['sector'].unique().tolist()))

#3 bedroom
bedroom = float(st.selectbox("number of bedroom :", sorted(df['bedRoom'].unique().tolist())))

#4 bathroom
bathroom = float(st.selectbox("number of bathroom :", sorted(df['bathroom'].unique().tolist())))

#5) balcony
balcony = st.selectbox("number of balconies :", sorted(df['balcony'].unique().tolist()))

#6) age_possession
age_possession = st.selectbox("Property age :", sorted(df['agePossession'].unique().tolist()))

#7) builtup area
built_up_area = float(st.number_input("Built up area :", ))

#8) servant_room
servant_room = st.selectbox("servant room :", ['Yes','No'])

#9) store_room
store_room = st.selectbox("store room :", ['Yes','No'])

#10) furnishing_type
furnishing_type = st.selectbox("furnishing type :", sorted(df['furnishing_type'].unique().tolist()))

#11) luxury_category
luxury_category = st.selectbox("luxury categorye :", sorted(df['luxury_category'].unique().tolist()))

#12) floor_type
floor_type = st.selectbox("floor type :", sorted(df['floor_category'].unique().tolist()))


if st.button('Predict'):

    values = [[property_type, sector, bedroom, bathroom, balcony, age_possession, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_type]]

    cols = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
           'agePossession', 'built_up_area', 'servant room', 'store room',
           'furnishing_type', 'luxury_category', 'floor_category']

    data = pd.DataFrame(values, columns=cols)

    st.dataframe(data)

    data['servant room'] = data['servant room'].replace(['Yes','No'],[1,0])
    data['store room'] = data['store room'].replace(['Yes', 'No'], [1, 0])

    price = np.expm1(pipeline.predict(data))[0]

    low = price - 0.22
    high = price + 0.22

    low = round(low,2)
    high = round(high,2)

    st.write("The price of flat is between {} Cr and {} Cr".format(low, high))

