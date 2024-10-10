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

# Preprocessing Corpus of Bachata Song Lyrics

The original corpus consists of 1,000 songs, which were downloaded using the "Genius" API, with a focus on the Bachata genre.
Out of those 1000, only 842 remained.
Below are the steps followed during the preprocessing phase:

## Data Collection
- **Source:** The song lyrics were retrieved via the "Genius" API.
- **Genre:** All songs were classified under the "Bachata" genre.
  
## Data Filtering

### Genre Validation
- **ChatGPT-Assisted Validation:** Each song's genre was reviewed with the assistance of ChatGPT to ensure it was correctly classified as Bachata. If a song was incorrectly labeled, it was listened to for verification.
  
### Language Filtering
- **Spanish Word Count:** Songs with less than 98% Spanish words were excluded from the corpus.
  
## Song Annotation

Each song was further processed by assigning two key attributes:
1. **Theme:** A short summary that describes the overall theme of the song.
2. **Sentiment:** The sentiment of the song, categorized as either "Neutral", "Negative", or "Positive".

### Manual Validation of Annotations
- **Theme Accuracy:** Out of 54 tested themes, none were found to be incorrect.
- **Sentiment Accuracy:**
  - Out of 18 songs with "Neutral" sentiment, 5 were misclassified (3 should have been "Positive" and 2 "Negative").
  - All songs labeled as "Negative" were correctly classified.
  - For songs labeled as "Positive", 3 were misclassified (1 should have been "Neutral" and 2 "Negative").

## Data Cleanup

An iterative process was applied to ensure that the lyrics were free from non-lyrical content:
- **Manual Examination:** Multiple phrases and non-lyrical elements (e.g., advertisements or artist comments) were manually removed from the lyrics. This process was repeated until 50 consecutive songs were found to have no extraneous content.

## Conclusions

