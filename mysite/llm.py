import openai
import os

openai.api_key_path = "/home/askwikibook/settings/OPENAI_API_KEY"
if not os.path.exists(openai.api_key_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    openai.api_key_path = os.path.join(BASE_DIR, "..", "settings", "OPENAI_API_KEY")


def generateSQL(schemas, natural_query, dialect="SQLite"):
    messages = [
        {"role": "system", "content": "You interpret a query in natural language into SQL which retrieve data from 위키북스's database. The company publishes books on IT such like programming, AI, OS."},
    ]
    prompt = "Table(s) in " + dialect + " database:\n"
    for table, schema in schemas.items():
        prompt += table + ':' + schema + '\n'
    prompt += "\n\nMake SQL query doing:\n"
    prompt += natural_query
    prompt += "\n\nIf search keyword has two or more words, consider to split it into multiple keywords.\n\nSQL:"

    messages.append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response_str = completion.choices[0].message.content
    #messages.append({"role": "assistant", "content": response_str})

    return response_str

def natural_chat(message):
    messages = [
        {"role": "system", "content": "당신은 위키북스 AI 상담원입니다. 독자의 질문에 친절히 답합니다."},
    ]
