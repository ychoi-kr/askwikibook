import openai

openai.api_key_path = "/home/askwikibook/settings/OPENAI_API_KEY"

def generateSQL(schemas, natural_query, dialect="SQLite"):
    messages = [
        {"role": "system", "content": "You interpret a query in natural language into SQL."},
    ]
    prompt = "Table(s) in " + dialect + " database:\n"
    for table, schema in schemas.items():
        prompt += table + ':' + schema + '\n'
    prompt += "\n\nMake SQL query doing:\n"
    prompt += natural_query
    prompt += "\n\nSQL:"

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