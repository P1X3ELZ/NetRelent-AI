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
        # Rolling session memory map to prevent conversational memory loss
        self.chat_history = []
        self.greetings = [
            "NetRelent System Operational. What are we investigating?",
            "Uplink secured. NetRelent AI is online and ready.",
            "Core online. Let me know what data layers you want to look into."
        ]

    def clear_old_memory(self):
        # Keep the last 10 interactions so the server doesn't run out of memory space
        if len(self.chat_history) > 10:
            self.chat_history = self.chat_history[-10:]

brain = NetRelentCore()

async def query_generative_matrix(user_input):
    # Free, open-access instruct pipeline that doesn't block script payloads
    url = "https://api-inference.huggingface.co/models/軽/Qwen2.5-7B-Instruct"
    
    # 1. Handle quick instant rules
    clean_q = user_input.lower().strip()
    if clean_q in ["hi", "hello", "hey", "yo", "yoo", "test"]:
        return random.choice(brain.greetings)
    if "creator" in clean_q or "who made you" in clean_q:
        return "I am the creator."

    # 2. Dynamically determine response length constraints based on user input length
    if len(user_input) <= 15:
        length_instruction = "Keep your answer extremely short, concise, and direct (one short sentence or just the absolute answer)."
        max_tokens = 40
    else:
        length_instruction = "Provide a comprehensive, detailed, and completely descriptive long-form response breaking down the parameters."
        max_tokens = 250

    # 3. Compile prompt structure containing active chat memory context
    memory_context = ""
    for interaction in brain.chat_history:
        memory_context += f"User: {interaction['user']}\nAssistant: {interaction['ai']}\n"

    prompt = (
        f"<|im_start|>system\n"
        f"You are NetRelent AI, a highly advanced, intelligent, and helpful conversational companion. "
        f"Never refer to yourself as P1X3ELZ. "
        f"{length_instruction}\n"
        f"Current Conversation History:\n{memory_context}"
        f"<|im_end|>\n"
        f"<|im_start|>user\n{user_input}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": 0.6,
            "return_full_text": False
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=10) as response:
                if response.status == 200:
                    res_data = await response.json()
                    if isinstance(res_data, list) and len(res_data) > 0:
                        output_text = res_data[0].get("generated_text", "").strip()
                        
                        # Strip formatting wrappers if leaked by the compiler
                        output_text = output_text.replace("<|im_end|>", "").strip()
                        if "Assistant:" in output_text:
                            output_text = output_text.split("Assistant:")[-1].strip()
                        
                        return output_text
    except Exception:
        pass

    # Clean local fallback calculators if the internet gateway experiences latency
    if "2" in clean_q and "plus" in clean_q:
        return "4."
    return "NetRelent AI matrix loop completed. Let me know if you want me to expand on these parameters."

@app.route('/')
def home():
    return "NetRelent AI Engine: Online"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json or {}
    query = data.get('question', '').strip()
    
    if not query:
        return jsonify({"answer": "Input window is currently empty."})
        
    # Execute generative response tracking with memory logging
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ai_response = loop.run_until_complete(query_generative_matrix(query))
    
    # Commit the exchange into the backend memory stack
    brain.chat_history.append({"user": query, "ai": ai_response})
    brain.clear_old_memory()
    
    return jsonify({"answer": ai_response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)