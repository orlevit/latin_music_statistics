import re
import os
import sys
import warnings
import pandas as pd
from lyricsgenius import Genius

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

from config import DATA_FILE, CHORUS_SAMPLE_NUMBER, SPANISH_THRESHOLD, NOT_BACHATA, PROCESSED_DATA_FILE, ADDITIONAL_WORDS_REMOVAL
from helper import *

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


GENIUS_API_TOKEN = 'Od2yrHNfOCRHimIH3ev-wGZxZNJz3-47I4QfpzihKstD4eQaCItV28UJ72MAiV2W' # DELETE!!!!!!!!!!!!!!!!!!!!!!!!!
genius = Genius(GENIUS_API_TOKEN, timeout=15, retries=3)

df = pd.read_csv(DATA_FILE, encoding='utf-8')

clean_lyrics, chorus_list, song_wo_chorus_list, all_chorus_list, chorus_counter_list = extract_lyrics(df)

# Checked 50 songs: chorus same(38)/little different(5)/very different(7)
# print_sample_chorus(CHORUS_SAMPLE_NUMBER, clean_lyrics, chorus_counter_list,  all_chorus_list):

df_spanish = clean_spanish_songs(df, clean_lyrics)
print(f'After filtering non Bachata songs: {len(df_spanish)} songs')
normalized_words(df_spanish, 'clean_lyrics', 'norm_words')
df_spanish['norm_words'] = df_spanish['norm_words'].apply(remove_words)
df_spanish['norm_w_len'] = df_spanish['norm_words'].apply(lambda x: len(x))
calc_sentiment(df_spanish)
find_song_topic(df_spanish, 'clean_lyrics')
df_spanish['all_artists'] = df_spanish.apply(lambda row: eval(row['artists']) + eval(row['featured_artists']), axis=1)
df_spanish.to_csv(PROCESSED_DATA_FILE) 