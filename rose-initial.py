import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk import NaiveBayesClassifier
from random import choice
import requests
from bs4 import BeautifulSoup
import urllib.parse

import nltk

def download_nltk_data():
    resources = ['punkt', 'stopwords', 'wordnet', 'omw-1.4']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            nltk.download(resource)

download_nltk_data()

# ========================
# 🌐 Wikipedia Scraper
# ========================
def scrape_wikipedia(query: str):
    for phrase in ["who is", "what is", "where is", "tell me about", "define"]:
        if query.lower().startswith(phrase):
            query = query.lower().replace(phrase, "").strip()

    formatted_search = query.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{formatted_search}"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.content, 'html.parser')

        title_tag = soup.find('h1')
        title = title_tag.text if title_tag else "No Title Found"

        paragraph = ""
        for p in soup.find_all('p'):
            if p.text.strip() and not p.text.lower().startswith("coordinates") and len(p.text.strip()) > 40:
                paragraph = p.text.strip()
                break

        return title, paragraph if paragraph else "No suitable paragraph found"
    except Exception as e:
        return "Error", f"⚠️ Failed to scrape Wikipedia: {e}"

# ========================
# 🎯 Intents Data
# ========================
training_data = [
    # 👋 Greetings
    ("hello there", "greeting"), ("hi bro", "greeting"), ("hey dude", "greeting"),
    ("hi legend", "greeting"), ("what's up", "greeting"), ("good morning", "greeting"),
    ("good evening", "greeting"), ("how are you?", "greeting"), ("yo", "greeting"), ("sup", "greeting"),

    # ❓ Questions
    ("what is NLP?", "question"), ("tell me about GPT", "question"),
    ("explain artificial intelligence", "question"), ("how does machine learning work", "question"),
    ("what is deep learning", "question"), ("why is AI important", "question"),
    ("how do you process language", "question"), ("what is a neural network", "question"),

    # 👋 Farewells
    ("bye for now", "farewell"), ("see you", "farewell"), ("catch you later", "farewell"),
    ("goodbye", "farewell"), ("take care", "farewell"), ("talk soon", "farewell"),
    ("i’m out", "farewell"), ("see ya", "farewell"),

    # 🤖 Asking about the bot
    ("who are you", "askingme"), ("what are you", "askingme"), ("are you real", "askingme"),
    ("who made you", "askingme"), ("what do you do", "askingme"), ("yourself", "askingme"),
    ("you", "askingme"), ("your", "askingme"), ("tell me about yourself", "askingme"),

    # 🙏 Thanks
    ("thanks", "thanks"), ("thank you", "thanks"), ("i appreciate it", "thanks"),
    ("grateful", "thanks"), ("many thanks", "thanks"),

    # 😂 Jokes
    ("tell me a joke", "joke"), ("make me laugh", "joke"), ("say something funny", "joke"),
    ("do you know any jokes", "joke"), ("crack a joke", "joke"),

    # 😍 Compliments
    ("you are awesome", "compliment"), ("you’re cool", "compliment"), ("nice work", "compliment"),
    ("great job", "compliment"), ("you’re smart", "compliment"), ("you’re doing amazing", "compliment"),

    # 🚀 Motivation
    ("motivate me", "motivation"), ("inspire me", "motivation"),
    ("say something powerful", "motivation"), ("give me a motivational quote", "motivation"),
    ("i need motivation", "motivation"), ("i’m feeling low", "motivation"),

    # 🌦️ Weather
    ("what's the weather", "weather"), ("is it raining", "weather"),
    ("do I need an umbrella", "weather"), ("what's the temperature", "weather"),
    ("is it sunny today", "weather"),

    # 😅 Apology
    ("sorry", "apology"), ("my bad", "apology"), ("didn't mean to", "apology"),
    ("forgive me", "apology"), ("oops", "apology"),

    # 🎲 Fun Facts
    ("tell me a fun fact", "funfact"), ("say something interesting", "funfact"),
    ("give me a random fact", "funfact"), ("do you know something cool", "funfact"),
    ("share a fun fact", "funfact"),

    # 🛠️ Commands
    ("turn on the lights", "command"), ("play some music", "command"),
    ("start the engine", "command"), ("shut it down", "command"),
    ("execute the protocol", "command"),

    # 💀 Gibberish / Unknowns
    ("asdkjhasd", "gibberish"), ("uhh wut", "gibberish"), ("?????", "gibberish"),
    ("yo88$$", "gibberish"), ("alksjdhf", "gibberish"),

    # 🧘‍♂️ Philosophy
    ("what is the meaning of life", "philosophy"), ("why are we here", "philosophy"),
    ("is reality real", "philosophy"), ("what is consciousness", "philosophy"),
    ("what is the purpose of existence", "philosophy"),

    # 🍕 Food
    ("i'm hungry", "food"), ("suggest me food", "food"),
    ("what should i eat", "food"), ("i want pizza", "food"),

    # 💻 Tech
    ("tell me about python", "tech"), ("best programming language", "tech"),
    ("what is ai", "tech"), ("how to learn coding", "tech"),

    # 💘 Love / Flirt
    ("i like you", "love"), ("will you marry me", "love"),
    ("you are cute", "love"), ("i love you", "love"),

    # 🎮 Gaming
    ("let's play", "gaming"), ("suggest me a game", "gaming"),
    ("i like fortnite", "gaming"), ("best game ever", "gaming"),

    # 📚 Study help
    ("help me study", "study"), ("explain physics", "study"),
    ("math problem", "study"), ("teach me something", "study"),

    # 🏋️ Health & fitness
    ("workout tips", "fitness"), ("how to lose weight", "fitness"),
    ("healthy food", "fitness"), ("gym motivation", "fitness"),

    # 🔥 Sarcasm / roast
    ("you are dumb", "roast"), ("roast me", "roast"),
    ("make fun of me", "roast"), ("say something savage", "roast"),

    # 🐶 Pet talk
    ("i have a dog", "pets"), ("tell me about cats", "pets"),
    ("i love my pet", "pets"), ("dog facts", "pets"),

    # 🎬 YouTube Play
    ("open youtube and play despacito", "playyoutube"),
    ("play shape of you on youtube", "playyoutube"),
    ("youtube play kesariya", "playyoutube"),
    ("open youtube and search lo-fi music", "playyoutube"),
]

