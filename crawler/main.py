import re
import os
import pandas as pd
from lyricsgenius import Genius
from config import DATA_FILE, CHORUS_SAMPLE_NUMBER, SPANISH_THRESHOLD
from helper import header_and_footer_removal, separate_chorus_rest, spanish_detection, text_cleaning, print_sample_chorus

GENIUS_API_TOKEN = 'Od2yrHNfOCRHimIH3ev-wGZxZNJz3-47I4QfpzihKstD4eQaCItV28UJ72MAiV2W'

genius = Genius(GENIUS_API_TOKEN, timeout=15, retries=3)

df = pd.read_csv(DATA_FILE, encoding = 'utf-8')
all_lyrics = df['lyrics'].to_list()


clean_lyrics = []
chorus_list = []
song_wo_chorus_list = []
all_chorus_list = []
chorus_counter_list = []

for lyrics in all_lyrics:
    lyrics_body = header_and_footer_removal(lyrics)
    chorus, rest, all_chorus, chorus_counter = separate_chorus_rest(lyrics_body)

    clean_lyrics.append(lyrics_body)
    chorus_list.append(chorus)
    song_wo_chorus_list.append(rest)
    all_chorus_list.append(all_chorus)
    chorus_counter_list.append(chorus_counter)

# print original and split chorus to files
# put it in a helper file

# Checked until 50(not included
# how many chorus same(38)/little different(5)/very different(7)

# print_sample_chorus(CHORUS_SAMPLE_NUMBER, clean_lyrics, chorus_counter_list,  all_chorus_list):

# song 50 is Italian
selected_lyrics = spanish_detection(clean_lyrics, SPANISH_THRESHOLD)
clean_selected_lyrics = text_cleaning(selected_lyrics)
pass



# 1) BOW for each song
# 2) BOW: distinction between chorus words and none chorus words (give chorus words higher weigh)
# 3) only chorus words
# 4)how many times the choros was different? statistics?