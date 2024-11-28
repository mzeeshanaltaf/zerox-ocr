import streamlit as st
from util import *
import asyncio
from datetime import datetime

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = None
if "azure_api_key" not in st.session_state:
    st.session_state.azure_api_key = None
    st.session_state.azure_ep = None
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = None
if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = None

if "markdown_zerox" not in st.session_state:
    st.session_state.markdown_zerox = None
    st.session_state.input_tokens = None
    st.session_state.output_tokens = None
    st.session_state.zerox_ocr_time = None

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

# Select the LLM model
model_name, api_key_status = model_selection()

# File uploader
st.subheader("Upload a PDF file:", divider='gray')
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"], label_visibility="collapsed", disabled=not api_key_status)

# If pdf file is not none then save the contents of the pdf file into temp file and preview the pdf
if uploaded_pdf is not None:
    # Save the contents of the uploaded file into temp file
    temp_file = "./temp.pdf"
    with open(temp_file, "wb") as file:
        file.write(uploaded_pdf.getvalue())

    # Reset the variables if new PDF is loaded.
    st.session_state.markdown_zerox = None
    st.session_state.input_tokens = None
    st.session_state.output_tokens = None
    st.session_state.zerox_ocr_time = None

    col1, col2 = st.columns([1, 1], vertical_alignment="top")

    # OCR with Zerox toolkit
    with (col1):
        st.subheader('OCR with Zerox:', divider='gray')
        run_ocr_zerox = st.button("Run OCR", type="primary", key="run_ocr_zerox", disabled=not uploaded_pdf)
        if run_ocr_zerox:
            with st.spinner('Processing ...'):
                st.session_state.markdown_zerox, st.session_state.zerox_ocr_time, st.session_state.input_tokens,\
                st.session_state.output_tokens = asyncio.run(perform_ocr_zerox(temp_file, model_name))

        # Display the markdown response and statistics of Zerox
        if st.session_state.markdown_zerox is not None:
            st.subheader('Statistics:', divider='gray')
            col3, col4, col5 = st.columns(3)
            col3.metric('Time Taken (sec)', f'{st.session_state.zerox_ocr_time:.2f}')
            col4.metric('Input Tokens', st.session_state.input_tokens)
            col5.metric('Output Tokens', st.session_state.output_tokens)
            st.subheader('Response:', divider='gray')

            with st.expander('Markdown Response', expanded=True, icon=':material/markdown:'):
                zerox_container = st.container(height=1000, key='zerox-container')
                zerox_container.markdown(st.session_state.markdown_zerox, unsafe_allow_html=True)

                # Create a unique file name based on current date & time for download
                file_name = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                st.download_button("Download", data=st.session_state.markdown_zerox,file_name=f"{file_name}_zerox.md",
                                   type='primary', icon=':material/markdown:', help='Download the Markdown Response')

    with col2:
        st.subheader('PDF Previewer:', divider='gray')
        with st.expander(':blue[***Preview PDF***]', expanded=False, icon=':material/preview:'):
            display_pdf_with_pdfjs(uploaded_pdf)

display_footer()
