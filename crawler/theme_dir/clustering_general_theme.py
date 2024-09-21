import os
import ast
import time
import math
import logging
import numpy as np
import pandas as pd
import streamlit as st

from tqdm import tqdm
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import MAX_THEME_CLUSTER_SIZE, THEME_BATCH_SIZE, SONGS_CLUSTERING_PROMPT, CLUSTERS_PROMPT, OPENAI_MODEL, DATA_THEME_SINGERS_DIR, ROBERTA_EMBEDDINGS_MODEL


##### Create general themes out of all the songs themes #####
def chatgpt_request_list_extraction(msgs, model_name, client):
    response = client.chat.completions.create(model=model_name, messages=msgs)
    return response
    
def extract_valid_list(response_text, model_name, client, logger, max_attempts=5):
    attempt = 0
    chatgpt_messages = []

    while attempt < max_attempts:

        try:
            extracted_list = ast.literal_eval(response_text)
            if isinstance(extracted_list, list):
                return extracted_list
                
        except (SyntaxError, ValueError):
            logger.info(f"Attempt: {attempt + 1} to extract the Python list from the text")
            attempt += 1
            prev_content = f"The previous {attempt + 1} attempt to extract of the valid python list from the text failed.\n Extract valid Python list with no additional text, formatting, or code. The output should look exactly like this: [\"...\"].\nProvide only the list, nothing else."
            chatgpt_messages = prepare_chatgpt_msg(response_text, prev_content, chatgpt_messages)
            extraction_response = chatgpt_request_list_extraction(chatgpt_messages, model_name, client)
            response_text = extraction_response.choices[0].message.content
    
    raise ValueError("Failed to extract a valid Python list after multiple attempts.")

def prepare_chatgpt_msg(curr_text, prev_text, chatgpt_messages):
    chatgpt_messages.append({"role": "user", "content": prev_text})
    chatgpt_messages.append({"role": "user", "content": curr_text})
    return chatgpt_messages

def python_list_to_batch_text_promt(base_prompt, a_list, prev_text, batch_size, row_i, max_len):
    batch_text = "\n".join(a_list[row_i: min(row_i + batch_size, max_len)])
    prompt = base_prompt.format(batch_text=batch_text)
    chatgpt_msg_request =  prepare_chatgpt_msg(prompt, prev_text, [])
    return chatgpt_msg_request

def check_max_clusters(failed_extraction, max_theme_clusters_size ,len_clusters_before):
    return (not failed_extraction) and (max_theme_clusters_size < len_clusters_before)


