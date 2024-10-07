# KNOWN_SENTIMENT_WORD_INSIGHT

KNOWN_SENTIMENT_WORD_INSIGHT_POSITIVE = """
        - When the sentiment is "Positive," compared to "Negative" or "Neutral," there is a high probability that the event being described occurred at night, as the word "noche" ("night") appears more frequently.
        - When the sentiment is "Positive," the use of words like "Mujer" ("Woman"), "Mami," and "Baby" suggests two things: (1) a significant presence of male artists in the dataset, and (2) that when the singer is in a positive mood, he is more likely to refer to his partner using affectionate terms or nicknames.
"""
KNOWN_SENTIMENT_WORD_INSIGHT_NEGATIVE = """
        - When the sentiment is "Negative" the word "Morir" ("Die") frequently appears, suggesting that when the singer suffers, it is in its most extreme form.
"""
# KNOWN_SENTIMENT_ARTIST_INSIGHT

KNOWN_SENTIMENT_ARTIST_INSIGHT_POSITIVE = """
        - An analysis of artists with a substantial discography (over 20 songs) reveals that:
            * Prince Royce stands out as one of the most positive, with approximately every other song carrying an upbeat or optimistic tone.
        - Interestingly, although Juan Luis Guerra does not have an extensive catalog of songs, each one carries a positive sentiment.
"""

KNOWN_SENTIMENT_ARTIST_INSIGHT_NEGATIVE = """
        - An analysis of artists with a substantial discography (over 20 songs) reveals that:
            * Frank Reyes as one of the most negative artists, with nearly 80% of his tracks expressing predominantly negative sentiment.
"""

# KNOWN_SENTIMENT_THEME_INSIGHT
KNOWN_SENTIMENT_THEME_INSIGHT_POSITIVE = """ 
        - When the sentiment is "Positive", the most likely theme is "Love and Relationships".
"""

KNOWN_SENTIMENT_THEME_INSIGHT_NEGATIVE = """ 
        - When the sentiment is "Negative", the most likely theme is "Hearthbreak and Loss".
"""

def find_known_sentiment_conc(sentiment):
    sentiment_c = sentiment.upper()
    conc_word_name = f"KNOWN_SENTIMENT_WORD_INSIGHT_{sentiment_c}"
    conc_artist_name = f"KNOWN_SENTIMENT_ARTIST_INSIGHT_{sentiment_c}"
    conc_theme_name = f"KNOWN_SENTIMENT_THEME_INSIGHT_{sentiment_c}"

    conc_word_text = ""
    if conc_word_name in globals():
        conc_word_text = globals()[conc_word_name]

    conc_artist_text = ""
    if conc_artist_name in globals():
        conc_artist_text = globals()[conc_artist_name]

    conc_theme_text = ""
    if conc_theme_name in globals():
        conc_theme_text = globals()[conc_theme_name]

    return conc_word_text, conc_artist_text, conc_theme_text
