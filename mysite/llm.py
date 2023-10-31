import openai
import os

openai.api_key_path = "/home/askwikibook/settings/OPENAI_API_KEY"
if not os.path.exists(openai.api_key_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    openai.api_key_path = os.path.join(BASE_DIR, "..", "settings", "OPENAI_API_KEY")

def chat_with_openai(system_prompt, user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return completion.choices[0].message.content

