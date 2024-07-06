'''
This file contains the implementation of an audio-based AI assistant using Azure Cognitive Services and OpenAI. 
The assistant allows users to interact with it through speech recognition and text-based chat. It leverages Azure Cognitive Services for speech recognition and Azure Search for semantic search capabilities. It also uses OpenAI for generating responses to user queries.

The main functionalities of the assistant include:
- Speech recognition from microphone input
- Text-to-speech conversion for assistant responses
- Chat-based conversation with the assistant
- Integration with different scenarios such as Car Loan Assistant, SOW Helper, and Edu Assistant

# This can run only on local machine as it requires microphone input

The code is organized into the following sections:
1. Importing necessary libraries and modules
2. Setting up environment variables and configurations
3. Creating the speech recognizer and audio configuration
4. Setting up the Streamlit user interface
5. Handling user prompts and selecting the scenario
6. Generating responses to user queries using Azure Cognitive Services and OpenAI
7. Implementing speech recognition and text-to-speech functionalities
8. Handling user interactions and displaying chat messages

'''



import azure.cognitiveservices.speech as speechsdk
import streamlit as st
import time
from openai import AzureOpenAI
import params
import base64
from azure.cognitiveservices.speech import AudioDataStream

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

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
audio_config = speechsdk.AudioConfig(use_default_microphone=True)

# Create a speech recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# Add FontAwesome CSS stylesheet
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)

# Create a button with the microphone icon
st.write('<style>.microphone-button { background-color: #007bff; color: white; border: none; border-radius: 5px; padding: 10px; }</style>', unsafe_allow_html=True)

st.title(params.app_title)

if "messages" not in st.session_state:
    st.session_state.messages = []
    system_prompt = ""
    with open(params.sys_prompt_file, "r") as file:
        # system_prompt = file.read().replace('\n', '')
        system_prompt = file.read()
        st.session_state.messages.append({"role": "system", "content": system_prompt})
        # st.text_area(label="System Prompt", value=system_prompt, height=500)

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
    if play_audio:
        text_to_speech(full_response)

def speech_recognize_once_from_mic():
    # Set up the speech config and audio config
    st.write("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return f"{result.text}"
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized"
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return f"Speech Recognition canceled: {cancellation_details.reason}"
    else:
        return "Unknown error"

def text_to_speech(text):
    speech_config2 = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
    speech_config2.speech_synthesis_voice_name = params.neural_voice_name

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config2)

    # Synthesize the text to speech
    result = speech_synthesizer.speak_text_async(text).get()
    print('performing TTS for text', text)
    
    # Check the result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return "Text to speech conversion successful"
    else:
        return "Text to speech conversion failed"


if st.button('🎙️', key='mic_button'):
    recognition_result = speech_recognize_once_from_mic()
    st.chat_input( recognition_result)
    st.session_state.messages.append({"role": "user", "content": recognition_result})
    with st.chat_message("user"):
        st.markdown(recognition_result)
    with st.chat_message("assistant"):
        get_response_to_user_query(True)
   # st.chat_message(recognition_result)


if prompt := st.chat_input("Hello!!!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        get_response_to_user_query(False)





