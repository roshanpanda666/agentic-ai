import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from intents import training_data
from responses import responses
import requests
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# ===== Preprocessing =====
def preprocess(sentence):
    tokens = word_tokenize(sentence.lower())
    return {word: True for word in tokens if word.isalpha() and word not in stop_words}

# ===== Train Model =====
training_set = [(preprocess(text), tag) for text, tag in training_data]
classifier = nltk.NaiveBayesClassifier.train(training_set)

# ===== Wikipedia Scraper Function (Improved) =====
def scrape_wikipedia(query: str):
    # 🧹 Clean unnecessary question phrases
    for phrase in ["who is", "what is", "where is", "tell me about", "define"]:
        if query.lower().startswith(phrase):
            query = query.lower().replace(phrase, "").strip()

    formatted_search = query.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{formatted_search}"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            return f"⚠️ Wikipedia page not found for '{query}'"

        soup = BeautifulSoup(response.content, 'html.parser')

        # 🏷️ Get title
        title_tag = soup.find('h1')
        title = title_tag.text if title_tag else "No Title Found"

        # 📜 Get main content paragraph
        paragraph = ""
        for p in soup.find_all('p'):
            if p.text.strip() and not p.text.lower().startswith("coordinates") and len(p.text.strip()) > 40:
                paragraph = p.text.strip()
                break

        if paragraph:
            return f"📖 {title}: {paragraph[:500]}..."
        else:
            return f"📖 {title}: No suitable paragraph found."

    except Exception as e:
        return f"⚠️ Failed to scrape Wikipedia: {e}"

# ===== Get Response =====
def get_response(user_input):
    question_words = ["what", "why", "how", "when", "who", "where"]

    # If it's a question → scrape Wikipedia
    if any(user_input.lower().startswith(q) for q in question_words):
        return scrape_wikipedia(user_input)

    # Otherwise → classify intent
    features = preprocess(user_input)
    intent = classifier.classify(features)
    return random.choice(responses[intent])

# ===== Chat Loop =====
print("🤖 Rose: Hey bhai! Type 'quit' to exit.")
while True:
    user_inp = input("You: ")
    if user_inp.lower() in ["quit", "exit", "bye"]:
        print("Rose:", random.choice(responses["farewell"]))
        break
    print("Rose:", get_response(user_inp))

