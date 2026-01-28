from google import genai #type: ignore
import time
import os

GEMINI_KEYS = [
]

MODEL_NAME = "gemini-2.0-flash" 

current_key_index = 0

def convert_with_gemini(text, target_language):
    global current_key_index
    
    TANGLISH_PROMPT = """
You are a native Tamil speaker from Chennai. Translate the following English text into 'Tanglish' (Tamil words written in English script).
RULES:
1. You MUST use Tamil verbs for actions (e.g., 'work aagala', 'restart pannunga').
2. Keep technical nouns in English (Printer, Network, Wi-Fi, Bank, OTP).
3. Do NOT use Hindi words like 'arre', 'na', 'ya'.
4. Output ONLY the translation.
"""

    HINGLISH_PROMPT = """
You are a native Hindi speaker. Translate the following English text into 'Hinglish'.
RULES:
1. Use Hindi grammar (e.g., 'kaam nahi kar raha hai').
2. Keep technical nouns in English.
3. Output ONLY the translation.
"""
    
    for attempt in range(len(GEMINI_KEYS)):
        try:
            api_key = GEMINI_KEYS[current_key_index]
            genai.configure(api_key=api_key)
            
            model = genai.GenerativeModel(MODEL_NAME)
            
            if target_language == "Tanglish":
                prompt = TANGLISH_PROMPT + f"\n\nTEXT TO TRANSLATE:\n{text}"
            else:
                prompt = HINGLISH_PROMPT + f"\n\nTEXT TO TRANSLATE:\n{text}"
            
            print(f"Using API Key #{current_key_index + 1} with {MODEL_NAME}...")
            response = model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            
        except Exception as e:
            error_msg = str(e)
            
            if "429" in error_msg or "quota" in error_msg.lower() or "resource_exhausted" in error_msg.lower():
                print(f"API Key #{current_key_index + 1} quota exceeded")
                current_key_index = (current_key_index + 1) % len(GEMINI_KEYS)
                
                if attempt < len(GEMINI_KEYS) - 1:
                    print(f"Switching to API Key #{current_key_index + 1}")
                    time.sleep(1)
                    continue
                else:
                    print("All API keys exhausted for today")
                    return None
            else:
                print(f"Gemini Error on Key #{current_key_index + 1}: {e}")
                return None
    
    return None