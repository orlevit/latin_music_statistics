import re
import os
import sys
import pandas as pd
import streamlit as st
from collections import Counter

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.abspath(os.path.join(parent_dir, "statistics_dir")))

from statistics_dir.statistics import *
from config import FINAL_DATA_FILE, TAG, GENERAL_SONGS_THEMS
from conclusion_text import *
from gui_helper import *


def gui_template(df, title, options, word_insight, sentiment_insight, artist_insight, theme_insight):

    ( artist_stat,
      norm_words_stat,
      theme_stat,
      sentiment_single_dist,
      sentiment_avg_dist,
      avg_words_per_song ) = general_statistics(df)

    analysis_option = st.sidebar.selectbox("Select analysis", options)

    if analysis_option == "General":
        st.markdown(
            f"<h1 style='text-align: center;'>{title}</h1>",
            unsafe_allow_html=True,
        )
        wordcloud_func(norm_words_stat)
        single_sentiment_markdown = max_sentiment_to_text(sentiment_single_dist)
        avg_sentiment_markdown = avg_sentiment_to_text(sentiment_avg_dist)

        st.markdown(
            GENERAL_GENERAL_INSIGHT.format(
                len_songs=len(df),
                len_diff_artists=len(artist_stat),
                single_sentiment=single_sentiment_markdown,
                avg_sentiment=avg_sentiment_markdown,
                avg_song_len=avg_words_per_song,
            )
        )

    elif analysis_option == "Word":
        st.markdown(
            '<h4 style="font-size:15px;text-align: center;">Frequency & Percentage as function of the normalized words form</h4>',
            unsafe_allow_html=True,
        )
        plot_top_percentage(
            df=norm_words_stat,
            x_label="Words",
            title="Words Percentage",
            rotation=90,
            samples_num=20,
        )

        st.subheader("Conclusions")
        st.markdown(word_insight)

    elif analysis_option == "Sentiment":
        st.write(
            "This graph is the average song sentiment (Averaging all the sentiments of the songs):"
        )
        plot_top_percentage(
            df=sentiment_avg_dist,
            x_label="Sentiment",
            title="Average Sentiment Percentage",
            annot_bar=False,
            rotation=0,
        )

        st.write(
            "The maximum sentiment percentage is selected as the single song sentiment:"
        )
        plot_top_percentage(
            df=sentiment_single_dist,
            x_label="Sentiment",
            title="Single Sentiment Percentage",
            rotation=0,
        )

    elif analysis_option == "Artist":
        plot_top_percentage(
            df=artist_stat,
            x_label="Artist",
            title="Artist Percentage",
            rotation=90,
            samples_num=20,
        )
        st.subheader("Conclusions")
        st.markdown(artist_insight)

    elif analysis_option == "Theme":
        gt_names = set(df["general_theme"].tolist())
        gs_numbered = "\n".join([f"{i+1}. {item}" for i, item in enumerate(gt_names)])
        plot_top_percentage(df=theme_stat, x_label="Theme", title="Theme percentage", rotation=90)

        st.subheader("Conclusions")
        st.markdown(theme_insight)
        st.subheader("General songs theme list:")
        st.markdown(gs_numbered)


df = pd.read_csv(FINAL_DATA_FILE, encoding="utf-8")
df["norm_words"] = df["norm_words"].apply(lambda x: eval(x))


# Additional analyses
options = st.sidebar.radio( "Select Analysis", ["General", "Known Sentiment", "Known Artist"])


# Most Common Words
if options == "General":
    gen_title = f"{TAG.upper()} STATISTICS"
    gui_template(df, title=gen_title, options = ["General", "Word", "Sentiment", "Artist", "Theme"], word_insight = GENERAL_WORD_INSIGHT , sentiment_insight = GENERAL_SENTIMENT_INSIGHT, artist_insight = GENERAL_ARTIST_INSIGHT, theme_insight = GENERAL_THEME_INSIGHT)

if options == "Known Sentiment":
    sentiment_options = st.sidebar.radio( "Select ", ["Positive", "Negative", "Neutral"])
    sen_title = f"{sentiment_options.upper()} SENTIMENT STATISTICS"
    df_sentiment = df[df['selected_sentiment'] == sentiment_options.lower()]
    gui_template(df_sentiment, sen_title, options = ["General", "Word", "Artist", "Theme"], word_insight = GENERAL_WORD_INSIGHT , sentiment_insight = GENERAL_SENTIMENT_INSIGHT, artist_insight = GENERAL_ARTIST_INSIGHT, theme_insight = GENERAL_THEME_INSIGHT)

if options == "Known Artist":
    try:
        df.loc[:, "all_artists"] = df["all_artists"].apply(lambda x: eval(x))
    except TypeError as e:
        pass

    df_all_artist = df.explode("all_artists")
    artist_counts = Counter(df_all_artist['all_artists'].tolist())
    sorted_elements = sorted(artist_counts, key=artist_counts.get, reverse=True)

    artist_options = st.sidebar.selectbox( "Select ", sorted_elements)
    df_artist = df_all_artist[df_all_artist["all_artists"] == artist_options]
    artist_title = f"{artist_options.upper()} STATISTICS"
    gui_template(df_artist, artist_title, options = ["General", "Word", "Sentimemt", "Theme"], word_insight = GENERAL_WORD_INSIGHT , sentiment_insight = GENERAL_SENTIMENT_INSIGHT, artist_insight = GENERAL_ARTIST_INSIGHT, theme_insight = GENERAL_THEME_INSIGHT)
