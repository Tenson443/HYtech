import requests

import requests


def ask_ollama(message):
    url = "http://localhost:11434/api/generate"

    pre_prompt = """You are a strict classification algorithm, NOT a conversational AI. Do not greet me. Do not say "I am ready". Do not ask what the question is. 
Your ONLY job is to output a single word from the allowed list.

Strict Rules:
1. Output MUST be exactly one of these subjects: Integrals, Extrema, Inductions, Series, Geometry, Trigonometry, Functions, Other
2. If the question does not fit any subject, output exactly: Other

Examples:
Message: im having an issue finding the edge x in the triangle with the 20 and 60 edges
Output: Geometry

Message: how do i solve an integral of x^2
Output: Integrals

Message: what is the maximum value of x^2 - 4x + 3
Output: Extrema

Message: prove by induction that 1+2+...+n = n(n+1)/2
Output: Inductions

Message: what is sin(90)
Output: Trigonometry

Message: find the sum of the geometric series
Output: Series

Message: how do i solve 2x + 5 = 15
Output: Functions

Message: what is the capital of France
Output: Other

"""

    full_prompt = pre_prompt + f"Message: {message}\nOutput: "

    payload = {
        "model": "llama3.2:3b",
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.0
        }
    }

    VALID_SUBJECTS = {"Integrals", "Extrema", "Inductions", "Series", "Geometry", "Trigonometry", "Functions", "Other"}

    try:
        # FIX: Increased timeout from 10 to 30. Local LLMs often take 15-20 seconds to "wake up" on the very first prompt!
        response = requests.post(url, json=payload, timeout=30)

        result = response.json()["response"].strip().replace(".", "").replace('"', '').replace("'", "")
        result = result.capitalize()

        if result not in VALID_SUBJECTS:
            print(f"\n--- DEBUG: AI failed on '{message}' ---")
            print(f"--- DEBUG: AI actually outputted: '{result}' ---\n")
            return "Other"

        return result
    except Exception as e:
        print(f"DEBUG: Exception occurred - {e}")
        return "Other"

if __name__ == "__main__":
    print("What is your question?")
    while True:
        prompt = input()
        if prompt.strip().lower() == "end":
            break
        answer = ask_ollama(prompt)
        print(answer)
    print("Bye, have a nice day.")
if __name__ == "__main__":
    print("What is your question?")
    while True:
        prompt = input()
        if prompt.strip().lower() == "end":
            break
        answer = ask_ollama(prompt)
        print(answer)
    print("Bye, have a nice day.")