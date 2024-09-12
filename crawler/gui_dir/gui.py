import re
import os
import sys
import pandas as pd
import streamlit as st
from openai import OpenAI
from collections import Counter

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.abspath(os.path.join(parent_dir, "statistics_dir")))
sys.path.append(os.path.abspath(os.path.join(parent_dir, "theme_and_sentiment")))

from statistics_dir.statistics import *
from statistics_dir.statistics_helper import calculate_counts
from config import FINAL_DATA_FILE, TAG, GENERAL_SONGS_THEMS, DATA_THEME_SINGERS_DIR
from conclusion_text import *
from gui_helper import *
from clustering_general_theme import load_artist_theme_df



df = pd.read_csv(FINAL_DATA_FILE, encoding="utf-8")
df["norm_words"] = df["norm_words"].apply(lambda x: eval(x))


# Additional analyses
options = st.sidebar.radio( "Select Analysis", ["General", "Known Sentiment", "Known Artist"])


# Most Common Words
if options == "General":
    gen_title = f"{TAG.upper()} STATISTICS"
    gui_template(df, title=gen_title, options = ["General", "Word", "Sentiment", "Artist", "Theme", "Data"], word_insight = GENERAL_WORD_INSIGHT , sentiment_insight = GENERAL_SENTIMENT_INSIGHT, artist_insight = GENERAL_ARTIST_INSIGHT, theme_insight = GENERAL_THEME_INSIGHT)

if options == "Known Sentiment":
    sentiment_options = st.sidebar.radio( "Select ", ["Positive", "Negative", "Neutral"])
    sen_title = f"{sentiment_options.upper()} SENTIMENT STATISTICS"
    df_sentiment = df[df['selected_sentiment'] == sentiment_options.lower()]
    gui_template(df_sentiment, sen_title, options = ["General", "Word", "Artist", "Theme", "Data"], word_insight = GENERAL_WORD_INSIGHT , sentiment_insight = GENERAL_SENTIMENT_INSIGHT, artist_insight = GENERAL_ARTIST_INSIGHT, theme_insight = GENERAL_THEME_INSIGHT)

if options == "Known Artist":
    try:
        df.loc[:, "all_artists"] = df["all_artists"].apply(lambda x: eval(x))
    except TypeError as e:
        pass

    df_all_artist = df.explode("all_artists")
    artist_counts = Counter(df_all_artist['all_artists'].tolist())
    sorted_elements = sorted(artist_counts, key=artist_counts.get, reverse=True)

    artist_options = st.sidebar.selectbox( "Select ", sorted_elements)

    # Artist - general theme
    df_artist = df_all_artist[df_all_artist["all_artists"] == artist_options]
    artist_title = f"{artist_options.upper()} GENERAL THEME STATISTICS"
    gui_template(df_artist, artist_title, options = ["General", "Word", "Sentiment", "Theme", "Data"], word_insight = GENERAL_WORD_INSIGHT , sentiment_insight = GENERAL_SENTIMENT_INSIGHT, artist_insight = GENERAL_ARTIST_INSIGHT, theme_insight = GENERAL_THEME_INSIGHT)

##    # Artist - specific theme
#    OPENAI_KEY = "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"
#    client = OpenAI(api_key = OPENAI_KEY)
#                   
#    unique_artist_gt_len = len(df_artist["general_theme"].unique())
#    df_specific_artist = load_artist_theme_df(df_artist, singer_name = artist_options, client=client, cluster_num = int(1.5 * unique_artist_gt_len))
#
#    artist_specific_title = f"{artist_options.upper()} SPECIFIC THEME STATISTICS"
#    ARTIST_GENERAL_THEME_DIR = os.path.join(DATA_THEME_SINGERS_DIR, artist_options)
#    ARTIST_GENERAL_THEME_FILE = os.path.join(ARTIST_GENERAL_THEME_DIR, f'{artist_options}_general_themes.csv')
#    artist_general_theme_df = pd.read_csv(ARTIST_GENERAL_THEME_FILE)
#    gt_names = set(artist_general_theme_df["general_theme"].tolist())
#    gs_numbered = "\n".join([f"{i+1}. {item}" for i, item in enumerate(gt_names)])
#    artist_theme_stat = calculate_counts(df_specific_artist, "general_theme")
#
#    st.subheader("-" * 100)
#
#    plot_top_percentage(df=artist_theme_stat, x_label="Theme", title="Theme percentage", rotation=90, samples_num = len(artist_theme_stat))
#    st.subheader("Specific artist general songs theme list:")
#    st.markdown(gs_numbered)
#
#
#    st.subheader("Conclusions")
#    st.markdown(GENERAL_THEME_INSIGHT)
