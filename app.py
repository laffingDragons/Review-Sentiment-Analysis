# importing necessary libraries
import openai
import spacy
import streamlit as st

# Set the API key securely (ensure this is done securely without hard-coding in production)
openai.api_key = "YOUR_API_KEY"

# Load Spacy NER model
nlp = spacy.load("en_core_web_sm")

# Define the function to analyze sentiment with word-level contributions using GPT
def analyze_sentiment_with_words(review, category):
    prompt = f"Analyze the sentiment of the following {category} review and provide sentiment contributions for each word (percentage):\n\nReview: {review}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a sentiment analysis assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    sentiment_analysis = response['choices'][0]['message']['content']
    return sentiment_analysis.strip()

# Function to perform Named Entity Recognition (NER)
def extract_entities(review):
    doc = nlp(review)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Streamlit app
st.title("Sentiment Analysis and Named Entity Recognition (NER) App")

# Input for category and review
category = st.selectbox("Enter the category of the review (e.g., Food, Product, Place, Other):", ["Food", "Product", "Place", "Other"])
review = st.text_area("Enter your review:")

# Analyze and display results
if st.button("Analyze"):
    if review:
        st.write("### Performing Sentiment Analysis...")
        sentiment_with_contributions = analyze_sentiment_with_words(review, category)
        st.write("Sentiment Analysis with Word-Level Contributions:")
        st.text(sentiment_with_contributions)

        st.write("### Performing Named Entity Recognition (NER)...")
        entities = extract_entities(review)
        st.write("Named Entities in the Review:")
        st.write(entities)
    else:
        st.warning("Please enter a valid review.")
