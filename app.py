'''
This file contains the implementation of an audio-based AI assistant using Azure OpenAI. 
The assistant allows users to interact with it through text-based chat. 

The main functionalities of the assistant include:
- Chat-based conversation with the assistant
- Integration with different scenarios such as Car Loan Assistant, SOW Helper, and Edu Assistant

The code is organized into the following sections:
1. Importing necessary libraries and modules
2. Setting up environment variables and configurations
4. Setting up the Streamlit user interface
5. Handling user prompts and selecting the scenario
8. Handling user interactions and displaying chat messages

'''


import streamlit as st
import time
from openai import AzureOpenAI
import params

# Environment variables
speech_key = params.speech_key
service_region = params.service_region

aoai_base_url = params.aoai_base_url
aoai_key = params.aoai_key
aoai_version = params.aoai_version
deployment_name = params.deployment_name

ai_search_url = params.ai_search_url
ai_search_key = params.ai_search_key
# index_name = params.index_name
# ai_semantic_config = params.ai_semantic_config
# query_type = params.query_type


st.title(params.app_title)

if "messages" not in st.session_state:
    st.session_state.messages = []
    system_prompt = ""
    with open(params.sys_prompt_file, "r") as file:
        # system_prompt = file.read().replace('\n', '')
        system_prompt = file.read()
        st.session_state.messages.append({"role": "system", "content": system_prompt})

with st.sidebar:
    st.text_area(label="System Prompt", value=st.session_state.messages[0]['content'], height=250)

add_selectbox = st.sidebar.selectbox(
    "Select the scenario you would like to run?",
    ("Car Loan Assistant", "SOW Helper", "Edu Assistant")
)

if add_selectbox == "Car Loan Assistant":
    index_name = params.car_loan_index_name
    ai_semantic_config = params.car_loan_ai_semantic_config
    query_type = params.car_loan_query_type
    with open(params.car_loan_prompt_assist_file_name, "r") as file:
        user_prompt = file.read()
        st.sidebar.text_area(label="prompt suggestions",value=user_prompt, height=250)
elif add_selectbox == "SOW Helper":
    index_name = params.sow_index_name
    ai_semantic_config = params.sow_ai_semantic_config
    query_type = params.sow_query_type
    with open(params.sow_prompt_file_name, "r") as file:
        user_prompt = file.read()
        st.sidebar.text_area(label="prompt suggestions",value=user_prompt, height=250)
elif add_selectbox == "Edu Assistant":
    index_name = params.edu_index_name
    ai_semantic_config = params.edu_ai_semantic_config
    query_type = params.edu_query_type  
    with open(params.edu_prompt_file_name, "r") as file:
        user_prompt = file.read()
        st.sidebar.text_area(label="prompt suggestions",value=user_prompt,height=250)


counter = 0
for message in st.session_state.messages:
    if counter == 0:
        counter += 1
        continue
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


client = AzureOpenAI(
azure_endpoint = aoai_base_url, 
api_key=aoai_key, 
api_version=aoai_version
)

def get_response_to_user_query(play_audio=False):
    message_placeholder = st.empty()
    full_response = ""

    print("calling LLM now ....")
    for message in st.session_state.messages:
        print('I am printing the conversation history', message)
    for response in client.chat.completions.create(
    model=deployment_name,
    messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
    extra_body={
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": ai_search_url,
                    "index_name": index_name,
                    "query_type": query_type,
                    "semantic_configuration": ai_semantic_config,
                    "authentication": {
                    "type": "api_key",
                    "key": ai_search_key
                    }
                }
            }
        ]
    },
    stream=True
    ):
        # print(response)
        try:
            if len(response.choices) > 0:
                delta = response.choices[0].delta
                if delta.content:
                    full_response += delta.content
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        except Exception as e:
            print("Error", e.args)
            pass
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

if prompt := st.chat_input("Hello!!!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        get_response_to_user_query(False)