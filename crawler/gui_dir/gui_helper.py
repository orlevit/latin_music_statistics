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

def plot_top_percentage(df, x_label, title, annot_bar=True, rotation=0, samples_num=10):

    top_df = df.sort_values(by="Percentage", ascending=False).head(samples_num)

    # Create the bar plot
    bars = plt.bar(top_df.iloc[:, 0], top_df["Percentage"], color="skyblue")

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

def wordcloud_func(df):
    words_dict = df.set_index("norm_words")["Frequency"].to_dict()
    wordcloud = WordCloud(width=800, height=400, background_color="white")
    wordcloud.generate_from_frequencies(words_dict)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)


def gui_template(df, title, options, word_insight, sentiment_insight, artist_insight, theme_insight):

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
            rotation=0,
        )

    elif analysis_option == "Artist":
        plot_top_percentage(
            df=artist_stat,
            x_label="Artist",
            title="Artist Percentage",
            rotation=90,
            samples_num=20,
        )
        st.subheader("Conclusions")
        st.markdown(artist_insight)

    elif analysis_option == "Theme":
        gt_names = set(df["general_theme"].tolist())
        gs_numbered = "\n".join([f"{i+1}. {item}" for i, item in enumerate(gt_names)])
        plot_top_percentage(df=theme_stat, x_label="Theme", title="Theme percentage", rotation=90)

        st.subheader("Conclusions")
        st.markdown(theme_insight)
        st.subheader("General songs theme list:")
        st.markdown(gs_numbered)
