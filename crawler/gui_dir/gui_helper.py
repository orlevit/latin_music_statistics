import os
import sys
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.abspath(os.path.join(parent_dir, "statistics_dir")))

from statistics_dir.statistics import *
from conclusion_text import *

def plot_top_percentage(df, x_label, title, sentiment_colors=None, annot_bar=True, rotation=0, samples_num=10):

    top_df = df.sort_values(by="Percentage", ascending=False).head(samples_num)

    if sentiment_colors is None:
        sentiment_colors = "skyblue"
    else:
        sentiment_colors = top_df['Sentiment'].map(sentiment_colors)
        

    # Create the bar plot
    bars = plt.bar(top_df.iloc[:, 0], top_df["Percentage"], color=sentiment_colors)

    # Add annotations to each bar
    if annot_bar:
        for ii, bar in enumerate(bars):
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval,
                top_df.iloc[ii]["Frequency"],
                ha="center",
                va="bottom",
            )

    plt.xlabel(x_label)
    plt.ylabel("Percentage")
    plt.title(title)

    if rotation != 0:
        plt.xticks(rotation=rotation)

    plt.tight_layout()
    st.pyplot(plt)
    plt.close()


def plot_top_samples_with_sentiments(nested_dict, x_label, title, sentiment_colors, annot_bar=True, rotation=0, samples_num=10):

    # Taking the top N samples
    top_n_samples = dict(list(nested_dict.items())[:samples_num]) # nested_dict should be sorted Reversed
    
    # Initialize plot
    fig, ax = plt.subplots()
    
    # Set colors for different sentiments

    sentiment_labels = ['negative', 'positive', 'neutral']
    # Plot each sentiment for the top categories
    for key_name_, stats in top_n_samples.items():
        base_value = 0  # Start from the bottom for each bar

        # Get the sentiment data from the current theme
        sentiments = stats['Sentiments']

        for sentiment in ['negative', 'positive', 'neutral']:
            count = sentiments.get(sentiment, 0)  # Default to 0 if sentiment not found
            sentiment_percentage = (count / stats['Frequency'])* stats['Percentage']


            # Plot each sentiment as a stacked bar
            if count > 0:  # Only plot non-zero counts
                bar = ax.bar(
                    key_name_, sentiment_percentage,
                    bottom=base_value,
                    color=sentiment_colors.get(sentiment, 'blue'),
                )

                # Annotate each sentiment's count in the middle of its segment
                if annot_bar:
                    ax.text(
                        key_name_, base_value + sentiment_percentage / 2,
                        f"{count}",  # Annotate with the count
                        ha='center', va='center', color='black' 
                    )
                    
                base_value += sentiment_percentage  # Update the base for the next sentiment

    for sentiment in sentiment_labels:
        ax.bar(key_name_, 0,  # Dummy bar for the legend
         color=sentiment_colors[sentiment],
         label=sentiment)
                
                     
    ax.set_xlabel(x_label)
    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.legend(title="Sentiment", bbox_to_anchor=(1.05, 1), loc='upper left')

    if rotation != 0:
        plt.xticks(rotation=rotation)

    plt.tight_layout()
    st.pyplot(plt)
    plt.close()
    
    
def wordcloud_func(df):
    words_dict = df.set_index("norm_words")["Frequency"].to_dict()
    wordcloud = WordCloud(width=800, height=400, background_color="white")
    wordcloud.generate_from_frequencies(words_dict)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)


def gui_template(df, title, options, word_insight, sentiment_insight, artist_insight, theme_insight):

    sentiment_colors = {
        'positive': 'green',
        'negative': 'red',
        'neutral': 'yellow'
    }
    
    ( artist_stat,
      norm_words_stat,
      theme_stat,
      sentiment_single_dist,
      sentiment_avg_dist,
      avg_words_per_song ) = general_statistics(df)

    analysis_option = st.sidebar.selectbox("Select analysis", options)

    if analysis_option == "General":
        st.markdown(
            f"<h1 style='text-align: center;'>{title}</h1>",
            unsafe_allow_html=True,
        )
        wordcloud_func(norm_words_stat)
        single_sentiment_markdown = max_sentiment_to_text(sentiment_single_dist)
        avg_sentiment_markdown = avg_sentiment_to_text(sentiment_avg_dist)

        st.markdown(
            GENERAL_GENERAL_INSIGHT.format(
                len_songs=len(df),
                len_diff_artists=len(artist_stat),
                single_sentiment=single_sentiment_markdown,
                avg_sentiment=avg_sentiment_markdown,
                avg_song_len=avg_words_per_song,
            )
        )

    elif analysis_option == "Word":
        st.markdown(
            '<h4 style="font-size:15px;text-align: center;">Frequency & Percentage as function of the normalized words form</h4>',
            unsafe_allow_html=True,
        )
        plot_top_percentage(
            df=norm_words_stat,
            x_label="Words",
            title="Words Percentage",
            rotation=90,
            samples_num=20,
        )

        st.subheader("Conclusions")
        st.markdown(word_insight)

    elif analysis_option == "Sentiment":
        st.write(
            "This graph is the average song sentiment (Averaging all the sentiments of the songs):"
        )
        plot_top_percentage(
            df=sentiment_avg_dist,
            x_label="Sentiment",
            title="Average Sentiment Percentage",
            sentiment_colors=sentiment_colors,
            annot_bar=False,
            rotation=0,
        )

        st.write(
            "The maximum sentiment percentage is selected as the single song sentiment:"
        )
        plot_top_percentage(
            df=sentiment_single_dist,
            x_label="Sentiment",
            title="Single Sentiment Percentage",
            sentiment_colors=sentiment_colors,            
            rotation=0,
        )
        

    elif analysis_option == "Artist":
        
        st.subheader("Conclusions")
        st.markdown(artist_insight)
        plot_top_samples_with_sentiments(nested_dict=artist_stat, 
                                         x_label="Artist",
                                         title="Artist Percentage",
                                         sentiment_colors=sentiment_colors,
                                         rotation=90)
    elif analysis_option == "Theme":
        gt_names = list(theme_stat.keys())
        gs_numbered = "\n".join([f"{i+1}. {k}" for i,(k,v)  in enumerate(theme_stat.items())])

        plot_top_samples_with_sentiments(nested_dict=theme_stat, 
                                         x_label="Theme",
                                         title="Theme percentage",
                                         sentiment_colors=sentiment_colors,                                         
                                         rotation=90)
        
        st.subheader("Conclusions")
        st.markdown(theme_insight)
        st.subheader("General songs theme list:")
        st.markdown(gs_numbered)
