import re
import os
import sys
import warnings
import pandas as pd
from statistics_helper import *

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

from config import PROCESSED_DATA_FILE


def general_statistics(df):
    df = pd.read_csv(PROCESSED_DATA_FILE, encoding='utf-8')
    
    df['all_artists'] = df['all_artists'].apply(lambda x: eval(x))
    artist_stat = calculate_counts(df, 'all_artists')
    
    df['norm_words'] = df['norm_words'].apply(lambda x: eval(x))
    norm_words_stat = calculate_counts(df, 'norm_words')
    
    diff_artists_num = len(artist_stat)
    sentiment_dist = dist_sentiment(df, 'selected_sentiment')
    avg_words_per_song = int(df['norm_w_len'].mean())

    return artist_stat, norm_words_stat, diff_artists_num, sentiment_dist, avg_words_per_song