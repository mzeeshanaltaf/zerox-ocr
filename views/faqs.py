import streamlit as st
from util import display_footer

# Page configuration options
page_title = "FAQs"
page_icon = "💬"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide", initial_sidebar_state="expanded")

st.title('FAQs')

expand_all = st.toggle("Expand all", value=False)


faq_data = {
        'What this Application is about?': '<p>This application takes a PDF document and extract text, tables, formulas from it with '
                                           'precision and deliver it in a clean and structured markdown format. '
                                           'This application makes use of Zerox OCR to perform lightning fast OCR.</p>',

        'Which AI models are supported?': """
        <p>This application supports the vision models of following providers:
            <ul>
                <li>OpenAI
                    <ul>
                        <li>gpt-4o-mini</li>
                        <li>gpt-4o</li>
                    </ul>
                </li>
                <li>Azure
                    <ul>
                        <li>gpt-4o</li>
                    </ul>
                </li>
                <li>Google
                    <ul>
                        <li>gemini-1.5-flash</li>
                        <li>gemini-1.5-pro</li>
                    </ul>
                </li>
                <li>Groq
                    <ul>
                        <li>llama-3.2-90b-vision-preview</li>
                    </ul>
                </li>
            </ul>
        </p>""",

        'Can I get the application source code?': '<p>Yes, Source code of this application is available at: <a href="https://github.com/mzeeshanaltaf/zerox-ocr/">GitHub</a></p>',

    }


# Display expandable boxes for each question-answer pair
for question, answer in faq_data.items():
    with st.expander(r"$\textbf{\textsf{" + question + r"}}$", expanded=expand_all):  # Use LaTeX for bold label
        st.markdown(f'<div style="text-align: justify;"> {answer} </div>', unsafe_allow_html=True)

display_footer()