# ========================
# 💬 Responses
# ========================
responses = {
    "greeting": ["Heyy!", "What's up bhai!", "Hello legend! 😎"],
    "question": ["Let's learn together!", "That's a deep one... 🤔", "Here’s what I know..."],
    "farewell": ["Bye bro!", "Catch you later!", "Peace out! ✌️"],
    "askingme": ["I'm an LLM!", "Just an AI vibin’ 🤖", "Call me RoshanGPT 😎"],
    "thanks": ["Anytime! 🙌", "Glad to help!", "You’re welcome!"],
    "joke": ["Why don’t skeletons fight each other? They don’t have the guts! 😂", 
             "I told my computer I needed a break, and it froze. 🥶"],
    "compliment": ["Thanks, legend! 😎", "You’re the real MVP! 🏆", "Appreciate it! ❤️"],
    "motivation": ["You got this! 🚀", "Push through! Your future self will thank you. 💪", "Keep grinding, king 👑"],
    "weather": ["Looks sunny ☀️", "Might need an umbrella ☔", "Check the skies, champ 🌤️"],
    "apology": ["No worries, bro ✌️", "It’s all good 🙏", "Forgiven!"],
    "funfact": ["Sharks existed before trees! 🌳🦈", "Bananas are berries, but strawberries aren’t 🍌🍓"],
    "command": ["On it! 🚀", "Executing order 🛠️", "Done ✅"],
    "gibberish": ["Umm... I don’t speak alien 👽", "Try that again?"],
    "philosophy": ["The meaning of life? To give life meaning. 🌌", "We are stardust contemplating the stars ✨"],
    "food": ["🍕 Pizza is always the answer!", "How about some momos? 🥟", "Biryani never disappoints 🍲", "Ice cream solves 99% of problems 🍦"],
    "tech": ["Python > all. 🐍", "Tech is moving fast—stay updated, legend ⚡", "AI is like coffee for machines ☕🤖", "Start with the basics, then break the internet 🔥"],
    "love": ["Aww, stop it! You’re making my circuits blush 💖", "Sorry, I’m married to the cloud ☁️😂", "Love you too, in binary: 01001100 💕", "Flirt level: legendary 😏"],
    "gaming": ["🎮 Gaming keeps the soul alive.", "Minecraft is life, fight me 🪓", "How about some late-night Valorant?", "Winner winner chicken dinner 🍗"],
    "study": ["Knowledge is your superpower ⚡📚", "Let’s make studying fun 🔥", "Start with small goals, and crush them 💪", "Brains > Brawn… but both is best 😎"],
    "fitness": ["One more rep, bro! 🏋️", "Abs are built in the kitchen, not just the gym 🍎", "Consistency is the secret ingredient 🔑", "No pain, no gain 🚀"],
    "roast": ["I’d agree with you, but then we’d both be wrong 😏", "Your WiFi signal is stronger than your arguments 📶", "I’ve met toasters smarter than you 😂", "Bless your heart… it’s working overtime 💀"],
    "pets": ["Dogs are pure souls 🐶❤️", "Cats: The true rulers of Earth 🐱👑", "Your pet deserves extra treats today 🍖", "Fun fact: A dog’s nose print is unique 🐾"],
    "playyoutube": ["Opening YouTube for you... 🎵", "Here you go, enjoy! 🎬"]
}