def batch_process_themes(list_to_cluster, prev_text, base_prompt, theme_batch_size, model, client, logger):
    row_i = 0
    total_clusters = []
    total_len =len(list_to_cluster)
    
    while row_i <= total_len:
        chatgpt_msg_request = python_list_to_batch_text_promt(base_prompt, list_to_cluster, prev_text, theme_batch_size, row_i, total_len)
        response = chatgpt_request_list_extraction(chatgpt_msg_request, model, client)
        curr_batch_size = theme_batch_size

        # Check if the response is not finished properly
        while response.choices[0].finish_reason != "stop":
            logger.info(f"Batch {row_i} to {row_i + curr_batch_size} didn't complete. Reducing batch size.")

            curr_batch_size = max(1, curr_batch_size // 2)  # Reduce batch size by half, but not below 1
            chatgpt_msg_request = python_list_to_batch_text_promt(base_prompt, batch_list, prev_text, theme_batch_size, row_i, total_len)
            response = chatgpt_request_list_extraction(chatgpt_msg_request, model, client)

        response_text = response.choices[0].message.content

        try:
            response_as_list = extract_valid_list(response_text, OPENAI_MODEL, client, logger, max_attempts=5)
        except ValueError as e:
            logger.error("Failed to extract valid list from ChatGOT prompt")            
            return(total_clusters) ,1
            
        total_clusters.extend(response_as_list)
        logger.info(f"Processed batch {row_i} to {row_i + THEME_BATCH_SIZE}")

        row_i += curr_batch_size
        
    return total_clusters, 0 

def get_general_themes(df, client, logger, max_clusters=None):
    if max_clusters is None:
        max_clusters = MAX_THEME_CLUSTER_SIZE
        
    prev_text = ''
    song_list = df['theme'].tolist()
    
    clustered_themes, failed_extraction = batch_process_themes(song_list, prev_text, SONGS_CLUSTERING_PROMPT, THEME_BATCH_SIZE, OPENAI_MODEL, client, logger)
    
    len_clusters_before = len(clustered_themes)
    continue_clustring = check_max_clusters(failed_extraction, max_clusters, len_clusters_before)
    
    decreasing_clusters_attempt = 1
    logger.info(f"Initial number of clusters: {len_clusters_before}")
    
    while continue_clustring:
        curr_clustered_themes, failed_extraction = batch_process_themes(clustered_themes, prev_text, CLUSTERS_PROMPT, THEME_BATCH_SIZE, OPENAI_MODEL, client, logger)
        prev_clusters_text = '\n'.join(clustered_themes)
        curr_clusters_text = '\n'.join(curr_clustered_themes)
        len_clusters_after = len(curr_clustered_themes)
        
        logger.info(f"The number of clusters: {len_clusters_after}")
    
        if len_clusters_before == len_clusters_after:
            decreasing_clusters_attempt += 1
            prev_text =  f'This is the {decreasing_clusters_attempt} attempt for clustering. ' +\
                         f'There are {len_clusters_after} many clusters - which are too many. ' +\
                         f'The previous clustered topic attempt was:\n{prev_clusters_text}\n\n\nTry again with those topics:\n' + curr_clusters_text
        else:
            decreasing_clusters_attempt = 1
            prev_text = ''
    
        continue_clustring = check_max_clusters(failed_extraction, max_clusters, len_clusters_after)
    
        clustered_themes = curr_clustered_themes
        len_clusters_before = len_clusters_after


    logger.info(f"The final number of clusters: {len(clustered_themes)}")
    return clustered_themes

##### create specific song themes embeddings and match the closest general theme embeddings #####

def create_embeddings(df, model, src_col, tgt_col):
    df[tgt_col] = None
    
    tic = time.time()
    
    # Use tqdm to add a progress bar to the loop
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
        response_emb = model.encode(row[src_col])    
        df.at[index, tgt_col] = response_emb.tolist()
    
    # Track the end time
    toc = time.time()
    
    # Print the time taken in minutes
    print(f"Time taken: {(toc - tic) / 60:.2f} minutes")


def find_closest_embeddings(df, general_themes_df):
    # Assuming embeddings are stored as lists or numpy arrays in the DataFrame columns

    for idx, theme_row in df.iterrows():
        try:
            current_embedding = eval(theme_row['theme_emb'])
        except TypeError as e:
            current_embedding = theme_row['theme_emb']
            
        vector1 = np.array(current_embedding).reshape(1, -1)

        # Initialize variables to find the closest match
        min_dist = float('inf')
        closest_theme = None
        
        # Iterate over general_themes_df to find the closest match
        for _, general_row in general_themes_df.iterrows():
            try:
                general_embedding = eval(general_row['general_theme_emb'])
            except TypeError as e:
                general_embedding = general_row['general_theme_emb']
                
            general_theme = general_row['general_theme']
            
            vector2 = np.array(general_embedding).reshape(1, -1)
            
            # Compute cosine similarity (distance) between the current embedding and the general embeddings
            dist = cosine_similarity(vector1, vector2)

            # Update closest match if a smaller distance is found
            if dist < min_dist:
                min_dist = dist
                closest_theme = general_theme
        
        # Store the closest theme in the df
        df.at[idx, 'general_theme'] = closest_theme

    return df

##### create specific themes for a artist #####

def create_specific_singer_theme(df, client, theme_dir, theme_file, log_file, final_file, cluster_num):
        
    # Establish logging
    os.makedirs(theme_dir, exist_ok = True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),  # Log messages to a file named 'app.log'
            logging.StreamHandler()          # Log messages to the console (stdout)
        ]
    )
    logger = logging.getLogger(__name__)

    # Find general themes
    general_themes_list = get_general_themes(df, client, logger, max_clusters = cluster_num)
    general_themes_df = pd.DataFrame(general_themes_list, columns = ['general_theme'])
    
    ### Embedding ###
    # emb_model = SentenceTransformer(ROBERTA_EMBEDDINGS_MODEL)
    # create_embeddings(general_themes_df,  emb_model, 'general_theme', 'general_theme_emb')
    # result_df = find_closest_embeddings(df, general_themes_df)

    match_generic_theme(df, general_themes_df, 'general_theme', client)
    
    general_themes_df.to_csv(theme_file, index = False)    
    df.to_csv(final_file, index=False)
    
    return df

