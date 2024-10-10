# Batchata music statistics    

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Conclusions](#Conclusions)
- [Process](#Process)

## Installation
1. Git clone the repository:
```
git clone https://github.com/orlevit/latin_music_statistics.git
```
2. Create virtual environment.
3. Install python packages within the virtual environment:
```
python install -r requirmentx.txt
```

## Usage
Run streamlit:
```
streamlit run gui_dir/gui.py(
```
## Dara preProcess
1000 songs were doneloaded through "Genius" API (collection of song lyrics) under the "Batchata" gener type.
They were examined with chatGPT for filtering suggested song that might have been wrongly classified as "Batchata" gener and listen to them. In addition, songs that have less than 98% Spanish words were filtered out. Only 842 were actually Batchata songs. Each song were given a theme(short summary of the song) and sentiment (how much of the song is "Neutral"/"Negative"/"Positive"), Those themes and theme were tested to see if they are make sence manually. (theme - 0/54  had wrong results for the theme. 5/18 - had wrong results for the neutral sentiment(3 positive/2 negative). 0/18 - had wrong results for the "Negative" sentiment. 3/18 - had wrong results for the "Negative" sentiment (1 neutral/2 negative).
filters were applied on those songs as multiple formats of phrases were added to the songs and are not part of the songs lyrics (iterative manual examination process until 50 consective lyrics were without additional unnecessary words).

## Conclusions

