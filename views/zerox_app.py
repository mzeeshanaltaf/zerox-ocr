import streamlit as st
from util import *
import os

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = None
if "azure_api_key" not in st.session_state:
    st.session_state.azure_api_key = None
    st.session_state.azure_ep = None
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = None
if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = None

page_title = "DocuVision 📄🔍✨"
page_icon = "📄"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")

st.title(page_title)
st.write(':blue[***Transforming PDFs into Markdown Magic! 🌟📄***]')
st.write("""
DocuVision takes your PDFs and performs lightning-fast OCR 🖹✨, extracting text with precision and delivering it 
in clean, structured Markdown format🖋️💡. Whether it’s scanned documents or complex layouts, this app simplifies 
your workflow, making document management effortless and accessible.🚀
""")
st.info("This application is powered by [Zerox OCR](https://github.com/getomni-ai/zerox). "
        "Popular toolkit for document OCR'ing.", icon=':material/info:')

st.subheader('Select the LLM:')
model_provider = st.selectbox('Choose the LLM Provider:', ('OpenAI', 'Azure', 'Google', 'Groq'))

model = '' # Variable to keep track of selected model
api_key_status = False # Variable to disable PDF uploading if key is none

if model_provider == 'OpenAI':
    if st.session_state.openai_api_key is None:
        st.warning('API Key not set. Configure the OpenAI API key from Configuration page.👈', icon=':material/warning:')
    else:
        model = st.pills('Select the Vision Model:', ['gpt-4o-mini', 'gpt-4o'], selection_mode='single', default='gpt-4o-mini')
        os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key
        api_key_status = True

if model_provider == 'Azure':
    if st.session_state.azure_api_key is None or st.session_state.azure_ep is None:
        st.warning('API or Endpoint is not configured. Configure the Azure API or Endpoint from Configuration page.👈', icon=':material/warning:')
    else:
        model = st.pills('Select the Vision Model:', ['gpt-4o'], selection_mode='single', default='gpt-4o')
        os.environ["AZURE_API_KEY"] = st.session_state.azure_api_key
        os.environ["AZURE_API_BASE"] = st.session_state.azure_ep
        os.environ["AZURE_API_VERSION"] = "2023-05-15"
        api_key_status = True

if model_provider == 'Google':
    if st.session_state.gemini_api_key is None:
        st.warning('API Key not set. Configure the Google Gemini API key from Configuration page.👈', icon=':material/warning:')
    else:
        model = st.pills('Select the Vision Model:', ['gemini-1.5-flash', 'gemini-1.5-pro'], selection_mode='single', default='gemini-1.5-flash')
        os.environ['GEMINI_API_KEY'] = st.session_state.gemini_api_key
        api_key_status = True

if model_provider == 'Groq':
    if st.session_state.groq_api_key is None:
        st.warning('API Key not set. Configure the Groq API key from Configuration page.👈', icon=':material/warning:')
    else:
        model = st.pills('Select the Vision Model:', ['llama-3.2-90b-vision-preview'], selection_mode='single', default='llama-3.2-90b-vision-preview')
        os.environ['GROQ_API_KEY'] = st.session_state.groq_api_key
        api_key_status = True

# File uploader
st.subheader("Upload a PDF file:", divider='gray')
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"], label_visibility="collapsed", disabled=not api_key_status)

# If pdf file is not none then save the contents of the pdf file into temp file and preview the pdf
if uploaded_pdf is not None:
    # Save the contents of the uploaded file into temp file
    temp_file = "./temp.pdf"
    with open(temp_file, "wb") as file:
        file.write(uploaded_pdf.getvalue())

    st.subheader('PDF Previewer:', divider='gray')
    with st.expander(':blue[***Preview PDF***]', expanded=False, icon=':material/preview:'):
        display_pdf(uploaded_pdf)

display_footer()