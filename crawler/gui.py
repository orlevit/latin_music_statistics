import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# data = pd.DataFrame(clean_selected_lyrics, columns=['lyrics'])#load_data()

nltk.download('vader_lexicon')
# Streamlit app
st.title("Bachata Lyrics Language Detection")

# Additional analyses
options = st.sidebar.radio("Select Analysis",
                           ["Most Common Words", "Sentiment Analysis", "Word Cloud", "Song Length", "Unique Words",
                            "Top Artists", "Themes"])

# Most Common Words
if options == "Most Common Words":
    st.title("Most Common Words in Bachata Lyrics")
    all_words = ' '.join(data['lyrics']).split()
    common_words = Counter(all_words).most_common(20)
    common_words_df = pd.DataFrame(common_words, columns=['Word', 'Frequency'])
    st.bar_chart(common_words_df.set_index('Word'))

# Sentiment Analysis
elif options == "Sentiment Analysis":
    st.title("Sentiment Analysis of Bachata Lyrics")
    sia = SentimentIntensityAnalyzer()
    data['sentiment'] = data['lyrics'].apply(lambda x: sia.polarity_scores(x)['compound'])

    # Plotting the histogram using Matplotlib
    plt.figure(figsize=(10, 5))
    plt.hist(data['sentiment'], bins=20, edgecolor='k')
    plt.title('Sentiment Analysis of Bachata Lyrics')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    st.pyplot(plt)

# Word Cloud
elif options == "Word Cloud":
    st.title("Word Cloud of Bachata Lyrics")
    all_words = ' '.join(data['lyrics'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# Song Length
elif options == "Song Length":
    st.title("Average Song Length in Bachata Lyrics")
    data['word_count'] = data['lyrics'].apply(lambda x: len(x.split()))
    st.write(f"Average song length: {data['word_count'].mean():.2f} words")

# Unique Words
elif options == "Unique Words":
    st.title("Unique Words in Bachata Lyrics")
    all_words = ' '.join(data['lyrics']).split()
    unique_words = set(all_words)
    st.write(f"Total unique words: {len(unique_words)}")

# Top Artists
elif options == "Top Artists":
    st.title("Top Artists in Bachata Lyrics Collection")
    top_artists = data['artist'].value_counts().head(10)
    st.bar_chart(top_artists)

# Themes
elif options == "Themes":
    st.title("Common Themes in Bachata Lyrics")
    # This is a placeholder for more advanced NLP analysis
    st.write("This section requires advanced NLP techniques to identify themes.")