def load_artist_theme_df(df, singer_name, client, cluster_num = None):
    ARTIST_GENERAL_THEME_DIR = os.path.join(DATA_THEME_SINGERS_DIR, singer_name)
    ARTIST_GENERAL_THEME_FILE = os.path.join(ARTIST_GENERAL_THEME_DIR, f'{singer_name}_general_themes.csv')
    ARTIST_GENERAL_THEME_LOG = os.path.join(ARTIST_GENERAL_THEME_DIR, f'{singer_name}_general_themes.log')
    ARTIST_FINAL_RESULTS_FILE = os.path.join(ARTIST_GENERAL_THEME_DIR, f'{singer_name}_final_results.csv')

    if cluster_num is None:
        cluster_num = len(df) // 10
            
    if os.path.exists(ARTIST_FINAL_RESULTS_FILE):
        artist_df = pd.read_csv(ARTIST_FINAL_RESULTS_FILE)

    elif client is not None:
        artist_df = create_specific_singer_theme(df,
                               client,                                           
                               ARTIST_GENERAL_THEME_DIR, 
                               ARTIST_GENERAL_THEME_FILE,
                               ARTIST_GENERAL_THEME_LOG,
                               ARTIST_FINAL_RESULTS_FILE,
                               cluster_num)
    else:
        st.title("There is no OPENAI key register for this new artist")
        raise("There is no OPENAI key register for this new artist")
        
    return artist_df

############### Match generic theme for each song theme ###############
def find_generic_theme(theme_txt, general_themes, client):
    
    MATCH_PROMPT = 'To which of the following general categories:\n{general_themes}\nThis theme fits best:\n{cur_theme}\nwrite only the catagory name:'
    WRONG_GENERAL_THEME =  'This is the {attempt_num} attempt.\n' +\
                 'You failed to extract the best fitting general theme out of the theme list.\n' +\
                 'You wrote name: "{name}" , which is not in the list.'


    attempt_num = 1
    curr_text = MATCH_PROMPT.format(general_themes=','.join(general_themes), cur_theme=theme_txt)
    chatgpt_msg_request = prepare_chatgpt_msg(curr_text, '', [])
    response = chatgpt_request_list_extraction(chatgpt_msg_request, OPENAI_MODEL, client)
    
    response_txt = response.choices[0].message.content
    while response_txt not in general_themes:
        attempt_num += 1
        prev_text = WRONG_GENERAL_THEME.format(attempt_num=attempt_num, name=response_txt)
    
        chatgpt_msg_request = prepare_chatgpt_msg(curr_text, prev_text, [])
        response = chatgpt_request_list_extraction(chatgpt_msg_request, OPENAI_MODEL, client)
        response_txt = response.choices[0].message.content
    
        print(f'{attempt_num}:\n\nprev_text {prev_text}')
        print('-'*100)
    return response_txt  

def match_generic_theme(df, df_general_themes, tgt_theme_col_name, client):
    df[tgt_theme_col_name] = ""
    general_themes = df_general_themes['general_theme'].tolist()
    
    # Use tqdm to add a progress bar to the loop
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
        result = find_generic_theme(row['theme'], general_themes, client)
        df.at[index, tgt_theme_col_name] = result

    
##################### clustering by specific artist

def filter_cluster_threshold(df_artist):
    unique_artist_gt_len = len(df_artist["general_theme"].unique())
    avg_samples_in_cluster = len(df_artist)// 10        
    denum_num = min(unique_artist_gt_len, avg_samples_in_cluster)
    artist_cluster_threshold = len(df_artist) // denum_num 

    return artist_cluster_threshold

def number_of_cluster(df_artist):
    unique_artist_gt_len = len(df_artist["general_theme"].unique())
    avg_samples_in_cluster = math.ceil(len(df_artist)// 10)
    artist_cluster_threshold = max(max(unique_artist_gt_len, avg_samples_in_cluster) ,6)
        
    return artist_cluster_threshold

def find_themes_specific_artist(df_artist, artist_name):
    OPENAI_KEY = os.getenv('OPENAI_KEY')

    if OPENAI_KEY:
        client = OpenAI(api_key=OPENAI_KEY)
    else:
        client = None

    artist_cluster_threshold = filter_cluster_threshold(df_artist)
    above_threshold = {key: value for key, value in  df_artist['general_theme'].value_counts().to_dict().items() if artist_cluster_threshold < value }
    df_artist_selected = df_artist[df_artist['general_theme'].isin(above_threshold.keys())]
    selected_cluster_num = number_of_cluster(df_artist_selected)

    df_specific_artist = load_artist_theme_df(df_artist, singer_name = artist_name, client=client, cluster_num = selected_cluster_num)

    return df_specific_artist

# emb_model = SentenceTransformer(ROBERTA_EMBEDDINGS_MODEL)
# create_embeddings(df, emb_model, 'theme', 'theme_emb')
# create_embeddings(general_themes_df,  emb_model, 'general_theme', 'general_theme_emb')
# result_df = find_closest_embeddings(df, general_themes_df)
# result_df.to_csv('final_data.csv', index=False)
