import requests
from bs4 import BeautifulSoup
from voice_engine import speak

#  Ask user for input
speak("type something to search")
search = input("🔍 Enter a topic to search on Wikipedia: ").strip().lower()

#  Clean unnecessary question phrases
for phrase in ["who is", "what is","where is", "tell me about", "define"]:
    if search.startswith(phrase):
        search = search.replace(phrase, "").strip()

#  Format search term for Wikipedia URL
formatted_search = search.replace(" ", "_")
url = f"https://en.wikipedia.org/wiki/{formatted_search}"

#  Send request
response = requests.get(url)

#  Parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')

#  Get Title
title_tag = soup.find('h1')
title = title_tag.text if title_tag else "No Title Found"

#  Find first real paragraph (not notices)
paragraph = ""
for p in soup.find_all('p'):
    if p.text.strip() and not p.text.lower().startswith("coordinates") and len(p.text.strip()) > 40:
        paragraph = p.text.strip()
        break

#  Show results
print(f"\n🔥 Title: {title}\n")
speak(title)
print(f"📜 Intro Paragraph:\n{paragraph if paragraph else 'No suitable paragraph found'}")
speak(paragraph if paragraph else 'No suitable paragraph found')