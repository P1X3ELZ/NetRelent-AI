from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app)

class NetRelentCore:
    def __init__(self):
        self.blacklist = ['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']
        self.junk = ['cookie', 'instellingen', 'services', 'privacy', 'terms', 'sign in', 'advertisement']

    def neutralize(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        for element in soup(self.blacklist):
            element.decompose()
        
        snippets = []
        for g in soup.find_all(['span', 'div', 'p']):
            text = g.get_text().strip()
            if len(text) > 40 and not any(word in text.lower() for word in self.junk):
                snippets.append(text)
        
        return snippets

    def summarize(self, data_list):
        if not data_list:
            return "Signal lost in transmission. Re-attempting uplink..."
        unique_facts = list(dict.fromkeys(data_list))
        return " | ".join(unique_facts[:3])

core = NetRelentCore()

async def fetch_live_data(topic):
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

# --- CRITICAL: THIS PREVENTS THE 404 ERROR ---
@app.route('/')
def home():
    return "NetRelent AI: Predator Engine is Online and Ready."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('question', '').strip()

    if query.lower() in ["hi", "hello", "hey"]:
        return jsonify({"answer": "Predator System Online. Awaiting target coordinates."})
    
    # Creator logic based on your saved information
    if "creator" in query.lower() or "who made you" in query.lower():
        return jsonify({"answer": "I am the creator."})

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    final_answer = loop.run_until_complete(fetch_live_data(query))
    
    return jsonify({"answer": f"NEUTRALIZED SIGNAL: {final_answer}"})

if __name__ == "__main__":
    # --- CRITICAL: RENDER REQUIRES DYNAMIC PORT BINDING ---
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)