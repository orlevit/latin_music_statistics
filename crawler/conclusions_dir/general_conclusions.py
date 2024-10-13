GENERAL_GENERAL_INSIGHT = """
- General statistics:
    1. There are {len_songs} songs in the corpus.
    2. There corpus has {len_diff_artists} different artists.
    3. {avg_sentiment}    
    4. {single_sentiment}
    5. The average unique words per song is: {avg_song_len}.
    6. The prominent singer percentage: Women - {women_percentage}%, Men - {men_percentage}%, Both - {both_percentage}%.
    """

GENERAL_WORD_INSIGHT ="""
        - The words "querer" ("want") and "amor" ("love") occur at significantly higher rates compared to other terms, it might indicating that a majority of the songs focus on desire and love, likely emphasizing the longing for love.
        - Although the precise meaning of the text may not be immediately clear from the words themselves, the predominantly negative sentiment, combined with terms that imply change, such as "dejar" ("leave"), "volver" ("return"), and "olvidar" ("forget") - points to an underlying theme of loss, most likely the loss of love.
        - To fully comprehend the song, in addition to understanding its grammar, one needs to have a familiarity with an average of 55 words.

        Since the following conclusions rely on sentiment allocations and are easier to deduce when sentiment is displayed within the bars. The pre-generated plot is included below, as generating it in real time would extend the processing time by a factor of 11.5.
        - When the artists think ("pensar"), the word usually (~67%) exists in songs with a negative sentiment, it may be more beneficial for them to refrain from such contemplation.
        - The word "vida" ("life") is usually (~63%) used in songs with a negative sentiment. This may suggests that bachata singers often express negative emotional themes in their lives.
        """

GENERAL_ARTIST_INSIGHT = """
        - Out of the graph above, only artists with more than 20 songs are considered sufficient and included in the analysis:
            * The five most frequent artists appear in 36% of the songs, with a significant drop in the presence of other artists beyond this point. This indicates that the vocabulary, sentiment, and themes conveyed by these prominent artists have a major impact on the overall statistics.
            * Frank Reyes and Ralphy Dreamz tend to produce a significantly higher volume of negative-themed songs compared to their peers.
            * Prince Royce is recognized as one of the most optimistic and positive artists in the Bachata music industry (For better view of this colclusion, slice by known positive sentiment).
        """

GENERAL_SENTIMENT_INSIGHT = """
        - It is most likely that a song will convey a negative sentiment.
        - The negative and positive songs exhibit a comparable level of neutral sentiment in their lyrics (~14%).
        - Interestingly, some songs demonstrate a neutral sentiment. Upon analysis, it seems these songs can be interpreted as either positive or negative depending on the listener’s perspective. As a result, the model refrained from assigning a definitive sentiment and instead classified them with a high neutral value.
        - The majority of "Neutral" songs are attributed to less frequent or lesser-known artists, suggesting that more prominent or well-known singers tend to convey clearer, more distinct sentiments, whether "Negative" or "Positive".
"""

GENERAL_THEME_INSIGHT = """
        - The predominant themes "Love and Relationships", "Heartbreak and Loss" and "Toxic Relationships" are representative of approximately 71% of the corpus. Notably, many of these songs delve into the complexities of deep emotional connections, often focusing on ongoing or concluded relationships rather than those in their initial stages. When exploring the theme of "Critique of Love," it becomes evident that this encompasses a broader critique of love itself, as well as specific commentary on contemporary relationships.
        - The theme of "Toxic Relationships" inherently conveys a negative connotation and cannot be interpreted in any other light. 
        """
