import re
import os
import sys
import warnings
import pandas as pd
from lyricsgenius import Genius

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.abspath(os.path.join(parent_dir, 'sentiment_dir')))
sys.path.append(os.path.abspath(os.path.join(parent_dir, 'theme_dir')))

from config import DATA_FILE, CHORUS_SAMPLE_NUMBER, SPANISH_THRESHOLD, NOT_BACHATA, FINAL_DATA_FILE, ADDITIONAL_WORDS_REMOVAL
from helper import *
from songs_sentiment import openai_sentiment_finder
from clustering_general_theme import create_specific_singer_theme

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

GENIUS_API_TOKEN = os.getenv('GENIUS_API_TOKEN')
genius = Genius(GENIUS_API_TOKEN, timeout=15, retries=3)

model_name = OPENAI_MODEL
OPENAI_KEY = os.getenv('OPENAI_KEY')                                                                                                                                          
client = OpenAI(api_key = OPENAI_KEY) 

df = pd.read_csv(DATA_FILE, encoding='utf-8')

clean_lyrics, chorus_list, song_wo_chorus_list, all_chorus_list, chorus_counter_list = extract_lyrics(df)

# Checked 50 songs: chorus same(38)/little different(5)/very different(7)
# print_sample_chorus(CHORUS_SAMPLE_NUMBER, clean_lyrics, chorus_counter_list,  all_chorus_list):

df_spanish = clean_spanish_songs(df, clean_lyrics)
print(f'After filtering non Bachata songs: {len(df_spanish)} songs')
normalized_words(df_spanish, 'clean_lyrics', 'norm_words')
df_spanish['norm_words'] = df_spanish['norm_words'].apply(remove_words)
df_spanish['norm_w_len'] = df_spanish['norm_words'].apply(lambda x: len(x))
df_spanish['norm_unique_words'] = df_spanish['norm_words'].apply(lambda x: set(x))
df_spanish['norm_unique_w_len'] = df_spanish['norm_unique_words'].apply(lambda x: len(x))

calc_sentiment(df_spanish)

df_spanish['all_artists'] = df_spanish.apply(lambda row: eval(row['artists']) + eval(row['featured_artists']), axis=1)
openai_sentiment_finder(df_spanish, client, model_name)                                                                                  create_specific_singer_theme(df_spanish, client, DATA_THEME_DIR, GENERAL_SONGS_THEMS, GENERAL_SONGS_THEMS_LOG, FINAL_DATA_FILE, cluster_num=20)

df_spanish.to_csv(FINAL_DATA_FILE)