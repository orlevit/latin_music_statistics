import pandas as pd


def calculate_counts(df, col):
    df_expanded = df.explode(col)

    all_counts = df_expanded[col].value_counts()

    total_records = len(df_expanded)
    percentages = (all_counts / total_records) * 100

    # Create a DataFrame with the statistics
    stats_df = pd.DataFrame({
        'Frequency': all_counts,
        'Percentage': percentages
    }).reset_index()
    stats_df.columns = [col, 'Frequency', 'Percentage']
    return stats_df

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
    sentiment_counts = df[col].value_counts()

    total_df = len(df)
    
    artist_percentages = (sentiment_counts / total_df) * 100

    # Create a DataFrame with the statistics
    stats_df = pd.DataFrame({
        'Frequency': sentiment_counts,
        'Percentage': artist_percentages
    }).reset_index()
    stats_df.columns = ['Sentiment', 'Frequency', 'Percentage']
    return stats_df

def avg_word_per_song(df, col):
    df['unique_word_count'] = df[col].apply(len)
    average_unique_words = df['unique_word_count'].mean()
    return average_unique_words