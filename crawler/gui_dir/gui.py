import re
import os
import sys
import pandas as pd
import streamlit as st

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.abspath(os.path.join(parent_dir, 'statistics_dir')))

from statistics_dir.statistics import *
from config import FINAL_DATA_FILE, TAG
from conclusion_text import * 
from gui_helper import *

df = pd.read_csv(FINAL_DATA_FILE, encoding='utf-8')
df['norm_words'] = df['norm_words'].apply(lambda x: eval(x))


# Additional analyses
options = st.sidebar.radio("Select Analysis",["General", "Known Sentiment", "Known Artist"])
artist_stat, norm_words_stat, diff_artists_num, sentiment_single_dist, sentiment_avg_dist, avg_words_per_song = general_statistics(df)


# Most Common Words
if options == "General":
    analysis_option = st.sidebar.selectbox("Select analysis", ["General", "Word", "Sentiment", "Artist"])

    if analysis_option == "General":
        st.markdown(f"<h1 style='text-align: center;'>{TAG.upper()} STATISTICS</h1>", unsafe_allow_html=True)
        st.write("Welcome to the Bachata statistics:")
        wordcloud_func(norm_words_stat)
        single_sentiment_markdown = max_sentiment_to_text(sentiment_single_dist)
        avg_sentiment_markdown = avg_sentiment_to_text(sentiment_avg_dist)
        
        st.markdown(GENERAL_GENERAL.format(len_songs=len(df), len_diff_artists=diff_artists_num, \
                                           single_sentiment=single_sentiment_markdown, avg_sentiment=avg_sentiment_markdown, avg_song_len=avg_words_per_song))

    elif analysis_option == "Word":
        st.markdown('<h4 style="font-size:15px;text-align: center;">Frequency & Percentage as function of the normalized words form</h4>', unsafe_allow_html=True)
        plot_top_percentage(df=norm_words_stat,x_label='Words',title='Words Percentage',rotation=90)

        st.subheader("Conclusions")
        st.markdown(GENERAL_WORD)

    elif analysis_option == "Sentiment":
        st.write("This graph is the average song sentiment (Averaging all the sentiments of the songs):")
        plot_top_percentage(df=sentiment_avg_dist, x_label='Sentiment', title='Average Sentiment Percentage',annot_bar=False, rotation=0)

        st.write("The maximum sentiment percentage is selected as the single song sentiment:")        
        plot_top_percentage(df=sentiment_single_dist, x_label='Sentiment', title='Single Sentiment Percentage',rotation=0)


    elif analysis_option == "Artist":
        plot_top_percentage(df=artist_stat, x_label='Artist', title='Artist Percentage', rotation=90)
        st.subheader("Conclusions")
        st.markdown(GENERAL_ARTIST)

if options == "Known Artist":
    artist_names = artist_stat['all_artists'].tolist()
    artist_option = st.sidebar.selectbox("Artist name", artist_names)

    ka_norm_words_stat, ka_num_songs_per_artist, ka_single_sentiment_dist, ka_avg_sentiment_dist, ka_avg_words_per_song =  artist_statistics(df, artist_option)
    plot_top_percentage(df=ka_norm_words_stat, x_label='Words',title='Words Percentage',rotation=90)
    ka_single_sentiment_markdown = max_sentiment_to_text(ka_single_sentiment_dist)
    ka_avg_sentiment_markdown = avg_sentiment_to_text(sentiment_avg_dist)

    st.markdown(ARTIST_GENERAL.format(len_songs=ka_num_songs_per_artist, single_sentiment=ka_single_sentiment_markdown, avg_sentiment = ka_avg_sentiment_markdown, avg_song_len=ka_avg_words_per_song))

