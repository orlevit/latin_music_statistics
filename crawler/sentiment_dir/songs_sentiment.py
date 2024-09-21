from config import OPENAI_MODEL, SENTIMENT_PROMPT, FINAL_DATA_FILE

def prepare_chatgpt_msg(curr_text, prev_text, chatgpt_messages):
    chatgpt_messages.append({"role": "user", "content": prev_text})
    chatgpt_messages.append({"role": "user", "content": curr_text})
    return chatgpt_messages

def chatgpt_request_extraction(msgs, model_name, client):
    response = client.chat.completions.create(model=model_name, messages=msgs)
    return response

def extract_valid_dict(response_text, model_name, client, logger, max_attempts=5):
    attempt = 0
    chatgpt_messages = []

    while attempt < max_attempts:
        try:
            extracted_dict = ast.literal_eval(response_text)
            if isinstance(extracted_dict, dict):
                return extracted_dict
                
        except (SyntaxError, ValueError):
            logger.info(f"Attempt: {attempt + 1} to extract the Python dictionary from the text")
            attempt += 1
            prev_content = f"The previous {attempt + 1} attempt to extract of the valid Python dictionary from the text failed.\n" \
                            f"The previous result was: {response_text}\n" \
                            "Extract valid Python dictionary with no additional text, formatting, or code. The output should look exactly like this: {\"...\"}.\n" \
                            "Provide only the dictionary, nothing else.\nMake sure that one of the sentiments has the highest value\n" \
                            "Make sure the sentiment percentage sum to 1."
            
            chatgpt_messages = prepare_chatgpt_msg(response_text, prev_content, chatgpt_messages)
            extraction_response = chatgpt_request_extraction(chatgpt_messages, model_name, client)
            response_text = extraction_response.choices[0].message.content
    
    raise ValueError("Failed to extract a valid Python list after multiple attempts.")

def get_dominant_sentiment(sentiment_dict_input):
    try:
        sentiment_dict = eval(sentiment_dict_input)
    except TypeError as e:
        sentiment_dict = sentiment_dict_input

   # print(sentiment_dict)
    if sentiment_dict['positive'] == sentiment_dict['negative']:
        #print(sentiment_dict_input)
        print('1')
        dominant_sentiment = 'neutral'
    else:
        dominant_sentiment = max(sentiment_dict, key=sentiment_dict.get)
    return dominant_sentiment


def calc_sentiment(df, dict_sentiment_col, select_sentiment_col):
    df[select_sentiment_col] = df[dict_sentiment_col].apply(get_dominant_sentiment)


def find_sentiment(df, song_lyrics_col, tgt_col, client, logger, model_name, sentiment_prompt):
    for ii, (idx, row) in enumerate(df.iterrows()):
        prompt = sentiment_prompt.format(song=row[song_lyrics_col])
        chatgpt_msg_request = prepare_chatgpt_msg(prompt, '', [])
        response = chatgpt_request_extraction(chatgpt_msg_request, model_name, client)
        response_text = response.choices[0].message.content
        
        extracted_dict = extract_valid_dict(response_text, model_name, client, logger, max_attempts=5)
        df.loc[idx, tgt_col] = str(extracted_dict)

    calc_sentiment(df, 'sentiment', 'selected_sentiment')

def openai_sentiment_finder(df, client, openai_model, ,song_lyrics_col='lyrics', tgt_col='sentiment'):                                                                                                 
    # Establish logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()          # Log messages to the console (stdout)
        ]
    )
    logger = logging.getLogger(__name__)

    find_sentiment(df, song_lyrics_col, tgt_col, client, logger, openai_model, SENTIMENT_PROMPT)