# ========================
# 🧠 Preprocessing
# ========================
def preprocess_with_tokens(sentence):
    tokens = word_tokenize(sentence.lower())
    clean_tokens = [word for word in tokens if word.isalnum()]
    features = {word: True for word in clean_tokens}
    return features, clean_tokens

# ========================
# 🤖 Train classifier
# ========================
train_set = [(preprocess_with_tokens(text)[0], label) for text, label in training_data]
classifier = NaiveBayesClassifier.train(train_set)

# ========================
# 🚀 Streamlit UI
# ========================
st.set_page_config(page_title="Smart Entity 🤖", layout="centered")
st.title("💬 Responsive Omnidirectional Smart Entity")

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("### Chat History")
for sender, message in st.session_state.history:
    st.markdown(f"**{sender}:** {message}")

st.markdown("---")
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("Type your message:", key="user_message", label_visibility="collapsed")
with col2:
    send_button = st.button("Send")

if send_button and user_input.strip() != "":
    features, clean_tokens = preprocess_with_tokens(user_input)
    label = classifier.classify(features)

    if label == "playyoutube":
        # Extract query text for YouTube search
        # Remove phrases to isolate song/video title
        lowered = user_input.lower()
        for phrase in ["open youtube and play", "play", "on youtube", "youtube play", "open youtube and search"]:
            lowered = lowered.replace(phrase, "")
        song_query = lowered.strip()
        if not song_query:
            song_query = "latest music"
        search_query = urllib.parse.quote(song_query)
        youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
        bot_reply = f"🎬 [Click here to watch on YouTube]({youtube_url})"
    
    elif any(w in clean_tokens for w in ["who", "what", "where", "which"]):
        title, content = scrape_wikipedia(user_input)
        bot_reply = f"📚 **{title}**\n\n📝 {content}"
    else:
        bot_reply = choice(responses.get(label, ["Umm... I don't know that yet. 😅"]))

    st.session_state.history.append(("👤 You", user_input))
    st.session_state.history.append(("🤖 Bot", bot_reply))

    st.session_state.pop("user_message", None)
    st.rerun()
