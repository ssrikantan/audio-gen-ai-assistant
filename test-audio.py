import streamlit as st

# Add FontAwesome CSS stylesheet
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)

# Create a button with the microphone icon
st.write('<style>.microphone-button { background-color: #007bff; color: white; border: none; border-radius: 5px; padding: 10px; }</style>', unsafe_allow_html=True)
if st.button('🎙️', key='mic_button'):
    st.write('Microphone button clicked!')
