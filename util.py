import streamlit as st
import base64
from pyzerox import zerox
import os
import pdfplumber
import streamlit.components.v1 as components

# Function for selecting LLM Model
def model_selection():
    st.subheader('Select the LLM:')
    model_provider = st.selectbox('Choose the LLM Provider:', ('OpenAI', 'Azure', 'Google', 'Groq'))

    model_name = ''  # Variable to keep track of selected model
    api_key_status = False  # Variable to disable PDF uploading if key is none

    if model_provider == 'OpenAI':
        if st.session_state.openai_api_key is None:
            st.warning('API Key not set. Configure the OpenAI API key from Configuration page.👈',
                       icon=':material/warning:')
        else:
            model = st.pills('Select the Vision Model:', ['gpt-4o-mini', 'gpt-4o'], selection_mode='single',
                             default='gpt-4o-mini')
            os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key
            api_key_status = True
            model_name = model

    if model_provider == 'Azure':
        if st.session_state.azure_api_key is None or st.session_state.azure_ep is None:
            st.warning(
                'API or Endpoint is not configured. Configure the Azure API or Endpoint from Configuration page.👈',
                icon=':material/warning:')
        else:
            model = st.pills('Select the Vision Model:', ['gpt-4o'], selection_mode='single', default='gpt-4o')
            os.environ["AZURE_API_KEY"] = st.session_state.azure_api_key
            os.environ["AZURE_API_BASE"] = st.session_state.azure_ep
            os.environ["AZURE_API_VERSION"] = "2023-05-15"
            api_key_status = True
            model_name = f'azure/{model}'

    if model_provider == 'Google':
        if st.session_state.gemini_api_key is None:
            st.warning('API Key not set. Configure the Google Gemini API key from Configuration page.👈',
                       icon=':material/warning:')
        else:
            model = st.pills('Select the Vision Model:', ['gemini-1.5-flash', 'gemini-1.5-pro'],
                             selection_mode='single', default='gemini-1.5-flash')
            os.environ['GEMINI_API_KEY'] = st.session_state.gemini_api_key
            api_key_status = True
            model_name = f'gemini/{model}'

    if model_provider == 'Groq':
        if st.session_state.groq_api_key is None:
            st.warning('API Key not set. Configure the Groq API key from Configuration page.👈',
                       icon=':material/warning:')
        else:
            model = st.pills('Select the Vision Model:', ['llama-3.2-90b-vision-preview'], selection_mode='single',
                             default='llama-3.2-90b-vision-preview')
            os.environ['GROQ_API_KEY'] = st.session_state.groq_api_key
            api_key_status = True
            model_name = f'groq/{model}'

    return model_name, api_key_status

# Function to display the PDF of a given file
def display_pdf(file):
    # Reading the uploaded file
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0" width="100%" height="700" type="application/pdf"></iframe>'

    # Displaying the PDF
    st.markdown(pdf_display, unsafe_allow_html=True)

# Function to perform OCR using zerox ocr engine
async def perform_ocr_zerox(source, model):
    markdown_format = ''
    kwargs = {}  # Placeholder for additional model kwargs which might be required for some models
    custom_system_prompt = None  # System prompt to use for the vision model
    select_pages = None  ## None for all, but could be int or list(int) page numbers (1 indexed)

    result = await zerox(file_path=source, model=model,
                         custom_system_prompt=custom_system_prompt, select_pages=select_pages, **kwargs)

    # Get the content of all the pages
    for i in range(len(result.pages)):
        markdown_format += result.pages[i].content

    completion_time = result.completion_time / 1000

    return markdown_format, completion_time, result.input_tokens, result.output_tokens


def display_footer():
    footer = """
    <style>
    /* Ensures the footer stays at the bottom of the sidebar */
    [data-testid="stSidebar"] > div: nth-child(3) {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
    }

    .footer {
        color: grey;
        font-size: 15px;
        text-align: center;
        background-color: transparent;
    }
    </style>
    <div class="footer">
    Made with ❤️ by <a href="mailto:zeeshan.altaf@92labs.ai">Zeeshan</a>.
    </div>
    """
    st.sidebar.markdown(footer, unsafe_allow_html=True)


def read_pdf_pages(file_path):
    # Open the PDF file
    with pdfplumber.open(file_path) as pdf:
        total_pages = len(pdf.pages)
    return total_pages



