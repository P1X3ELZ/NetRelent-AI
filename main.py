from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
import random
import re

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
        
        # 1. Direct Greetings
        if q in ["hi", "hello", "hey", "yoo", "yo", "test"]:
            return random.choice(self.greetings)
            
        # 2. Creator Definition
        if "creator" in q or "who made you" in q or "who created you" in q:
            return "I am the creator."
            
        # 3. Native Math Calculation Engine
        math_match = re.search(r'(\d+)\s*([\+\-\*\/])\s*(\d+)', q)
        if math_match:
            try:
                num1 = int(math_match.group(1))
                op = math_match.group(2)
                num2 = int(math_match.group(3))
                if op == '+': result = num1 + num2
                elif op == '-': result = num1 - num2
                elif op == '*': result = num1 * num2
                elif op == '/': result = num1 / num2 if num2 != 0 else "undefined (cannot divide by zero)"
                return f"Calculation complete: {num1} {op} {num2} = {result}."
            except Exception:
                pass
                
        return None

brain = NetRelentIntelligence()

async def fetch_live_news(region="world"):
    # Target custom RSS endpoints based on user input flags
    if region == "middle_east":
        url = "https://feeds.bbci.co.uk/news/world/middle_east/rss.xml"
        header_text = "Here are the latest BBC News updates tracking across the Middle East right now:"
    else:
        url = "https://feeds.bbci.co.uk/news/world/rss.xml"
        header_text = "Here are the latest global news developments tracking right now:"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=6) as response:
                if response.status == 200:
                    xml_content = await response.text()
                    soup = BeautifulSoup(xml_content, 'xml')
                    items = soup.find_all('item')
                    
                    if items:
                        headlines = []
                        for item in items[:3]: # Pull top 3 hot-topic headlines
                            title = item.title.text.strip()
                            headlines.append(f"• {title}")
                        
                        return f"{header_text}\n\n" + "\n".join(headlines)
    except Exception:
        pass
        
    return "I couldn't establish a live news uplink data packet stream right now. Please test the input parameter again shortly."

@app.route('/')
def home():
    return "NetRelent AI: Core Systems Functional."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json or {}
    query = data.get('question', '').strip()
    
    if not query:
        return jsonify({"answer": "Input window empty. Let me know what you are running."})
        
    # Check for greetings, math equations, or creator questions first
    fast_check = brain.local_logic(query)
    if fast_check is not None:
        return jsonify({"answer": fast_check})
        
    # Smart Regional News Routing Configuration
    query_lower = query.lower()
    if "news" in query_lower or "happen" in query_lower or "update" in query_lower:
        region = "world"
        if "middle east" in query_lower or "east" in query_lower:
            region = "middle_east"
            
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        news_result = loop.run_until_complete(fetch_live_news(region))
        return jsonify({"answer": news_result})
        
    # Dynamic general fallback response
    return jsonify({"answer": random.choice(brain.generic_responses)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)