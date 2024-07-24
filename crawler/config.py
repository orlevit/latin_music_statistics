import os

TAG = 'bachata'
SONGS_LIMIT = 1000
SPANISH_THRESHOLD = 0.98

# Local definitions
BASE_DIR = os.getcwd()
CHORUS_SAMPLE_NUMBER = 50
CHORUS_SAMPLE_DIR_NAME = 'chorus_sample'

DATA_FILE = os.path.join(BASE_DIR, 'data.csv')
CHORUS_SAMPLE_DIR = os.path.join(BASE_DIR, CHORUS_SAMPLE_DIR_NAME)
GENIUS_API_TOKEN = 'Od2yrHNfOCRHimIH3ev-wGZxZNJz3-47I4QfpzihKstD4eQaCItV28UJ72MAiV2W'
