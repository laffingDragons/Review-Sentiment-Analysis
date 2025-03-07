import streamlit as st
import openai
import spacy
from spacy.cli import download
import streamlit_js_eval as js

# Function to get OpenAI key from local storage
def get_openai_key():
    return js.eval_js("localStorage.getItem('openai_api_key')")

# Function to set OpenAI key in local storage
def set_openai_key(api_key):
    js.eval_js(f"localStorage.setItem('openai_api_key', '{api_key}')")

# Ask user for OpenAI API key if not found in local storage
st.sidebar.header("🔑 OpenAI API Key Configuration")
st.sidebar.write("Enter your OpenAI API key below. It will be saved in local storage for future use.")

def configure_api_key():
    api_key = get_openai_key()
    if not api_key:
        api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")
        if st.sidebar.button("Save API Key"):
            set_openai_key(api_key)
            st.sidebar.success("API Key saved! Refresh the page to apply changes.")
    else:
        st.sidebar.success("API Key loaded from local storage.")
        if st.sidebar.button("Edit API Key"):
            api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")
            if st.sidebar.button("Update API Key"):
                set_openai_key(api_key)
                st.sidebar.success("API Key updated! Refresh the page to apply changes.")
    return api_key

# Load API Key
openai.api_key = configure_api_key()

# Load or download SpaCy NER model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Customizing Streamlit UI
st.set_page_config(page_title="Sentiment & NER Analyzer", page_icon="🌱", layout="centered")
st.markdown(
    """
    <style>
        .css-18e3th9 { background-color: #d5e8d4; }
        .stButton button { background-color: #4CAF50; color: white; border-radius: 10px; box-shadow: 0 0 10px #8bc34a; }
        .stTextInput input { background-color: #e8f5e9; border: 2px solid #a5d6a7; border-radius: 8px; }
        .title-text { font-family: 'Cursive', sans-serif; font-size: 24px; color: #2e7d32; }
        .stApp { background-color: #d5e8d4; }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the app
st.title("Sentiment & NER Analyzer")
st.markdown("<div class='title-text'>Analyze your text with sentiment insights and named entity recognition.<br/></div>", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to analyze sentiment
def analyze_sentiment_with_words(review, category):
    prompt = f"Analyze the sentiment of the following {category} review and provide sentiment contributions for each word (percentage):\n\nReview: {review}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a sentiment analysis assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Function to perform Named Entity Recognition (NER)
def extract_entities(review):
    doc = nlp(review)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    icon = "🌿" if role == "user" else "✨"
    with st.chat_message(role):
        st.markdown(f"{icon} {content}")

# Collect user input
category = st.selectbox("Select the category of the review (e.g., Food, Product, Place, Other):", ["Food", "Product", "Place", "Other"])
user_input = st.text_area("Enter your review:")

if st.button("Analyze"):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"🌿 {user_input}")

        # Perform sentiment analysis
        assistant_response = analyze_sentiment_with_words(user_input, category)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(f"✨ **Sentiment Analysis Result:**\n{assistant_response}")

        # Perform and display NER results
        entities = extract_entities(user_input)
        st.markdown("### Named Entities in the Review:")
        st.write(entities if entities else "No named entities found.")
    else:
        st.warning("Please enter a valid review.")
