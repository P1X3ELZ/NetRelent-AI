from flask import Flask, request, jsonify
from flask_cors import CORS
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
        
        # Keyword-based natural response matrices
        self.knowledge_base = {
            "news": [
                "The tech world is moving fast right now—AI developments are scaling rapidly, open-source communities are expanding, and server frameworks are getting lighter.",
                "Global tech networks are currently focusing heavily on decentralized web apps, instant execution APIs, and premium glassmorphic UI engineering trends.",
                "Latest updates point toward massive efficiency gains in edge-computing servers and clean user interfaces dominates modern design boards."
            ],
            "weather": [
                "Systems report optimal atmospheric conditions across core data sectors. Standard local readings appear steady.",
                "Satellite feeds show standard cloud patterns and stable regional weather variables across major web hosting hubs."
            ],
            "coding": [
                "Writing clean architecture is key. Keep your functions isolated, handle execution errors cleanly, and optimize backend routes.",
                "Always make sure your cross-origin policies (CORS) are properly declared and keep your dependencies updated to avoid silent compilation issues."
            ],
            "status": [
                "All memory channels are perfectly balanced, server response cycles are below 12ms, and the UI link is stable.",
                "Systems are operating at 100% capacity. Node pathways are cleared for execution."
            ]
        }

        self.generic_responses = [
            "That sounds like an interesting angle. Tell me more about what you're building or trying to achieve here.",
            "I follow you completely. Let's dig deeper into that concept or adjust our development vectors.",
            "Understood. If you need me to break down specific data frameworks or clear up code logic, give me the parameters.",
            "Systems logged that thought. Let's see how we can map that out into our current workspace design layout."
        ]

    def think(self, user_query):
        q = user_query.lower().strip()
        
        # Direct instant rules
        if q in ["hi", "hello", "hey", "yoo", "yo", "test"]:
            return random.choice(self.greetings)
            
        if "creator" in q or "who made you" in q:
            return "I am the creator."

        # Scan for matching conversational contexts
        if "news" in q or "update" in q or "happen" in q:
            return random.choice(self.knowledge_base["news"])
        if "weather" in q or "temperature" in q:
            return random.choice(self.knowledge_base["weather"])
        if "code" in q or "program" in q or "script" in q or "bug" in q:
            return random.choice(self.knowledge_base["coding"])
        if "status" in q or "system" in q or "working" in q:
            return random.choice(self.knowledge_base["status"])

        # Smart fallback if input doesn't trigger specific category rules
        return random.choice(self.generic_responses)

brain = NetRelentIntelligence()

@app.route('/')
def home():
    return "NetRelent AI: Core Systems Functional."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json or {}
    query = data.get('question', '').strip()
    
    if not query:
        return jsonify({"answer": "Input window empty. Let me know what you are running."})
        
    # Execute immediate conversational lookup without external API block risks
    response_text = brain.think(query)
    return jsonify({"answer": response_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)