from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import aiohttp
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

class NetRelentCore:
    def __init__(self):
        self.blacklist = ['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']
        # Junk words to filter out (including those Dutch cookie terms you saw)
        self.junk = ['cookie', 'instellingen', 'services', 'privacy', 'terms', 'sign in', 'advertisement']

    def neutralize(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        for element in soup(self.blacklist):
            element.decompose()
        
        # Target common snippet classes for Google
        snippets = []
        # Look for paragraph tags or specific div blocks that usually hold news
        for g in soup.find_all(['span', 'div', 'p']):
            text = g.get_text().strip()
            if len(text) > 40 and not any(word in text.lower() for word in self.junk):
                snippets.append(text)
        
        return snippets

    def summarize(self, data_list):
        if not data_list:
            return "Signal lost in transmission. Re-attempting uplink..."
        
        # Remove duplicates and keep the top 3 most unique facts
        unique_facts = list(dict.fromkeys(data_list))
        return " | ".join(unique_facts[:3])

core = NetRelentCore()

async def fetch_live_data(topic):
    # Added 'hl=en' to the URL to force English results regardless of server location
    search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}&hl=en"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(search_url, timeout=10) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    clean_data = core.neutralize(html)
                    return core.summarize(clean_data)
        except Exception as e:
            return f"Error: {str(e)}"
    return "Neutralization failed: Target shielded."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('question', '').strip()

    if query.lower() in ["hi", "hello", "hey"]:
        return jsonify({"answer": "Predator System Online. Awaiting target coordinates."})
    
    if "creator" in query.lower() or "who made you" in query.lower():
        # Referencing the creator as requested in your saved info
        return jsonify({"answer": "I am the creator."})

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    final_answer = loop.run_until_complete(fetch_live_data(query))
    
    return jsonify({"answer": f"NEUTRALIZED SIGNAL: {final_answer}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)