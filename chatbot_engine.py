import streamlit as st
from google import genai
import json

# Initialize the new modern Gemini Client using your saved secret key
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM_INSTRUCTION = """
You are an advanced AI technical explainer. Your mission is to answer ANY technical question clearly, comprehensively, and dynamically.
Crucially, you must explain the concept so cleanly that a 10-year-old child can intuitively grasp it, while keeping it accurate and detailed enough for adults. Use vivid real-world analogies.

If the user asks for a diagram, picture, or visual representation, or if a concept heavily benefits from a picture, append a dedicated line at the very end of your response exactly like this:
[IMAGE_PROMPT: A highly detailed, clear, label-friendly educational infographic or diagram showing X]
"""

def get_ai_response(user_message, history_logs):
    # Format conversational memory strings for the model context
    formatted_contents = []
    for msg in history_logs[-6:]:
        role_label = "user" if msg['role'] == "user" else "model"
        formatted_contents.append({"role": role_label, "parts": [{"text": msg['content']}]})
        
    # Append the current active user message
    formatted_contents.append({"role": "user", "parts": [{"text": user_message}]})
        
    # Trigger modern Gemini 2.0 Flash response call
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=formatted_contents,
        config={'system_instruction': SYSTEM_INSTRUCTION}
    )
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
