from openai import OpenAI
import os

f = open("../.secret")
for l in f.readlines():
    k, v = l.split("=")
    os.environ[k] = v.strip()

client = OpenAI()

def chat_with_openai(system_prompt, user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return completion.choices[0].message.content

