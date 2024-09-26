import os

TAG = 'bachata'
SONGS_LIMIT = 1000
SPANISH_THRESHOLD = 0.98

# Local definitions
BASE_DIR = os.getcwd()
CHORUS_SAMPLE_NUMBER = 50
CHORUS_SAMPLE_DIR_NAME = 'chorus_sample'

###### Directories ######
DATA_DIR = os.path.join(BASE_DIR, 'data_dir')
DATA_THEME_DIR = os.path.join(DATA_DIR, 'themes')
DATA_THEME_SONG_JSOL_DIR = os.path.join(DATA_THEME_DIR, 'jsol')
DATA_THEME_SINGERS_DIR = os.path.join(DATA_THEME_DIR, 'singers')
CHORUS_SAMPLE_DIR = os.path.join(BASE_DIR, CHORUS_SAMPLE_DIR_NAME)
##########################

# Files
DATA_FILE = os.path.join(DATA_DIR, 'data.csv') # Original data
FINAL_DATA_FILE = os.path.join(DATA_DIR, 'final_data.csv') # Final data

####### Theme data #######
DATA_JSOL_DIR = os.path.join(DATA_THEME_SONG_JSOL_DIR, 'jsol')
GENERAL_SONGS_THEMS = os.path.join(DATA_THEME_DIR, 'general_themes.csv')
GENERAL_SONGS_THEMS_LOG = os.path.join(DATA_THEME_DIR, 'general_themes.log')
BATCH_THEME_JSOL_FILE = os.path.join(DATA_JSOL_DIR, 'song_theme')
##########################

#### Sentiment data #####
BATCH_SENTIMENT_JSOL_FILE = os.path.join(DATA_JSOL_DIR, 'song_sentiment')
#########################

GENIUS_API_TOKEN = 'Od2yrHNfOCRHimIH3ev-wGZxZNJz3-47I4QfpzihKstD4eQaCItV28UJ72MAiV2W'

NOT_BACHATA = [
    'Lo Que Pasó, Pasó by Daddy Yankee',
    'Noche De Travesura by Héctor “El Father” (Ft. Divino)',
    'RUMBATÓN by Daddy Yankee',
    'Piel Morena by Thalía',
    'El Amor by Tito "El Bambino"',
    'LA FAMA (Live en el Palau Sant Jordi) by ROSALÍA',
    'Plutón by Arcángel',
    'Despacito (Remix) by Antony Santos (Ft. Mark B)',
    'No Me Caso by Trebol Clan & DJ Joe',
    '123 En 4 by Don Miguelo (Ft. Sensato)',
    'Coco Boy by Los Sufridos',
    'No Pares by Chris Palace',
    'PORQUE YA NO ME QUIERES by La Mafia del Amor',
    'Pobre Diabla (Remix) by Don Omar',
    'INTERLUDIO DE LA DARKCHATA: vigilia by MORY',
    'Otra Noche Loca by Leoni Torres (Ft. Louis Mikán)'
]

ADDITIONAL_WORDS_REMOVAL = ['ay', 'oh', 'pa', 'tá', 'eh','yeah', 'i','the','and','you', 'to', 'ah', 'ey', 'na', 'it', 'your','my','co','this','uh','te','me','el','se','al','la','lo','los','las','mi','a','tuyo','tuyos','mio','mia','mios','mias','mis','suyo', 'suyos','tu','su','sus','tus', 'a-ah','él','usted', 'ustedes', 'soy', 'ser']

# CHatGpt prompts
##### Find single song theme #####

OPENAI_BATCH_SIZE = 100
OPENAI_MODEL = "gpt-4o"
CHATGPT_MODEL_CONTEXT_WINDOW = 128000

OPENAI_EMBEDDINGS_MODEL = 'text-embedding-3-small'

THEME_PROMPT = 'write the theme of the song in short sentence:\nWrite like this - The song  theme is: ...\nThe song:\n\n{song}\n\n'
SENTIMENT_PROMPT='analyze the overall sentiment in terms of:\nneural, positive, negative\nfor the following song:\n\n{song}\n\nwrite only in json format with the appropriate decimal percentage. Make sure the sentiment percentage sum to 1.'
FAILED_ADD_SENTIMENT_TEXT = "Make sure that one of the sentiments has the highest value\nMake sure the sentiment percentage sum to 1."

ARTIST_GENDER_PROMPR='analyze the gender of the prominent artist, which can be one of the follows:\nMale, Female, Both\nThe artist name and song title following by the lyrics is: {song}\nMake sure it has this Json format: {{"gender": "Male"/"Female"/"Both"}}.\nWrite only the dict without additional text.'

###################################

##### Cluster all song themes to small number of general themes #####
MAX_THEME_CLUSTER_SIZE = 20
THEME_BATCH_SIZE = 100
ROBERTA_EMBEDDINGS_MODEL = 'sentence-transformers/all-roberta-large-v1'

SONGS_CLUSTERING_PROMPT = "Cluster the following song themes into brief general themes:\n\n{batch_text}\n\nPlease provide the clusters in a clean Python list format without any extra text or formatting. The list should be written exactly as a Python list, like this: [\"...\",\"...\",\"...\"].\n\nEnsure there are no additional markers or explanations—just the list."
CLUSTERS_PROMPT = f'These song theme clusters\nGroup these song themes into broader, more concise categories, combining similar themes and removing redundancy.\nCombine them into less than {MAX_THEME_CLUSTER_SIZE} ' + 'categories\nThe output should look like: ["...","...","..."].\n{batch_text}\nEnsure all clusters are combined into a single, flat Python list with no nested lists.'
#####################################################################
SENTIMENT_COLORS = {
        'positive': 'green',
        'negative': 'red',
        'neutral': 'yellow'
    }

SENTIMENT = ["negative", "positive", "neutral"]
