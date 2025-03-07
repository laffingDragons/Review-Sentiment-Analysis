import streamlit as st

# Customizing Streamlit UI - MUST BE FIRST!
st.set_page_config(page_title="Sentiment & NER Analyzer", page_icon="🌱", layout="centered")

import spacy
from spacy.cli import download
from openai import OpenAI

# Load or download SpaCy NER model
@st.cache_resource
def load_nlp_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_nlp_model()
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

# Sidebar for API key configuration
st.sidebar.header("🔑 OpenAI API Key Configuration")
st.sidebar.write("Enter your OpenAI API key below.")

# Get API key from session state or user input
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password", value=st.session_state.openai_api_key)

if api_key:
    st.session_state.openai_api_key = api_key
    st.sidebar.success("API Key set!")
else:
    st.sidebar.warning("Please enter an API key to use the sentiment analysis feature.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to analyze sentiment
def analyze_sentiment_with_words(review, category):
    if not st.session_state.openai_api_key:
        return "Please enter an OpenAI API key to use sentiment analysis."
    
    client = OpenAI(api_key=st.session_state.openai_api_key)
    
    prompt = f"Analyze the sentiment of the following {category} review and provide sentiment contributions for each word (percentage):\n\nReview: {review}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sentiment analysis assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

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
        with st.spinner("Analyzing sentiment..."):
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
