import re
import os
import sys
import warnings
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.abspath(os.path.join(parent_dir, 'statistics_dir')))

from statistics_dir.statistics import *

from config import PROCESSED_DATA_FILE, TAG


import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def plot_top_percentage(df, x_label, title, rotation=0):

    top_df = df.sort_values(by='Percentage', ascending=False).head(20)
    
    # Create the bar plot
    bars = plt.bar(top_df.iloc[:, 0], top_df['Percentage'], color='skyblue')
    
    # Add annotations to each bar
    for ii, bar in enumerate(bars):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2,yval, top_df.iloc[ii]['Frequency'], ha='center', va='bottom')
    
    plt.xlabel(x_label)
    plt.ylabel('Percentage')
    plt.title(title)
    
    if rotation != 0:
        plt.xticks(rotation=rotation)
    
    plt.tight_layout()
    
    st.pyplot(plt)


df = pd.read_csv(PROCESSED_DATA_FILE, encoding='utf-8')

st.title(f"{TAG} Statistics".upper())

# Additional analyses
options = st.sidebar.radio("Select Analysis",["General", "Known Sentiment", "Known Artist"])


# Most Common Words
if options == "General":
   # st.title("Most Common Words in Bachata Lyrics")
    artist_stat, norm_words_stat, diff_artists_num, sentiment_dist, avg_words_per_song = general_statistics(df)

    analysis_option = st.sidebar.selectbox("Select analysis", ["General", "Sentiment", "Artist"])

    if analysis_option == "General":
        plot_top_percentage(df=norm_words_stat,x_label='Words',title='Words Percentage',rotation=90)

    elif analysis_option == "Sentiment":
        plot_top_percentage(df=sentiment_dist, x_label='Sentiment', title='Sentiment Percentage',rotation=0)
    
    elif analysis_option == "Artist":
        plot_top_percentage(df=artist_stat, x_label='Artist', title='Artist Percentage', rotation=90)