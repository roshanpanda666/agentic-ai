import nltk
from voice_engine import speak
from nltk.tokenize import word_tokenize
from nltk import NaiveBayesClassifier
from scrapper import scrape_wikipedia
from intents import training_data
from responses import responses  # 💬 Modular response data

# 📦 Download required NLTK data
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

# 🗣️ Chat loop
while True:
    user_input = input("👤 You: ")

    # 🧠 Classify intent
    features, clean_tokens = preprocess_with_tokens(user_input)
    label = classifier.classify(features)

    print("📌 Detected intent:", label)
    print("🔍 Clean tokens:", clean_tokens)

    # 🌐 Wiki question?
    if any(w in clean_tokens for w in ["who", "what", "where", "which"]):
        title, content = scrape_wikipedia(user_input)
        print("📚", title)
        print("📝", content)
        speak(title)
        speak(content)
    
    else:
        # 💬 Respond with style
        from random import choice
        reply = choice(responses.get(label, ["Umm... I don't know that yet. 😅"]))
        print("🤖 Bot:", reply)
        speak(reply)
