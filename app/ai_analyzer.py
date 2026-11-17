
import json
import os

from groq import Groq


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def ask_llm(prompt: str):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_completion_tokens=300,
        stream=False
    )

    return response.choices[0].message.content


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
