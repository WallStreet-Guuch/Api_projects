import os
import requests

def generate_ai_system_brief(raw_telemetry):
    api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_KEY")
    endpoint = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are an autonomous engineering assistant. Analyze system telemetry and give a concise 2-sentence executive summary."
            },
            {
                "role": "user",
                "content": f"Analyze this regional grid status: {raw_telemetry}"
            }
        ],
        "temperature": 0.3
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    
    if response.status_code == 200:
        ai_message = response.json()["choices"][0]["message"]["content"]
        print("--- Autonomous AI Telemetry Summary ---")
        print(ai_message)
    else:
        print(f"AI API Error: HTTP {response.status_code}")

# Example Run
sample_data = "Solar output dropped 40% in 15 mins due to localized storm. Battery reserves at 82%."
generate_ai_system_brief(sample_data)