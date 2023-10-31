from llm import chat_with_openai
from hints_generator import get_more_hints

def generateSQL(schemas, natural_query, dialect="SQLite"):
    system_prompt = "You interpret a query in natural language into SQL which retrieve data from 위키북스's database. "
    system_prompt += "The company publishes books on IT such like programming, AI, OS. "
    
    user_prompt = "Table(s) in " + dialect + " database:\n"
    for table, schema in schemas.items():
        user_prompt += table + ':' + schema + '\n'
    user_prompt += "\n\nMake SQL query doing:\n"
    user_prompt += natural_query

    user_prompt += "\n\nHints:\n\n"
    user_prompt += "A good place to look for a product or service name is in the title or book_intro.\n"
    user_prompt += get_more_hints(natural_query)

    user_prompt += "\n\nSQL:"
    print(user_prompt)

    response_str = chat_with_openai(system_prompt, user_prompt)
    return response_str

