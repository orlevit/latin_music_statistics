import os
import re
from langdetect import DetectorFactory, detect_langs

from config import CHORUS_SAMPLE_DIR

''' Remove header and footer '''


def header_and_footer_removal(lyrics):
    # First row removal
    text = "\n".join(lyrics.split("\n")[1:])

    # Removal of the last row
    text = re.sub(r'\d*Embed$', '', text)
    return text


''' Separate the chorus from the rest of the song '''


def separate_chorus_rest(single_lyric):
    rest = ''
    chorus = ''
    all_chorus_list = []
    prev_loc = 0
    chorus_counter = 0
    has_chorus_ind = False
    for i in re.finditer(r"\[(Coro|Chorus|Estribillo|Refrán).*?\][\s\S]*?(\n\n|$|(?=\[))", single_lyric):
        # end_span = i.span()[1] - 1 if single_lyric[i.span()[1] - 1] == '[' else i.span()[1]
        end_span = i.span()[1]
        single_chorus = single_lyric[i.span()[0]: end_span]

        if not has_chorus_ind:
            has_chorus_ind = True
            chorus += single_chorus

        rest += single_lyric[prev_loc: i.span()[0]] + '\n'
        prev_loc = end_span
        chorus_counter += 1
        all_chorus_list.append(single_chorus)
    rest += single_lyric[prev_loc:]

    return chorus, rest, '\n'.join(all_chorus_list), chorus_counter


''' Inspect the result of the splitting '''


def print_sample_chorus(chorus_sample_number, clean_lyrics, chorus_counter_list, all_chorus_list):
    if not os.path.exists(CHORUS_SAMPLE_DIR):
        os.makedirs(CHORUS_SAMPLE_DIR)

    # for i in range(CHORUS_SAMPLE_NUMBER):
    for i in range(chorus_sample_number):
        with open(rf"{CHORUS_SAMPLE_DIR}/{i}_song.txt", "w", encoding="utf-8") as f:
            # Writing data to a file
            f.writelines(clean_lyrics[i])

        with open(rf"{CHORUS_SAMPLE_DIR}/{i}_song_chorus.txt", "w", encoding="utf-8") as f:
            # Writing data to a file
            f.write(str(chorus_counter_list[i]) + "\n")
            f.writelines(all_chorus_list[i])


''' Detect lyrics in Spanish'''

def spanish_detection(lyrics, threshold):

    DetectorFactory.seed = 0
    no_lyrics_list = []
    es_not_detected_list = []
    es_prob_less = []
    es_selected_songs = []

    for i in range(len(lyrics)):
        if len(lyrics[i]):
            q = detect_langs(lyrics[i])
            es_detected = [single_lang for single_lang in q if single_lang.lang == 'es']
            if len(es_detected):
                lang_prob = es_detected[0].prob
                if threshold < lang_prob:
                    es_selected_songs.append(lyrics[i])
                else:
                    es_prob_less.append(i)
            else:
                es_not_detected_list.append(i)
        else:
            no_lyrics_list.append(i)

    print(f'Songs without lyrics: {len(no_lyrics_list)}')
    print(f'Songs which Spanish was not detected: {len(es_not_detected_list)}')
    print(f'Songs which Spanish was detected and below the threshold={threshold}: {len(es_prob_less)}')
    print(f'Songs which Spanish was detected and above the threshold={threshold}: {len(es_selected_songs)}')
    print(f'Percentage of the data selected: {round(len(es_selected_songs)/len(lyrics), 2)}%')

    return es_selected_songs


def text_cleaning(lyrics):
    clean_lyrics = []

    for text in lyrics:
        text = re.sub(r'\[.*\]\n', '', text)
        text = re.sub(r'\(.*?\)[\s*]?|[\s*]?\(.*?\)', '', text)
        text = re.sub(r'\".*?\"[\s*]?|[\s*]?\".*?\"', '', text)
        text = re.sub(r'[!¡?¿,.,]', '', text)
        text = re.sub(r'See [\w\s]+ LiveGet tickets as low as \$\d+You might also like|You might also like', '', text)
        
        clean_lyrics.append(text)

    return clean_lyrics