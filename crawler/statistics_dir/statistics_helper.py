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

def dist_single_sentiment(df, col):
    sentiment_counts = df[col].value_counts()

    total_df = len(df)
    
    artist_percentages = (sentiment_counts / total_df) * 100

    # Create a DataFrame with the statistics
    stats_df = pd.DataFrame({
        'Frequency': sentiment_counts,
        'Percentage': artist_percentages
    }).reset_index()
    stats_df.columns = ['Sentiment', 'Frequency', 'Percentage']
    stats_df = stats_df.sort_values(by='Sentiment', ascending=False)

    return stats_df

def dist_avg_sentiment(df, col):
    sen_list = []
    for v in df[col].tolist():
        sen_list.append(eval(v))
    
    df_sentiment_raw = pd.DataFrame(sen_list)
    df_series_sentiment = df_sentiment_raw.mean()
    df_sentiment = df_series_sentiment.reset_index()
    df_sentiment.columns = ['Sentiment', 'Percentage']

    df_sentiment = df_sentiment.sort_values(by='Sentiment', ascending=False)

    return df_sentiment

def avg_word_per_song(df, col):
    df['unique_word_count'] = df[col].apply(len)
    average_unique_words = df['unique_word_count'].mean()
    return average_unique_words