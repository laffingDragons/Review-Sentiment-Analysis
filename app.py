import streamlit as st
import openai
import spacy
from spacy.cli import download

# Initialize OpenAI client using Streamlit's secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load or download SpaCy NER model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Customizing Streamlit with green theme and spiritual touches
st.set_page_config(page_title="Sentiment & NER Analyzer", page_icon="🌱", layout="centered")
st.markdown(
    """
    <style>
        .css-18e3th9 {
            background-color: #d5e8d4;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            box-shadow: 0 0 10px #8bc34a;
        }
        .stTextInput input {
            background-color: #e8f5e9;
            border: 2px solid #a5d6a7;
            border-radius: 8px;
        }
        .title-text {
            font-family: 'Cursive', sans-serif;
            font-size: 24px;
            color: #2e7d32;
        }
        .stApp {
            background-color: #d5e8d4;
        }
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

# Function to analyze sentiment with word-level contributions using GPT
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
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Display chat history with subtle icons
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    icon = "🌿" if role == "user" else "✨"
    with st.chat_message(role):
        st.markdown(f"{icon} {content}")

# Collect user input for category and review
category = st.selectbox("Select the category of the review (e.g., Food, Product, Place, Other):", ["Food", "Product", "Place", "Other"])
user_input = st.text_area("Enter your review:")

# Process and display response if there's input
if st.button("Analyze"):
    if user_input:
        # Append user's input
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
        if entities:
            st.write(entities)
        else:
            st.write("No named entities found.")
    else:
        st.warning("Please enter a valid review.")
