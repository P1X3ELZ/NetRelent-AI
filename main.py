from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import aiohttp
import os
import random

app = Flask(__name__)
CORS(app)

class NetRelentEngine:
    def __init__(self):
        self.greetings = [
            "Hey! NetRelent AI is up and running. What's on your mind?",
            "Hello! Systems are online. How can I help you out today?",
            "Yo! Uplink established. Shoot me your questions."
        ]

    def local_logic(self, query):
        q = query.lower().strip()
        if q in ["hi", "hello", "hey", "yoo", "yo", "test"]:
            return random.choice(self.greetings)
        if "creator" in q or "who made you" in q:
            return "I am the creator."
        return None

core_engine = NetRelentEngine()

async def generate_ai_response(query):
    # Route through a high-speed public generative language pipeline
    url = "https://api-inference.huggingface.co/models/軽/Qwen2.5-7B-Instruct"
    
    # Clean prompt context to keep answers concise, sharp, and helpful
    payload = {
        "inputs": f"<|im_start|>system\nYou are NetRelent AI, a helpful, smooth, and intelligent conversational assistant. Give concise, engaging, and directly helpful answers without sounding overly dramatic or tech-robotic.<|im_end|>\n<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant\n",
        "parameters": {"max_new_tokens": 150, "temperature": 0.7}
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=8) as response:
                if response.status == 200:
                    res_data = await response.json()
                    if isinstance(res_data, list) and len(res_data) > 0:
                        full_text = res_data[0].get("generated_text", "")
                        # Split away the structural prompt framing if present
                        if "<|im_start|>assistant\n" in full_text:
                            return full_text.split("<|im_start|>assistant\n")[-1].replace("<|im_end|>", "").strip()
                        return full_text.strip()
    except Exception:
        pass

    # Clean conversational fallback if internet access slows down
    return f"I hear you. I'm currently processing some data nodes regarding '{query}'—let me know if you want me to look into anything else!"

@app.route('/')
def home():
    return "NetRelent AI: Engine is Online and Ready."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json or {}
    query = data.get('question', '').strip()
    
    if not query:
        return jsonify({"answer": "Input field is empty. Let me know what you need!"})
        
    # Check for direct greetings or creator inquiries instantly
    local_check = core_engine.local_logic(query)
    if local_check:
        return jsonify({"answer": local_check})
        
    # Run generative text model pipeline
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ai_response = loop.run_until_complete(generate_ai_response(query))
    
    return jsonify({"answer": ai_response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)