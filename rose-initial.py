import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk import NaiveBayesClassifier
from scrapper import scrape_wikipedia
from intents import training_data
from responses import responses
from random import choice

# 📦 Download required NLTK data (only once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# 🧠 Preprocessing
def preprocess_with_tokens(sentence):
    tokens = word_tokenize(sentence.lower())
    clean_tokens = [word for word in tokens if word.isalnum()]
    features = {word: True for word in clean_tokens}
    return features, clean_tokens

# 🎯 Train classifier
train_set = [(preprocess_with_tokens(text)[0], label) for text, label in training_data]
classifier = NaiveBayesClassifier.train(train_set)

# 🚀 Streamlit UI
st.set_page_config(page_title="Smart Entity 🤖", layout="centered")
st.title("💬 Responsive Omnidirectional Smart Entity")

# Store chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat messages
st.markdown("### Chat History")
for sender, message in st.session_state.history:
    st.markdown(f"**{sender}:** {message}")

# Divider
st.markdown("---")

# Input section
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("Type your message:", key="user_message", label_visibility="collapsed")
with col2:
    send_button = st.button("Send")

# Handle sending
if send_button and user_input.strip() != "":
    # Classify intent
    features, clean_tokens = preprocess_with_tokens(user_input)
    label = classifier.classify(features)

    # Decide response
    if any(w in clean_tokens for w in ["who", "what", "where", "which"]):
        title, content = scrape_wikipedia(user_input)
        bot_reply = f"📚 **{title}**\n\n📝 {content}"
    else:
        bot_reply = choice(responses.get(label, ["Umm... I don't know that yet. 😅"]))

    # Save to chat history
    st.session_state.history.append(("👤 You", user_input))
    st.session_state.history.append(("🤖 Bot", bot_reply))

    # Clear input box
    st.session_state.pop("user_message", None)
    st.rerun()
