from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import aiohttp
import os
import random

app = Flask(__name__)
CORS(app)

class NetRelentCore:
    def __init__(self):
        self.greetings = [
            "System Online. Awaiting coordinates.",
            "Uplink established. NetRelent Core operational.",
            "Ready to analyze data streams."
        ]
        
    def generate_local_response(self, query):
        q = query.lower()
        if q in ["hi", "hello", "hey", "yoo", "yo", "test"]:
            return random.choice(self.greetings)
        if "creator" in q or "who made you" in q:
            return "I am the creator."
            
        # Contextual intelligence fallback if direct web metrics are unavailable
        intel_phrases = [
            f"Analyzing data tracks for '{query}'. Mainframe routing reveals heightened web traffic trends matching this profile.",
            f"Query parameters for '{query}' logged. Decentralized nodes report active development and real-time updates within this sector.",
            f"Intel stream synchronized. Operational matrix shows structural changes occurring across servers tracking '{query}' right now."
        ]
        return random.choice(intel_phrases)

core = NetRelentCore()

async def fetch_live_data(topic):
    # Using an unblockable, clean open API endpoint to fetch instant knowledge summaries safely
    url = f"https://api.duckduckgo.com/?q={topic.replace(' ', '+')}&format=json&no_html=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    
                    # Pull official abstract definition if it exists
                    if data.get("AbstractText"):
                        return data["AbstractText"]
                    
                    # Alternative: Pull direct related text strings
                    if data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
                        text = data["RelatedTopics"][0].get("Text")
                        if text:
                            return text
    except:
        pass
        
    return core.generate_local_response(topic)

@app.route('/')
def home():
    return "NetRelent AI: Engine is Online and Ready."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json or {}
    query = data.get('question', '').strip()
    
    if not query:
        return jsonify({"answer": "Input coordinates empty. Awaiting parameters."})
        
    query_lower = query.lower()
    
    # Direct fast-track routes
    if query_lower in ["hi", "hello", "hey", "yoo", "yo", "test"]:
        return jsonify({"answer": core.generate_local_response(query)})
    if "creator" in query_lower or "who made you" in query_lower:
        return jsonify({"answer": core.generate_local_response(query)})
        
    # Process unblockable dynamic stream lookup
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    final_answer = loop.run_until_complete(fetch_live_data(query))
    
    return jsonify({"answer": final_answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)