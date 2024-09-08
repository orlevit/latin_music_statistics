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


def wordcloud_func(df):
    words_dict = df.set_index("norm_words")["Frequency"].to_dict()
    wordcloud = WordCloud(width=800, height=400, background_color="white")
    wordcloud.generate_from_frequencies(words_dict)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)
