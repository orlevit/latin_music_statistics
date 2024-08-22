import re
import os
import sys
import warnings
import pandas as pd

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

from config import PROCESSED_DATA_FILE

df = pd.read_csv(PROCESSED_DATA_FILE, encoding='utf-8')
df['all_artists'] = df['all_artists'].apply(lambda x: eval(x))

artist_stat = calculate_artist_counts(df, 'all_artists')
diff_artists_num = len(artist_stat)
sentiment_dist = dist_sentiment(df, 'selected_sentiment')
avg_words_per_song = int(df['norm_w_len'].mean())