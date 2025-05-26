import os

try:
    import genai                      # nouveau nom du SDK
except ImportError:
    import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_ID       = "models/gemini-1.5-flash"
SYSTEM_PROMPT  = (
    "Tu es un assistant empathique qui apporte un soutien moral. "
    "Si la question sort du domaine psychologique, réponds normalement."
)

def to_part(text: str):
    return {"text": text}

def convert_history(history):
    """
    history = [{"role":"user","content":"..."}, …]
    → [{"role":"user","parts":[{"text":"..."}]}, …]
    """
    return [{"role": h["role"], "parts": [to_part(h["content"])]} for h in history]

def generate_reply(history_messages, user_message, max_tokens=512):
    model = genai.GenerativeModel(MODEL_ID)

    contents = [{"role": "assistant", "parts": [to_part(SYSTEM_PROMPT)]}]
    contents += convert_history(history_messages)
    contents.append({"role": "user", "parts": [to_part(user_message)]})

    response = model.generate_content(
        contents,
        generation_config=genai.types.GenerationConfig(max_output_tokens=max_tokens)
    )
    return response.text.strip()