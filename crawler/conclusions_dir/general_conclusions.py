GENERAL_GENERAL_INSIGHT = """
- General statistics:
    1. There are {len_songs} songs in the corpus.
    2. There corpus has {len_diff_artists} different artists.
    3. {single_sentiment}
    4. {avg_sentiment}    
    5. The average unique words per song is: {avg_song_len}.
    6. The prominent singer percentage: Women ({women_percentage}%), Men ({men_percentage}%), Both ({both_percentage}%).
    """

GENERAL_WORD_INSIGHT ="""
        - The words "Querer" and "Amor" occur at significantly higher rates compared to other terms, indicating that a majority of the songs focus on desire and love, likely emphasizing the longing for love.
        - While the precise meaning of the text may not be immediately apparent from the words alone, the context and sentiment conveyed through key terms like "dejar" (leave), "volver" (return), "morir" (die), and "olvidar" (forget) suggest an underlying theme of loss—most likely the loss of love. 
        - To fully comprehend the song, in addition to understanding its grammar, you need to have a familiarity with an average of 55 words.
        - When the artists think ("pensar"), the word usually (~80%) exists in songs with a negative sentiment, it may be more beneficial for them to refrain from such contemplation.
        """

GENERAL_ARTIST_INSIGHT = """
        - The five most frequent artists appear in 36% of the songs, with a significant drop in the presence of other artists beyond this point. This indicates that the vocabulary, sentiment, and themes conveyed by these prominent artists have a major impact on the overall statistics.
        - "Frank Reyes" and "Ralphy Dreamz" tend to produce a significantly higher volume of negative-themed songs compared to their peers.
        - "Prince Royce" is recognized as one of the most optimistic and positive artists in the music industry.
        * Only songs featuring more than 20 samples are considered.
        """

GENERAL_SENTIMENT_INSIGHT = """
        - It is most likely that a song will convey a negative sentiment.
        - The negative and positive songs exhibit a comparable level of neutral sentiment in their lyrics (~14%).
        - Interestingly, some songs demonstrate a neutral sentiment. Upon analysis, it seems these songs can be interpreted as either positive or negative depending on the listener’s perspective. As a result, the model refrained from assigning a definitive sentiment and instead classified them with a high neutral value.
        - The majority of "Neutral" songs are attributed to less frequent or lesser-known artists, suggesting that more prominent or well-known singers tend to convey clearer, more distinct sentiments, whether "Negative" or "Positive"
"""
 

GENERAL_THEME_INSIGHT = """ 
        - Every second songs is  focus on theme of "Hearthbreak and Loss", or "Love and Relationship.
        - The theme of "Toxic Relationships" inherently conveys a negative connotation and cannot be interpreted in any other light. 
        - The term "vida" has approximately a 65% probability of being used in songs with negative sentiment. This suggests that batchata singers have negative emotional themes in their lives.
        - The predominant themes identified are "Toxic Relationships," "Love and Relationships," and "Heartbreak and Loss." Notably, many of the songs delve into the complexities of deep emotional connections, often focusing on ongoing or concluded relationships rather than those in their initial stages. When exploring the theme of "Critique of Love," it becomes evident that this encompasses a broader critique of love itself, as well as specific commentary on contemporary relationships.
        """

