# Sentiment Analysis and Named Entity Recognition (NER) App

## 🚀 About This Project
This is a **Streamlit** application that performs:
- **Sentiment Analysis**: Uses OpenAI's GPT-4 to analyze sentiment with word-level contributions.
- **Named Entity Recognition (NER)**: Uses **SpaCy** to extract named entities (e.g., names, locations, products) from the text.

---

## 🛠️ Features
- ✅ **Sentiment Analysis** using GPT-4 with word-level sentiment breakdown.
- ✅ **NER Extraction** using **SpaCy** (`en_core_web_sm` model).
- ✅ **Interactive UI** powered by **Streamlit**.

---

## 📌 Installation & Setup

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-username/sentiment-ner-app.git
cd sentiment-ner-app
```

### 2️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

### 3️⃣ **Download the SpaCy Model**
```sh
python -m spacy download en_core_web_sm
```

### 4️⃣ **Run the Application**
```sh
streamlit run app.py
```

---

## 🔑 OpenAI API Key Setup
1. Open `app.py` and replace **`YOUR_API_KEY`** with your actual OpenAI API Key.
2. For security, **never hardcode API keys in production**. Use environment variables instead.

Example:
```sh
export OPENAI_API_KEY="your-key-here"
```

---

## 📦 Dependencies
- **Streamlit** (for UI)
- **OpenAI API** (for Sentiment Analysis)
- **SpaCy** (for Named Entity Recognition)

Install dependencies manually with:
```sh
pip install streamlit openai spacy
python -m spacy download en_core_web_sm
```

---

## 📜 License
This project is **MIT Licensed**. You are free to use and modify it.

---

### 📧 Contact
For any issues, reach out via [GitHub Issues](https://github.com/your-username/sentiment-ner-app/issues).

---
