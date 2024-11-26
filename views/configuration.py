import streamlit as st
from util import display_footer

st.title("Configuration")

expand_all = st.toggle("Expand all", value=False)

with st.expander('OpenAI API Key Configuration', icon=':material/key:', expanded=expand_all):
    with st.form('OpenAI API Key Configuration'):
        st.session_state.openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password",
                                                    value=st.session_state.openai_api_key,
                                                    help='Get API Key from: https://platform.openai.com/api-keys')
        submitted_openai = st.form_submit_button('Submit', type='primary')

with st.expander('Azure API Key Configuration', icon=':material/key:', expanded=expand_all):
    with st.form('Azure OpenAI Key Configuration'):
        st.session_state.azure_api_key = st.text_input("Enter your Azure API Key:", type="password",
                                                      value=st.session_state.azure_api_key)
        st.session_state.azure_ep = st.text_input("Enter your Azure End Point:", type="password",
                                                      value=st.session_state.azure_ep)
        submitted_azure = st.form_submit_button('Submit', type='primary')

with st.expander('Google Gemini API Key Configuration', icon=':material/key:', expanded=expand_all):
    with st.form('Google Gemini Keys Configuration'):
        st.session_state.gemini_api_key = st.text_input("Enter your Google Gemini API Key:", type="password",
                                                      value=st.session_state.gemini_api_key,
                                                      help='Get Google Gemini API Key from: Get API Key from: https://aistudio.google.com/app/apikey')
        submitted_gemini = st.form_submit_button('Submit', type='primary')

with st.expander('Groq API Key Configuration', icon=':material/key:', expanded=expand_all):
    with st.form('Groq API Key Configuration'):
        st.session_state.groq_api_key = st.text_input("Enter your Groq API Key:", type="password",
                                                      value=st.session_state.groq_api_key,
                                                      help='Get Groq API Key from: https://console.groq.com/keys')
        submitted_groq = st.form_submit_button('Submit', type='primary')

# Display footer
display_footer()