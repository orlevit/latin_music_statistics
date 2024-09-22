import os
import sys
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.abspath(os.path.join(parent_dir, "statistics_dir")))
sys.path.append(os.path.abspath(os.path.join(parent_dir, "theme_and_sentiment")))

from clustering_general_theme import find_themes_specific_artist
from general_functions import center_text
from statistics_dir.statistics import *
from conclusion_text import *
from config import SENTIMENT_COLORS, SENTIMENT


def plot_top_percentage(
    df,
    x_label,
    title,
    sentiment_colors=None,
    annot_bar=True,
    rotation=0,
    samples_num=10,
):

    top_df = df.sort_values(by="Percentage", ascending=False).head(samples_num)

    if sentiment_colors is None:
        sentiment_colors = "skyblue"
    else:
        sentiment_colors = top_df["Sentiment"].map(sentiment_colors).fillna('gray')

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


def plot_top_samples_with_sentiments(
    nested_dict,
    x_label,
    title,
    sentiment_colors,
    annot_bar=True,
    rotation=0,
    samples_num=10,
):

    # Taking the top N samples
    top_n_samples = dict(
        list(nested_dict.items())[:samples_num]
    )  # nested_dict should be sorted Reversed

    # Initialize plot
    fig, ax = plt.subplots(figsize=(17, 15))

    for item in (
        [ax.title, ax.xaxis.label, ax.yaxis.label]
        + ax.get_xticklabels()
        + ax.get_yticklabels()
    ):
        item.set_fontsize(20)
    # Set colors for different sentiments

    sentiment_labels = SENTIMENT
    # Plot each sentiment for the top categories
    for key_name, stats in top_n_samples.items():
        base_value = 0  # Start from the bottom for each bar

        # Get the sentiment data from the current theme
        sentiments = stats["Sentiments"]

        for sentiment in SENTIMENT:
            count = sentiments.get(sentiment, 0)  # Default to 0 if sentiment not found
            sentiment_percentage = (count / stats["Frequency"]) * stats["Percentage"]

            # Plot each sentiment as a stacked bar
            if count > 0:  # Only plot non-zero counts
                bar = ax.bar(
                    key_name,
                    sentiment_percentage,
                    bottom=base_value,
                    color=SENTIMENT_COLORS.get(sentiment, "blue"),
                )

                # Annotate each sentiment's count in the middle of its segment
                if annot_bar:
                    ax.text(
                        key_name,
                        base_value + sentiment_percentage / 2,
                        f"{count}",  # Annotate with the count
                        ha="center",
                        va="center",
                        color="black",
                        fontsize=20,
                    )

                base_value += (
                    sentiment_percentage  # Update the base for the next sentiment
                )

    for sentiment in sentiment_labels:
        ax.bar(
            key_name,
            0,  # Dummy bar for the legend
            color=SENTIMENT_COLORS[sentiment],
            label=sentiment,
        )

    ax.set_xlabel(x_label)
    ax.set_ylabel("Count")
    ax.set_title(title, fontsize=20)
    ax.legend(
        title="Sentiment",
        bbox_to_anchor=(1.05, 1),
        loc="upper left",
        prop={"size": 20},
        fontsize=20,
        title_fontsize=20,
    )

    if rotation != 0:
        plt.xticks(rotation=rotation)

    plt.tight_layout()
    st.pyplot(plt)
    plt.close()


def wordcloud_func(df):
    words_dict = df.set_index("norm_words")["Frequency"].to_dict()
    wordcloud = WordCloud(width=800, height=400, background_color="white")
    wordcloud.generate_from_frequencies(words_dict)
    
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")  # Turn off the axis
    st.pyplot(fig)

    #plt.imshow(wordcloud, interpolation="bilinear")
    #plt.axis("off")
    #st.pyplot(plt)


def gui_template(
    df,
    title,
    options,
    specific_artist_name,
    word_insight,
    sentiment_insight,
    artist_insight,
    theme_insight,
):


    (
        artist_stat,
        norm_words_stat_freq,
        # norm_words_stat_freq_sent,
        theme_stat,
        sentiment_single_dist,
        sentiment_avg_dist,
        avg_words_per_song,
    ) = general_statistics(df)

    analysis_option = st.sidebar.selectbox("Select analysis", options)

    if analysis_option == "General":
        st.markdown(
            f"<h1 style='text-align: center;'>{title}</h1>",
            unsafe_allow_html=True,
        )
        wordcloud_func(norm_words_stat_freq)
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
            df=norm_words_stat_freq,
            x_label="Words",
            title="Words Percentage",
            rotation=90,
            samples_num=20,
        )

        # plot_top_samples_with_sentiments(
        #     nested_dict=norm_words_stat_freq_sent,
        #     x_label="Words",
        #     title="Words Percentage",
        #     sentiment_colors=SENTIMENT_COLORS,
        #     rotation=90,
        #     samples_num=20
        # )
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
            sentiment_colors=SENTIMENT_COLORS,
            annot_bar=False,
            rotation=0,
        )

        st.write(
            "The maximum sentiment percentage is selected to represent the overall sentiment of the song:"
        )
        plot_top_percentage(
            df=sentiment_single_dist,
            x_label="Sentiment",
            title="Single Sentiment Percentage",
            sentiment_colors=SENTIMENT_COLORS,
            rotation=0,
        )

    elif analysis_option == "Data":
        st.dataframe(
            df[
                [
                    "title_with_artists",
                    "sentiment",
                    "theme",
                    "general_theme",
                    "selected_sentiment",
                ]
            ]
        )

    elif analysis_option == "Artist":

        plot_top_samples_with_sentiments(
            nested_dict=artist_stat,
            x_label="Artist",
            title="Artist Percentage",
            sentiment_colors=SENTIMENT_COLORS,
            rotation=90,
        )
        st.subheader("Conclusions")
        st.markdown(artist_insight)

    elif analysis_option == "Theme":
        # Plot specific themes
        if specific_artist_name != "":
            specific_artist_themes_df = find_themes_specific_artist(
                df, specific_artist_name
            )
            specific_artist_theme_stat = calculate_counts_with_sentiment(
                specific_artist_themes_df, "general_theme", "selected_sentiment"
            )

            st.markdown(center_text(f'{specific_artist_name} themes'), unsafe_allow_html=True)

            plot_top_samples_with_sentiments(
                nested_dict=specific_artist_theme_stat,
                x_label="Theme",
                title="Theme percentage",
                sentiment_colors=SENTIMENT_COLORS,
                rotation=90,
                samples_num=len(specific_artist_theme_stat)
            )

#            st.subheader("-" * 60)

        # Plot general themes
        st.markdown(center_text(f'General themes distribution by artist'), unsafe_allow_html=True)

        plot_top_samples_with_sentiments(
            nested_dict=theme_stat,
            x_label="Theme",
            title="Theme percentage",
            sentiment_colors=SENTIMENT_COLORS,
            rotation=90,
            samples_num=len(theme_stat)
        )

        st.subheader("Conclusions")
        st.markdown(theme_insight)
