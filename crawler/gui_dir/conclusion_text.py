GENERAL_GENERAL_INSIGHT = """
- General statistics:
    1. There are {len_songs} songs in the corpus.
    2. There corpus has {len_diff_artists} different artists.
    3. {single_sentiment}
    4. {avg_sentiment}    
    5. The average unique words per song is: {avg_song_len}.
    """

GENERAL_WORD_INSIGHT ="""
        - The words "Querer" and "Amor" occur at significantly higher rates compared to other terms, indicating that a majority of the songs focus on desire and love, likely emphasizing the longing for love.
        - While the precise meaning of the text may not be immediately apparent from the words alone, the context and sentiment conveyed through key terms like "dejar" (leave), "volver" (return), "morir" (die), and "olvidar" (forget) suggest an underlying theme of loss—most likely the loss of love. 
        """

GENERAL_ARTIST_INSIGHT = """
        - The five most frequent artists appear in 36% of the songs, with a significant drop in the presence of other artists beyond this point. This indicates that the vocabulary, sentiment, and themes conveyed by these prominent artists have a major impact on the overall statistics.
        - The majority of "Neutral" songs are attributed to less frequent or lesser-known artists, suggesting that more prominent or well-known singers tend to convey clearer, more distinct sentiments, whether "Negative" or "Positive."
        """

GENERAL_SENTIMENT_INSIGHT = """ SSS """

GENERAL_THEME_INSIGHT = """ SSS """

# Per artist
ARTIST_GENERAL_INSIGHT = """
- Artist statistics:
    1. There are {len_songs} songs for this artist.
    2. {single_sentiment}
    3. {avg_sentiment}    
    4. The average words per song is: {avg_song_len}.
    """


def max_sentiment_to_text(df):
    markdown = "Single sentiment Distribution (The maximum sentiment percentage is selected as the single song sentiment)\n"
    for index, row in df.iterrows():
        markdown += f" \t \t - {row['Sentiment']} (Frequency: {row['Frequency']} | Percentage: {row['Percentage']:.2f}%)\n"
        
    return markdown

def avg_sentiment_to_text(df):
    markdown = "Average sentiment Distribution (Averaging all the sentiments of the songs)\n"
    
    for index, row in df.iterrows():
         markdown += f" \t \t - {row['Sentiment']} (Percentage: {row['Percentage']:.2f}%)\n"
        
    return markdown
    
