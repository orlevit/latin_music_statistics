import numpy as np
import pandas as pd


def eval_col(df, col_name):
    try:
        df.loc[:, col_name] = df[col_name].apply(lambda x: eval(x))
    except (TypeError, NameError, SyntaxError) as e:
        pass

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

def calc_general_themes_counts(df_org, col):
    df = df_org.copy()
    miscellaneous_threshold = max(int(len(df) * 0.025), 2)

    all_counts = df[col].value_counts()
    
    miscellaneous_themes = [k for k, v in all_counts.items() if  v <= miscellaneous_threshold]
    df.loc[:, 'general_themes_w_miscellaneous'] = df[col]
    df.loc[df[col].isin(miscellaneous_themes), 'general_themes_w_miscellaneous'] = 'Miscellaneous'

    gt_stat, _ = calculate_counts_with_sentiment(df, "general_themes_w_miscellaneous", "selected_sentiment")
    
    if 'Miscellaneous' in gt_stat:
        gt_stat['Miscellaneous'] = gt_stat.pop('Miscellaneous')
    
    return gt_stat


# Added a custom function for a specific case. It still needs to be integrated more smoothly.
def known_sentiment_artists_calc_counts_with_sentiment(df, col, sentiment_col, sentiment_order):
    df_expanded = df.explode(col)

    # Calculate frequency and percentage for the main column
    all_counts = df_expanded[col].value_counts()

    stats_df = pd.DataFrame({
        col: all_counts.index,
        'Frequency': all_counts.values,
    })
    
    # Create nested dictionary to hold sentiments within each category
    nested_dict = {}
    for col_value in stats_df[col]:
        singer_frequency = int(all_counts[col_value])        
        selected_df = df_expanded[df_expanded[col] == col_value]
        sentiment_counts = selected_df[sentiment_col].value_counts()

        # Ensure the sentiment order is always "Negative", "Positive", "Neutral"
        ordered_sentiments =  list(sentiment_counts.keys())
        ordered_counts = {sentiment: sentiment_counts.get(sentiment, 0) for sentiment in ordered_sentiments}
        sent_counts = sentiment_counts.get(sentiment_order[0], 0)

        if sent_counts != 0:
            nested_dict[col_value] = {
                'Frequency': sent_counts,
                'Percentage': round(sent_counts/singer_frequency, 2),
                'Sentiments': ordered_counts
            }
    artist_stat_len = len(nested_dict)
    top_sorted_data = dict(sorted(nested_dict.items(), key=lambda item: item[1]['Frequency'], reverse=True)[:10])
    sorted_data = dict(sorted(top_sorted_data.items(), key=lambda item: item[1]['Sentiments'].get(sentiment_order[0], 0), reverse=True))

    return sorted_data, artist_stat_len
    

def calculate_counts_with_sentiment(df, col, sentiment_col, sentiment_order=None):
    df_expanded = df.explode(col)

    # Calculate frequency and percentage for the main column
    all_counts = df_expanded[col].value_counts()
    total_records = len(df)
    percentages = (all_counts / total_records) * 100

    stats_df = pd.DataFrame({
        col: all_counts.index,
        'Frequency': all_counts.values,
        'Percentage': percentages.values
    })

    # Create nested dictionary to hold sentiments within each category
    nested_dict = {}
    for col_value in stats_df[col]:
        selected_df = df_expanded[df_expanded[col] == col_value]
        sentiment_counts = selected_df[sentiment_col].value_counts()

        # Ensure the sentiment order is always "Negative", "Positive", "Neutral"
        ordered_sentiments =  list(sentiment_counts.keys())
        ordered_counts = {sentiment: sentiment_counts.get(sentiment, 0) for sentiment in ordered_sentiments}

        nested_dict[col_value] = {
            'Frequency': int(all_counts[col_value]),
            'Percentage': round(percentages[col_value], 2),
            'Sentiments': ordered_counts
        }

    sorted_data = dict(sorted(nested_dict.items(), key=lambda item: item[1]['Frequency'], reverse=True))
    artist_stat_len = len(sorted_data)
    # sorted_data = order_nested_dict(nested_dict, sentiment_order)

    return sorted_data, artist_stat_len

def most_common_word(df, text_column, top=10):

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
    df_series_sentiment = df_sentiment_raw.mean() * 100 
    df_sentiment = df_series_sentiment.reset_index()
    df_sentiment.columns = ['Sentiment', 'Percentage']

    df_sentiment = df_sentiment.sort_values(by='Sentiment', ascending=False)

    return df_sentiment

def avg_word_per_song(df, col):
    df['unique_word_count'] = df[col].apply(len)
    average_unique_words = df['unique_word_count'].mean()
    return average_unique_words

def gender_stat(df):
    df_len = len(df)
    men_p = np.round((len(df[df['gender'] == 'Male']) / df_len) * 100, 2)
    women_p = np.round((len(df[df['gender'] == 'Female']) / df_len) * 100, 2)
    both_p = np.round((len(df[df['gender'] == 'Both']) / df_len) * 100, 2)

    return women_p, men_p, both_p
