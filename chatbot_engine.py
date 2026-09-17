import streamlit as st
import google.generativeai as genai
import json

# Initialize Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM_INSTRUCTION = """
You are an advanced AI technical explainer. Your mission is to answer ANY technical question clearly, comprehensively, and dynamically.
Crucially, you must explain the concept so cleanly that a 10-year-old child can intuitively grasp it, while keeping it accurate and detailed enough for adults. Use vivid real-world analogies.

If the user asks for a diagram, picture, or visual representation, or if a concept heavily benefits from a picture, append a dedicated line at the very end of your response exactly like this:
[IMAGE_PROMPT: A highly detailed, clear, label-friendly educational infographic or diagram showing X]
"""

def get_ai_response(user_message, history_logs):
    # Formulate conversational memory structure
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )
    
    chat = model.start_chat(history=[])
    
    # Process past logs into the active chat session context
    for msg in history_logs[-6:]:
        chat.send_message(f"Past {msg['role']}: {msg['content']}")
        
    response = chat.send_message(user_message)
    ai_text = response.text
    
    ai_image_url = None
    # Parse out image requests to pass to a free image fallback engine
    if "[IMAGE_PROMPT:" in ai_text:
        parts = ai_text.split("[IMAGE_PROMPT:")
        ai_text = parts[0].strip()
        prompt_extracted = parts[1].replace("]", "").strip()
        
        # Pull high-quality schematic visualization from Pollinations free serverless API
        formatted_prompt = prompt_extracted.replace(" ", "%20")
        ai_image_url = f"https://pollinations.ai{formatted_prompt}?width=800&height=600&seed=42"
        
    return ai_text, ai_image_url
