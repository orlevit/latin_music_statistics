import re
import os
import sys
import warnings
import pandas as pd
from statistics_helper import *

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)


def general_statistics(df):
    try:
        df.loc[:, "all_artists"] = df["all_artists"].apply(lambda x: eval(x))
    except TypeError as e:
        pass

    artist_stat = calculate_counts(df, "all_artists")
    norm_words_stat = calculate_counts(df, "norm_words")
    gt_stat = calculate_counts(df, "general_theme")


    sentiment_single_dist = dist_single_sentiment(df, "selected_sentiment")
    sentiment_avg_dist = dist_avg_sentiment(df, "sentiment")
    avg_words_per_song = int(df["norm_w_len"].mean())

    return (
        artist_stat,
        norm_words_stat,
        gt_stat,
        sentiment_single_dist,
        sentiment_avg_dist,
        avg_words_per_song,
    )


def artist_statistics(df, artist_name):
    df_expanded = df.explode("all_artists")
    df_artist = df_expanded[df_expanded["all_artists"] == artist_name]

    # df['norm_words'] = df_artist['norm_words'].apply(lambda x: eval(x))
    norm_words_stat = calculate_counts(df_artist, "norm_words")

    num_songs_per_artist = len(df_artist)
    sentiment_single_dist = dist_single_sentiment(df_artist, "selected_sentiment")
    sentiment_avg_dist = dist_avg_sentiment(df_artist, "sentiment")
    avg_words_per_song = int(df_artist["norm_w_len"].mean())

    return (
        norm_words_stat,
        num_songs_per_artist,
        sentiment_single_dist,
        sentiment_avg_dist,
        avg_words_per_song,
    )
