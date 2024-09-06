import os

TAG = 'bachata'
SONGS_LIMIT = 1000
SPANISH_THRESHOLD = 0.98

# Local definitions
BASE_DIR = os.getcwd()
CHORUS_SAMPLE_NUMBER = 50
CHORUS_SAMPLE_DIR_NAME = 'chorus_sample'

DATA_DIR = os.path.join(BASE_DIR, 'data_dir')
DATA_FILE = os.path.join(DATA_DIR, 'data.csv')
GENERAL_SONGS_THEMS = os.path.join(DATA_DIR, 'general_themes.csv')

FINAL_DATA_FILE = os.path.join(DATA_DIR, 'final_data.csv') # after add openai theme and sentiment
PROCESSED_DATA_FILE = os.path.join(DATA_DIR, 'processed_data.csv')
DATA_JSOL_DIR = os.path.join(DATA_DIR, 'jsol')

BATCH_THEME_JSOL_FILE = os.path.join(DATA_JSOL_DIR, 'song_theme')
BATCH_SENTIMENT_JSOL_FILE = os.path.join(DATA_JSOL_DIR, 'song_sentiment')

CHORUS_SAMPLE_DIR = os.path.join(BASE_DIR, CHORUS_SAMPLE_DIR_NAME)
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

ADDITIONAL_WORDS_REMOVAL = ['ay', 'oh', 'pa', 'tá', 'eh','yeah', 'i','the','and','you']

OPENAI_BATCH_SIZE = 100
OPENAI_MODEL = "gpt-4o"
CHATGPT_MODEL_CONTEXT_WINDOW = 128000

OPENAI_EMBEDDINGS_MODEL = 'text-embedding-3-small'
THEME_PROMPT = 'write the theme of the song in short sentence:\nWrite like this - The song  theme is: ...\nThe song:\n\n{song}\n\n'
SENTIMENT_PROMPT='analyis the overall sentiment in terms of:\nneural, positive, negative\nfor the following song:\n\n{song}\n\nnwrite only in json formt with the appropriate decimal percentage'