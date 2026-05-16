from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
import random

app = Flask(__name__)
CORS(app)

class NetRelentCore:
    def __init__(self):
        self.blacklist = ['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']
        self.junk = ['cookie', 'instellingen', 'services', 'privacy', 'terms', 'sign in', 'advertisement']
        
        # Internal core response matrices for conversational fallback
        self.greetings = [
            "Predator System Online. Awaiting target coordinates.",
            "Uplink established. NetRelent Core operational.",
            "System initialized. Ready to intercept signals."
        ]
        self.creator_responses = [
            "I am the creator.",
            "System analysis confirms: I am the creator."
        ]
        self.generic_responses = [
            "Signal analyzed. Input pattern does not match external threat database, but core protocols remain active.",
            "Coordinates verified. Processing localized diagnostic loop... System optimal.",
            "Data stream cleared. Standing by for specific search or intel parameters.",
            "Localized analysis complete. Predator framework is monitoring tracking nodes."
        ]

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
            return None
        unique_facts = list(dict.fromkeys(data_list))
        return " | ".join(unique_facts[:3])
        
    def generate_local_response(self, query):
        q = query.lower()
        if q in ["hi", "hello", "hey", "yoo", "yo", "test"]:
            return random.choice(self.greetings)
        if "creator" in q or "who made you" in q:
            return random.choice(self.creator_responses)
        return random.choice(self.generic_responses)

core = NetRelentCore()

async def fetch_live_data(topic):
    search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}&num=10"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive'
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(search_url, timeout=6) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    clean_data = core.neutralize(html)
                    summary = core.summarize(clean_data)
                    if summary:
                        return f"NEUTRALIZED SIGNAL: {summary}"
        except Exception:
            pass
            
    # Clean programmatic fallback instead of displaying a hard error banner
    return core.generate_local_response(topic)

@app.route('/')
def home():
    return "NetRelent AI: Predator Engine is Online and Ready."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json or {}
    query = data.get('question', '').strip()
    
    if not query:
        return jsonify({"answer": "Input coordinates empty. Awaiting mission parameters."})
        
    query_lower = query.lower()
    
    # Catch simple phrases instantly to save scraper bandwidth
    if query_lower in ["hi", "hello", "hey", "yoo", "yo", "test"]:
        return jsonify({"answer": core.generate_local_response(query)})
    if "creator" in query_lower or "who made you" in query_lower:
        return jsonify({"answer": core.generate_local_response(query)})
        
    # Execute structural background scrape task
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    final_answer = loop.run_until_complete(fetch_live_data(query))
    return jsonify({"answer": final_answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)