# Function for selecting LLM Model
def model_selection():
    st.subheader('Select the LLM:')
    model_provider = st.selectbox('Choose the LLM Provider:', ('OpenAI', 'Azure', 'Google', 'Groq'))

    model_name = ''  # Variable to keep track of selected model
    api_key_status = False  # Variable to disable PDF uploading if key is none

    if model_provider == 'OpenAI':
        if st.session_state.openai_api_key is None:
            st.warning('API Key not set. Configure the OpenAI API key from Configuration page.👈',
                       icon=':material/warning:')
        else:
            model = st.pills('Select the Vision Model:', ['gpt-4o-mini', 'gpt-4o'], selection_mode='single',
                             default='gpt-4o-mini')
            os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key
            api_key_status = True
            model_name = model

    if model_provider == 'Azure':
        if st.session_state.azure_api_key is None or st.session_state.azure_ep is None:
            st.warning(
                'API or Endpoint is not configured. Configure the Azure API or Endpoint from Configuration page.👈',
                icon=':material/warning:')
        else:
            model = st.pills('Select the Vision Model:', ['gpt-4o'], selection_mode='single', default='gpt-4o')
            os.environ["AZURE_API_KEY"] = st.session_state.azure_api_key
            os.environ["AZURE_API_BASE"] = st.session_state.azure_ep
            os.environ["AZURE_API_VERSION"] = "2023-05-15"
            api_key_status = True
            model_name = f'azure/{model}'

    if model_provider == 'Google':
        if st.session_state.gemini_api_key is None:
            st.warning('API Key not set. Configure the Google Gemini API key from Configuration page.👈',
                       icon=':material/warning:')
        else:
            model = st.pills('Select the Vision Model:', ['gemini-1.5-flash', 'gemini-1.5-pro'],
                             selection_mode='single', default='gemini-1.5-flash')
            os.environ['GEMINI_API_KEY'] = st.session_state.gemini_api_key
            api_key_status = True
            model_name = f'gemini/{model}'

    if model_provider == 'Groq':
        if st.session_state.groq_api_key is None:
            st.warning('API Key not set. Configure the Groq API key from Configuration page.👈',
                       icon=':material/warning:')
        else:
            model = st.pills('Select the Vision Model:', ['llama-3.2-90b-vision-preview'], selection_mode='single',
                             default='llama-3.2-90b-vision-preview')
            os.environ['GROQ_API_KEY'] = st.session_state.groq_api_key
            api_key_status = True
            model_name = f'groq/{model}'

    return model_name, api_key_status

# Function to display the PDF of a given file
def display_pdf(file):
    # Reading the uploaded file
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0" width="100%" height="700" type="application/pdf"></iframe>'

    # Displaying the PDF
    st.markdown(pdf_display, unsafe_allow_html=True)

# Function to perform OCR using zerox ocr engine
async def perform_ocr_zerox(source, model):
    markdown_format = ''
    kwargs = {}  # Placeholder for additional model kwargs which might be required for some models
    custom_system_prompt = None  # System prompt to use for the vision model
    select_pages = None  ## None for all, but could be int or list(int) page numbers (1 indexed)

    pages = read_pdf_pages(source)
    st.write(pages)
    return None, None, None, None

    # result = await zerox(file_path=source, model=model,
    #                      custom_system_prompt=custom_system_prompt, select_pages=select_pages, **kwargs)

    # Get the content of all the pages
    # for i in range(len(result.pages)):
    #     markdown_format += result.pages[i].content

    # completion_time = result.completion_time / 1000

    # return markdown_format, completion_time, result.input_tokens, result.output_tokens


def display_footer():
    footer = """
    <style>
    /* Ensures the footer stays at the bottom of the sidebar */
    [data-testid="stSidebar"] > div: nth-child(3) {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
    }

    .footer {
        color: grey;
        font-size: 15px;
        text-align: center;
        background-color: transparent;
    }
    </style>
    <div class="footer">
    Made with ❤️ by <a href="mailto:zeeshan.altaf@92labs.ai">Zeeshan</a>.
    </div>
    """
    st.sidebar.markdown(footer, unsafe_allow_html=True)


def read_pdf_pages(file_path):
    # Open the PDF file
    with pdfplumber.open(file_path) as pdf:
        total_pages = len(pdf.pages)
    return total_pages

def display_pdf_with_pdfjs(file):
    # Convert file to base64
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')

    # Define the HTML structure for PDF.js
    pdf_js_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.6.347/pdf.js"></script>
        <style>
            #canvas-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 20px;
                width: 100%;
                height: auto;
                overflow: auto;
            }}
            .pdf-page {{
                margin: auto;
                border: 1px solid #ccc;
                display: block;
            }}
        </style>
    </head>
    <body>
        <div id="canvas-container"></div>   
        <script>
            // Initialize PDF.js
            const pdfData = atob("{base64_pdf}");
            const loadingTask = pdfjsLib.getDocument({{data: pdfData}});
            const canvasContainer = document.getElementById('canvas-container');

            loadingTask.promise.then(pdf => {{
                for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {{
                    pdf.getPage(pageNum).then(page => {{
                        const scale = 1.25;
                        const viewport = page.getViewport({{scale: scale}});

                        // Create a new canvas for each page
                        const canvas = document.createElement('canvas');
                        canvas.className = 'pdf-page';
                        canvasContainer.appendChild(canvas);

                        // Prepare canvas context
                        const context = canvas.getContext('2d');
                        canvas.height = viewport.height;
                        canvas.width = viewport.width;

                        // Render PDF page into canvas context
                        const renderContext = {{
                            canvasContext: context,
                            viewport: viewport
                        }};
                        page.render(renderContext).promise.then(() => {{
                        }});
                    }});
                }}
            }}).catch(error => {{
                console.error('Error loading PDF:', error);
            }});
        </script>
    </body>
    </html>
    """

    # Embed the HTML into Streamlit
    components.html(pdf_js_code, height=800, scrolling=True)
    
