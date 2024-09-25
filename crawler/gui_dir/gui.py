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
sys.path.append(os.path.abspath(os.path.join(parent_dir, "theme_dir")))
sys.path.append(os.path.abspath(os.path.join(parent_dir, "conclusions_dir")))

from statistics_dir.statistics import *
from statistics_dir.statistics_helper import calculate_counts
from config import (
    FINAL_DATA_FILE,
    TAG,
    GENERAL_SONGS_THEMS,
    DATA_THEME_SINGERS_DIR,
    SENTIMENT_COLORS,
)
from general_conclusions import  GENERAL_WORD_INSIGHT, GENERAL_ARTIST_INSIGHT, GENERAL_SENTIMENT_INSIGHT, GENERAL_THEME_INSIGHT 

from known_sentiment_conclusions import KNOWN_SENTIMENT_GENERAL_INSIGHT
from known_artist_conclusions import KNOWN_ARTIST_GENERAL_INSIGHT

from conclusion_text import *
from gui_helper import *
from clustering_general_theme import load_artist_theme_df


df = pd.read_csv(FINAL_DATA_FILE, encoding="utf-8")
df["norm_words"] = df["norm_words"].apply(lambda x: eval(x))


# Additional analyses
options = st.sidebar.radio(
    "Select Analysis", ["General", "Known Sentiment", "Known Artist"]
)


# Most Common Words
if options == "General":
    gen_title = f"{TAG.upper()} STATISTICS"
    gui_template(
        df,
        title=gen_title,
        options=["General", "Word", "Sentiment", "Artist", "Theme", "Data"],
        specific_artist_name="",
        word_insight=GENERAL_WORD_INSIGHT,
        sentiment_insight=GENERAL_SENTIMENT_INSIGHT,
        artist_insight=GENERAL_ARTIST_INSIGHT,
        theme_insight=GENERAL_THEME_INSIGHT,
    )

if options == "Known Sentiment":
    sentiment_options = st.sidebar.radio("Select ", ["Positive", "Negative", "Neutral"])
    sen_title = f"{sentiment_options.upper()} SENTIMENT STATISTICS"
    df_sentiment = df[df["selected_sentiment"] == sentiment_options.lower()]
    gui_template(
        df_sentiment,
        sen_title,
        options=["General", "Word", "Artist", "Theme", "Data"],
        specific_artist_name="",
        word_insight=GENERAL_WORD_INSIGHT,
        sentiment_insight=GENERAL_SENTIMENT_INSIGHT,
        artist_insight=GENERAL_ARTIST_INSIGHT,
        theme_insight=GENERAL_THEME_INSIGHT,
        out_of_total_percentage=False,
        present_sentiments=[sentiment_options.lower()],
        df_total=df
    )

if options == "Known Artist":
    try:
        df.loc[:, "all_artists"] = df["all_artists"].apply(lambda x: eval(x))
    except TypeError as e:
        pass

    df_all_artist = df.explode("all_artists")
    artist_counts = Counter(df_all_artist["all_artists"].tolist())
    sorted_elements = sorted(artist_counts, key=artist_counts.get, reverse=True)

    artist_options = st.sidebar.selectbox("Select ", sorted_elements)

    df_artist = df_all_artist[df_all_artist["all_artists"] == artist_options]


    artist_specific_title = f"{artist_options.upper()} SPECIFIC THEME STATISTICS"
    artist_title = f"{artist_options.upper()} GENERAL THEME STATISTICS"
    gui_template(
        df_artist,
        artist_title,
        options=["General", "Word", "Sentiment", "Theme", "Data"],
        specific_artist_name=artist_options,
        word_insight=GENERAL_WORD_INSIGHT,
        sentiment_insight=GENERAL_SENTIMENT_INSIGHT,
        artist_insight=GENERAL_ARTIST_INSIGHT,
        theme_insight=GENERAL_THEME_INSIGHT,
    )
