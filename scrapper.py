import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(query: str):
    # 🧹 Clean unnecessary question phrases
    for phrase in ["who is", "what is", "where is", "tell me about", "define"]:
        if query.lower().startswith(phrase):
            query = query.lower().replace(phrase, "").strip()

    formatted_search = query.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{formatted_search}"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
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

        return title, paragraph if paragraph else "No suitable paragraph found"

    except Exception as e:
        return "Error", f"⚠️ Failed to scrape Wikipedia: {e}"

