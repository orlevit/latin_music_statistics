THEME_BATCH_SIZE = 100
#SONGS_CLUSTERING_PROMT = 'Cluster the following song themes into brief general themes:\n\n{batch_text}\nWrite only the song theme clusters it as a list.\nThe output should look like a list as: ["...","...","..."].\nOnly write the list!\n'
SONGS_CLUSTERING_PROMPT = "Cluster the following song themes into brief general themes:\n\n{batch_text}\n\nPlease provide the clusters in a clean Python list format without any extra text or formatting. The list should be written exactly as a Python list, like this: [\"...\",\"...\",\"...\"].\n\nEnsure there are no additional markers or explanations—just flat Python list with no nested lists.\nDo not write description, only the general themes\nDouble check it is single flat list"
# CLUSTERS_PROMT  = 'These song theme clusters\nGroup these song themes into broader, more concise categories, combining similar themes and removing redundancy.\nCombine them to less than {cotagoreis} categories\nWrite it as single pyhton list.\n{batch_text}\n\nThe output should look like: ["...","...","..."]\nThe concise clusters as python list are\n'
CLUSTERS_PROMPT = 'These song theme clusters\nGroup these song themes into broader, more concise categories, combining similar themes and removing redundancy.\nCombine them into less than {categories} categories\nThe output should look like: ["...","...","..."].\nEnsure all clusters are combined into a single, flat Python list with no nested lists.'

OPENAI_MODEL = "gpt-4o"
MAX_THEME_CLUSTER_SIZE = 20
import ast

def chatgpt_request_list_extraction(msgs, model_name):
    response = client.chat.completions.create(model=model_name, messages=msgs)
    return response
    
def requesft_clustering(batch_list, model_name):
    batch_text = "\n".join(batch_list)
    prompt = CLUSTERING_PROMT.format(batch_text=batch_text)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
    )
    return response
    
def extract_valid_list(response_text, model_name, max_attempts=5):
    attempt = 0
    chatgpt_messages = []

    while attempt < max_attempts:

        try:
            # Try to evaluate the response content to see if it's a valid list
            extracted_list = ast.literal_eval(response_text)
            if isinstance(extracted_list, list):
                return extracted_list
        except (SyntaxError, ValueError):
            print(f"Attempt: {attempt + 1} to extract the python list form the text")
            attempt += 1
            content = f"The previous {attempt + 1} attempt to extract of the valid python list from the text failed.\n Wxtract valid Python list with no additional text, formatting, or code. The output should look exactly like this: [\"...\"].\nProvide only the list, nothing else."
            chatgpt_messages.append({"role": "user", "content": response_text})
            chatgpt_messages.append({"role": "user", "content": content})
            # If it fails, resend the request to ChatGPT
            # extraction_prompt = prompt.format(clusters_list=response_text)
            extraction_response = chatgpt_request_list_extraction(chatgpt_messages, model_name)
            response_text = extraction_response.choices[0].message.content
    # If it still fails after the maximum number of attempts, raise an exception
    raise ValueError("Failed to extract a valid Python list after multiple attempts.")

def prepare_chatgpt_msg(curr_list, prev_list):
    prev_text = "\n".join(prev_list)
    curr_text = "\n".join(curr_list)

def batch_process_themes(list_to_cluster, prev_list_to_cluster, prompt, theme_batch_size, model):
    row_i = 0
    total_clusters = []
    total_len =len(list_to_cluster)
    
    while row_i <= total_len:
        batch_list = list_to_cluster[i: i + theme_batch_size]
        response = request_clustering(batch_list, model)
        curr_batch_size = theme_batch_size

        # Check if the response is not finished properly
        while response.choices[0].finish_reason != "stop":
            print(f"Batch {row_i} to {row_i + curr_batch_size} didn't complete. Reducing batch size.")
            curr_batch_size = max(1, curr_batch_size // 2)  # Reduce batch size by half, but not below 1
            batch_list = list_to_cluster[i: min(row_i + curr_batch_size, df_len)]
            response = request_clustering(batch_list, model)

        response_text = response.choices[0].message.content

        try:
            response_as_list = extract_valid_list(response_text, OPENAI_MODEL, max_attempts=5)
        except ValueError as e:
            print(f"Failed to extract valid list from CHATGPT prompt")
            return(total_clusters) ,1

        print('-'*200)
        print(response_as_list)
        print('-'*200)
        total_clusters.extend(response_as_list)
        print(f"Processed batch {row_i} to {row_i + THEME_BATCH_SIZE}")

        row_i += curr_batch_size
        
    return total_clusters, 0 

b= []
song_list = df['theme'].tolist()
clustered_themes, failed_extraction = batch_process_themes(song_list, '', SONGS_CLUSTERING_PROMPT, THEME_BATCH_SIZE, OPENAI_MODEL)
b.append(clustered_themes)

prev_clustered_clusters_text = ''
while (not failed_extraction) and (MAX_THEME_CLUSTER_SIZE < len(clustered_themes)):
    print(f"The number of clusters: {len(clustered_themes)}")
    curr_clustered_themes, failed_extraction = batch_process_themes(clustered_themes, prev_clustered_clusters_text, CLUSTERS_PROMPT.format(categories=MAX_THEME_CLUSTER_SIZE), THEME_BATCH_SIZE, OPENAI_MODEL)
    prev_clustered_clusters_text = clustered_themes
    clustered_themes = curr_clustered_themes

    b.append(clustered_themes)

print(f"The final number of clusters: {len(clustered_themes)}")
