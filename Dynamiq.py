import streamlit as st
from dynamiq.nodes.llms.openai import OpenAI
from dynamiq.connections import OpenAI as OpenAIConnection
from dynamiq import Workflow
from dynamiq.prompts import Prompt, Message

# Dictionary of languages and their corresponding Dynamiq prompts
languages = {
    "Spanish": "Translate the following text into Spanish: ",
    "German": "Translate the following text into German: ",
    "Japanese": "Translate the following text into Japanese: ",
    "French": "Translate the following text into French: "
}

# Function to set up and run the translation workflow
def translate_text(input_text, language, api_key):
    try:
        # Set up the prompt and connection
        prompt_template = languages[language] + input_text
        prompt = Prompt(messages=[Message(content=prompt_template, role="user")])
        llm = OpenAI(
            id="openai",
            connection=OpenAIConnection(api_key=api_key),
            model="gpt-4",
            temperature=0.3,
            max_tokens=1000,
            prompt=prompt
        )
        # Define and run the workflow
        workflow = Workflow()
        workflow.flow.add_nodes(llm)
        result = workflow.run(input_data={"text": input_text})

        # Log the entire output for inspection
        st.write("Debugging Result Output:", result.output)

        # Access and return the translation based on observed structure
        return result.output.get('openai', {}).get('output', {}).get('content', 'Translation not available')
        
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit user interface setup
st.title('Multilingual Translator')

# Add a text input for the API key
api_key = st.text_input("Enter your OpenAI API key:", type="password")

text_to_translate = st.text_area("Enter the English text you want to translate:", value='', max_chars=500)
selected_language = st.selectbox("Select the language to translate to:", options=list(languages.keys()))

# Button to perform translation
if st.button('Translate'):
    if not api_key:
        st.write("Please enter your OpenAI API key.")
    elif text_to_translate:
        translation = translate_text(text_to_translate, selected_language, api_key)
        st.write('Translation:', translation)
    else:
        st.write("Please enter some text to translate.")
