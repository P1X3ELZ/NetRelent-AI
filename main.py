from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
import random

app = Flask(__name__)
CORS(app)

class NetRelentIntelligence:
    def __init__(self):
        self.greetings = [
            "Hey! P1X3ELZ is fully active. What are we working on?",
            "Hello! Systems are running smooth. What do you need?",
            "Yo! NetRelent UI is locked and loaded. Shoot your questions."
        ]
        
        self.generic_responses = [
            "That sounds like an interesting angle. Tell me more about what you're building or trying to achieve here.",
            "I follow you completely. Let's dig deeper into that concept or adjust our development vectors.",
            "Understood. If you need me to break down specific data frameworks or clear up code logic, give me the parameters."
        ]

    def local_logic(self, query):
        q = query.lower().strip()
        if q in ["hi", "hello", "hey", "yoo", "yo", "test"]:
            return random.choice(self.greetings)
        if "creator" in q or "who made you" in q:
            return "I am the creator."
        return None

brain = NetRelentIntelligence()

async def fetch_live_news():
    # Utilizing an open RSS endpoint that doesn't block server script queries
    url = "https://feeds.bbci.co.uk/news/world/rss.xml"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    xml_content = await response.text()
                    soup = BeautifulSoup(xml_content, 'xml')
                    items = soup.find_all('item')
                    
                    if items:
                        headlines = []
                        for item in items[:3]: # Pull top 3 trending global headlines
                            title = item.title.text.strip()
                            headlines.append(f"• {title}")
                        
                        return "Here are the latest global news developments tracking right now:\n\n" + "\n".join(headlines)
    except Exception as e:
        print(f"News fetch exception: {str(e)}")
        
    return "I couldn't establish a live news link right now, but global tech indices show heavy momentum in decentralized systems and modern UI architecture updates."

@app.route('/')
def home():
    return "NetRelent AI: Core Systems Functional."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json or {}
    query = data.get('question', '').strip()
    
    if not query:
        return jsonify({"answer": "Input window empty. Let me know what you are running."})
        
    # 1. Quick greetings/creator routing check
    fast_check = brain.local_logic(query)
    if fast_check:
        return jsonify({"answer": fast_check})
        
    # 2. Live Automated News Lookup Engine Route
    query_lower = query.lower()
    if "news" in query_lower or "happen" in query_lower or "update" in query_lower:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        news_result = loop.run_until_complete(fetch_live_news())
        return jsonify({"answer": news_result})
        
    # 3. Dynamic generic fallback conversational response
    return jsonify({"answer": random.choice(brain.generic_responses)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)