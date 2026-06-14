import json
from urllib import response
import requests

def ask_llm(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "qwen2.5:3b",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {"num_predict": 200}
        }
    )
    return response.json()["message"]["content"]

def analyze_code_with_ai(
    code: str,
    metrics: dict,
    prediction: str,
    probability: float
):

    prompt = f"""
You are a senior software engineer and code reviewer.

Analyze the following Python code.

Prediction:
{prediction}

Probability:
{probability}

Metrics:
{json.dumps(metrics)}

Code:
{code}

Return your response in the following format:

SUMMARY:
<short summary>

ISSUES:
- issue 1
- issue 2
- issue 3

RECOMMENDATIONS:
- recommendation 1
- recommendation 2
- recommendation 3

RISK_ASSESSMENT:
<risk explanation>
"""
    response = ask_llm(prompt)
    
    return response