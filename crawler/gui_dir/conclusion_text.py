GENERAL_GENERAL = """
- General statistics:
    1. There are {len_songs} songs in the corpus.
    2. There corpus has {len_diff_artists} different artists.
    3. {sentiment}
    4. The average words per song is: {avg_song_len}.
    """

GENERAL_WORD ="""
        - The percentage of occurrences for the words 'Querer' and 'Amor' is significantly higher than for other words, suggesting that the predominant theme among the singers is a desire for love.
        - While the precise meaning of the text may not be immediately apparent from the words alone, the context and sentiment conveyed through key terms like "dejar" (leave), "volver" (return), "pensar" (think), "morir" (die), and "olvidar" (forget) suggest an underlying theme of loss—most likely the loss of love. 
        """

GENERAL_ARTIST = """
        - The five most frequent artists appear in 36% of the songs, with a significant drop in the presence of other artists beyond this point. This indicates that the vocabulary, sentiment, and themes conveyed by these prominent artists have a major impact on the overall statistics.
        """


# Per artist
ARTIST_GENERAL = """
- Artist statistics:
    1. There are {len_songs} songs for this artist.
    2. {sentiment}    
    3. The average words per song is: {avg_song_len}.
    """


def sentiment_to_text(df):
    markdown = "Sentiment Distribution\n"
    for index, row in df.iterrows():
        markdown += f" \t \t - {row['Sentiment']} (Frequency: {row['Frequency']} | Percentage: {row['Percentage']:.2f}%)\n"
        
    return markdown
    