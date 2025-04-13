import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

st.set_page_config(
    page_title="Analytics Module"
)


st.title("📊 Real Estate Analytics")

final_df = pd.read_csv("analytics_directory/final_df.csv")
wordcloud_df = pd.read_csv("analytics_directory/worldcloud_df.csv")

st.header("Sector price(in crores) per sqft geomap")

group_df = final_df.groupby('sector', as_index=False).agg({
        'price': 'mean',
        'built_up_area': 'mean',
        'price_per_sqft': 'mean',
        'latitude': 'mean',
        'longitude': 'mean'
    })

fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                            color_continuous_scale=px.colors.cyclical.IceFire, zoom=10.5,
                            mapbox_style="open-street-map", text='sector')
st.plotly_chart(fig, use_container_width=True)

st.header("Feature wordcloud")
sector_value = st.selectbox('Sector : ', sorted(wordcloud_df['sector'].unique().tolist()))

import ast
main = []
for item in wordcloud_df[wordcloud_df['sector'] == sector_value]['features'].dropna().apply(ast.literal_eval):
    main.extend(item)

plt.rcParams["font.family"] = "Arial"
feature_text = ' '.join(main)
wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=set(['s']),  # Any stopwords you'd like to exclude
                          min_font_size=10).generate(feature_text)

fig = plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
st.pyplot(fig)

st.title("")
st.header("Area vs Price(in crores)")
property_type = st.selectbox("Property type :", ['Flat', 'House', 'Both'])
if property_type == 'Both':
    fig = px.scatter(data_frame=final_df,y = 'price', x ='built_up_area', color='bedRoom')
    st.plotly_chart(fig, use_container_width=True)

elif property_type == 'Flat':
    fig = px.scatter(data_frame=final_df[final_df['property_type'] == 'flat'], y='price', x='built_up_area', color='bedRoom')
    st.plotly_chart(fig, use_container_width=True)

else:
    fig = px.scatter(data_frame=final_df[final_df['property_type'] == 'house'], y='price', x='built_up_area', color='bedRoom')
    st.plotly_chart(fig, use_container_width=True)

st.title('')
st.header('BHK Pie Chart')

sector_value = st.selectbox("Sector : ", sorted(final_df['sector'].unique().tolist()+['All']))
if sector_value == 'All':
    fig = px.pie(data_frame=final_df, names='bedRoom')
    st.plotly_chart(fig, use_container_width=True)

else:
    fig = px.pie(data_frame=final_df[final_df['sector'] == sector_value], names='bedRoom')
    st.plotly_chart(fig, use_container_width=True)

st.title('')
st.header('Box plot of BHK and Price(in crores')

fig = px.box(data_frame=final_df[final_df['bedRoom']<=4], x = 'bedRoom', y= 'price')
st.plotly_chart(fig, use_container_width=True)

st.title("")
st.header("side by side displot for property type")
fig, ax = plt.subplots(figsize=(10, 4))
sns.kdeplot(final_df[final_df['property_type'] == 'flat']['price'], label='Flat', ax=ax,fill =True,color='blue')
sns.kdeplot(final_df[final_df['property_type'] == 'house']['price'], label='House', ax=ax,fill = True, color = 'red')
plt.legend()
st.pyplot(fig)
