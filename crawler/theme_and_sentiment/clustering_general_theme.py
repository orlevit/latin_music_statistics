import ast
import time
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from config import MAX_THEME_CLUSTER_SIZE, THEME_BATCH_SIZE, SONGS_CLUSTERING_PROMPT, CLUSTERS_PROMPT, OPENAI_MODEL


##### Create general themes out of all the songs themes #####
def chatgpt_request_list_extraction(msgs, model_name):
    response = client.chat.completions.create(model=model_name, messages=msgs)
    return response
    
def extract_valid_list(response_text, model_name, logger, max_attempts=5):
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
            extraction_response = chatgpt_request_list_extraction(chatgpt_messages, model_name)
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


def batch_process_themes(list_to_cluster, prev_text, base_prompt, theme_batch_size, model, logger):
    row_i = 0
    total_clusters = []
    total_len =len(list_to_cluster)
    
    while row_i <= total_len:
        chatgpt_msg_request = python_list_to_batch_text_promt(base_prompt, list_to_cluster, prev_text, theme_batch_size, row_i, total_len)
        response = chatgpt_request_list_extraction(chatgpt_msg_request, model)
        curr_batch_size = theme_batch_size

        # Check if the response is not finished properly
        while response.choices[0].finish_reason != "stop":
            logger.info(f"Batch {row_i} to {row_i + curr_batch_size} didn't complete. Reducing batch size.")

            curr_batch_size = max(1, curr_batch_size // 2)  # Reduce batch size by half, but not below 1
            chatgpt_msg_request = python_list_to_batch_text_promt(base_prompt, batch_list, prev_text, theme_batch_size, row_i, total_len)
            response = chatgpt_request_list_extraction(chatgpt_msg_request, model)

        response_text = response.choices[0].message.content

        try:
            response_as_list = extract_valid_list(response_text, OPENAI_MODEL, logger, max_attempts=5)
        except ValueError as e:
            logger.error("Failed to extract valid list from ChatGOT prompt")            
            return(total_clusters) ,1
            
        total_clusters.extend(response_as_list)
        logger.info(f"Processed batch {row_i} to {row_i + THEME_BATCH_SIZE}")

        row_i += curr_batch_size
        
    return total_clusters, 0 

def get_general_themes(df, logger):
    prev_text = ''
    song_list = df['theme'].tolist()
    
    clustered_themes, failed_extraction = batch_process_themes(song_list, prev_text, SONGS_CLUSTERING_PROMPT, THEME_BATCH_SIZE, OPENAI_MODEL, logger)
    
    len_clusters_before = len(clustered_themes)
    continue_clustring = check_max_clusters(failed_extraction, MAX_THEME_CLUSTER_SIZE, len_clusters_before)
    
    decreasing_clusters_attempt = 1
    logger.info(f"Initial number of clusters: {len_clusters_before}")
    
    while continue_clustring:
        curr_clustered_themes, failed_extraction = batch_process_themes(clustered_themes, prev_text, CLUSTERS_PROMPT, THEME_BATCH_SIZE, OPENAI_MODEL, logger)
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
    
        continue_clustring = check_max_clusters(failed_extraction, MAX_THEME_CLUSTER_SIZE, len_clusters_after)
    
        clustered_themes = curr_clustered_themes
        len_clusters_before = len_clusters_after


    logger.info(f"The final number of clusters: {len(clustered_themes)}")


##### create specific song themes embeddings and match the closest general theme embeddings #####

def create_embeddings(df, model, src_col, tgt_col):
    df[tgt_col] = None
    
    tic = time.time()
    
    # Use tqdm to add a progress bar to the loop
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
        response_emb = model.encode(row[src_col])    
        df.at[index, tgt_col] = response_emb
    
    # Track the end time
    toc = time.time()
    
    # Print the time taken in minutes
    print(f"Time taken: {(toc - tic) / 60:.2f} minutes")


def find_closest_embeddings(df, general_themes_df):
    # Assuming embeddings are stored as lists or numpy arrays in the DataFrame columns
    df['closest_general_theme'] = None

    for idx, theme_emb in df.iterrows():
        current_embedding = theme_emb['theme_emb']
        
        # Initialize variables to find the closest match
        min_dist = float('inf')
        closest_theme = None
        
        # Iterate over general_themes_df to find the closest match
        for _, general_row in general_themes_df.iterrows():
            general_embedding = general_row['general_theme_emb']
            general_theme = general_row['general_theme']
            
            # Compute cosine similarity (distance) between the current embedding and the general embeddings
            dist = cosine(current_embedding, general_embedding)

            # Update closest match if a smaller distance is found
            if dist < min_dist:
                min_dist = dist
                closest_theme = general_theme
        
        # Store the closest theme in the df
        df.at[idx, 'general_theme'] = closest_theme

    return df

# emb_model = SentenceTransformer(ROBERTA_EMBEDDINGS_MODEL)
# create_embeddings(df, emb_model, 'theme', 'theme_emb')
# create_embeddings(general_themes_df,  emb_model, 'general_theme', 'general_theme_emb')
# result_df = find_closest_embeddings(df, general_themes_df)
# result_df.to_csv('final_data.csv', index=False)