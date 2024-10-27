def max_sentiment_to_text(df):
    markdown = "Single sentiment distribution (The highest sentiment percentage is selected as the sentiment for a single song):\n"
    for index, row in df.iterrows():
        markdown += f" \t \t - {row['Sentiment']} - Frequency: {row['Frequency']} | Percentage: {row['Percentage']:.2f}%.\n"
        
    return markdown

def avg_sentiment_to_text(df):
    markdown = "Average sentiment distribution (Averaging the sentiments of all the songs):\n"
    
    for index, row in df.iterrows():
         markdown += f" \t \t - {row['Sentiment']} - Percentage: {row['Percentage']:.2f}%.\n"
        
    return markdown
    
