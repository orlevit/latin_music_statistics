import re
import pandas as pd
from lyricsgenius import Genius
from config import GENIUS_API_TOKEN, DATA_FILE, TAG, SONGS_LIMIT

genius = Genius(GENIUS_API_TOKEN, timeout=15, retries=3)


def songs_w_tags(tag):
    page = 1
    results = []
    total_songs = 0
    while total_songs != SONGS_LIMIT:
        res = genius.tag(tag, page=page)
        songs_hits = len(res['hits'])
        if songs_hits == 0:
            break
        results.append(res)
        page = res['next_page'] if res['next_page'] is not None else page + 1
        total_songs += songs_hits

    return results


def get_urls(tag_results):
    songs_url = []
    songs_meta = []
    for page_num in range(len(tag_results)):
        for song_num in range(len(tag_results[page_num]['hits'])):
            song_meta = tag_results[page_num]['hits'][song_num]
            songs_meta.append(song_meta)
            songs_url.append(song_meta['url'])

    return songs_meta, songs_url


def find_lyrics(songs_meta, songs_url):
    lyrics = []
    for song_i, url in enumerate(songs_url):
        song_lyrics = genius.lyrics(song_url=url)
        songs_meta[song_i]['lyrics'] = song_lyrics
        lyrics.append(song_lyrics)
    return songs_meta, lyrics



tagged_pages = songs_w_tags(TAG)
songs_meta, songs_url = get_urls(tagged_pages)
songs_meta, lyrics = find_lyrics(songs_meta, songs_url)
df = pd.DataFrame(songs_meta)
df.to_csv(DATA_FILE,encoding = 'utf-8')
