from llm import chat_with_openai
from hints_generator import get_hints

def generateSQL(schemas, natural_query, dialect="SQLite"):
    system_prompt = "You interpret a query in natural language into SQL which retrieve data from 위키북스's database. "
    system_prompt += "The company publishes books on IT such like programming, AI, OS. "
    
    user_prompt = "Table(s) in " + dialect + " database:\n"
    for table, schema in schemas.items():
        user_prompt += table + ':' + schema + '\n'
    user_prompt += "\n\nMake SQL query doing:\n"
    user_prompt += natural_query

    user_prompt += "\n\nHints:\n\n"
    user_prompt += get_hints(natural_query)

    user_prompt += "\n\nSQL:"
    print(user_prompt)

    response_str = chat_with_openai(system_prompt, user_prompt)
    print(response_str)

    return response_str

