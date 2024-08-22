# def most_common_word(df, text_column):
#     nlp = spacy.load('es_core_news_sm')

#     # Remove stop words, lemmatize
#     def preprocess_text(text):
#         doc = nlp(text.lower())  # Convert to lowercase and process with Spacy

#         # Remove stop words and punctuation, and perform lemmatization
#         tokens = [token.lemma_ for token in doc if token.text not in spanish_stop_words and not token.is_punct and not token.is_space]
#         return tokens

#     # Function to get the 10 most common words and their percentage
#     def get_top_10_words_percentage(df, text_column):
#         all_words = []

#         # Preprocess the text and collect all words
#         df[text_column].apply(lambda x: all_words.extend(preprocess_text(x)))

#         # Count word frequencies
#         word_counts = Counter(all_words)
#         total_words = sum(word_counts.values())

#         # Get the 10 most common words
#         most_common_words = word_counts.most_common(10)

#         # Calculate percentage for each word
#         word_percentages = [(word, count, round(count / total_words * 100, 2)) for word, count in most_common_words]

#         return word_percentages
#         #pd.DataFrame(word_percentages, columns=['Word_common', 'Count', 'Percentage'])

#     # Use the function on the 'clean_lyrics' column
#     top_10_words_df = get_top_10_words_percentage(df, text_column)

#     # Display the top 10 words with their counts and percentages
#     print(top_10_words_df)

def calculate_artist_counts(df):
    df_expanded = df.explode('Combined')

    # Step 2: Count the frequency of each artist
    artist_counts = df_expanded['Combined'].value_counts()

    # Step 3: Calculate the percentage of each artist's appearances
    total_artists = len(df_expanded)
    artist_percentages = (artist_counts / total_artists) * 100

    # Create a DataFrame with the statistics
    stats_df = pd.DataFrame({
        'Frequency': artist_counts,
        'Percentage': artist_percentages
    }).reset_index()
    stats_df.columns = ['Artist', 'Frequency', 'Percentage']
    return artist_counts

def most_common_word(df, text_column, top=10):

    # all_words = df[text_column].apply(lambda x: eval(x)).explode().tolist()
    all_words = df[text_column].explode().tolist()

    word_counts = Counter(all_words)
    total_words = sum(word_counts.values())

    most_common_words = word_counts.most_common(top)

    # Calculate percentage for each word
    word_percentages = [(word, count, round(count / total_words * 100, 2)) for word, count in most_common_words]

    return stats_df

# def num_of_diff_artists(df, col):
#     unique_artists_count = df[col].explode().nunique()
#     return unique_artists_count

def dist_sentiment(df, col):
    sentiment_distribution = df[col].value_counts()
    return sentiment_distribution

def avg_word_per_song(df, col):
    df['unique_word_count'] = df[col].apply(len)
    average_unique_words = df['unique_word_count'].mean()
    return average_unique_words