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
PROCESSED_DATA_FILE = os.path.join(DATA_DIR, 'processed_data.csv')

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