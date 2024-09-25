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
    
