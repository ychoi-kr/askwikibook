import openai
import os
import re

from string_utils import contains_any


openai.api_key_path = "/home/askwikibook/settings/OPENAI_API_KEY"
if not os.path.exists(openai.api_key_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    openai.api_key_path = os.path.join(BASE_DIR, "..", "settings", "OPENAI_API_KEY")


def generateSQL(schemas, natural_query, dialect="SQLite"):
    system_prompt = "You interpret a query in natural language into SQL which retrieve data from 위키북스's database. "
    system_prompt += "The company publishes books on IT such like programming, AI, OS. "
    messages = [
        {"role": "system", "content": system_prompt},
    ]

    user_prompt = "Table(s) in " + dialect + " database:\n"
    for table, schema in schemas.items():
        user_prompt += table + ':' + schema + '\n'
    user_prompt += "\n\nMake SQL query doing:\n"
    user_prompt += natural_query
    user_prompt += "\n\nHints:\n\n"
    #user_prompt += "Before create SQL, think about what a query in Korean would mean in English.\n"
    user_prompt += "A good place to look for a product or service name is in the title or book_intro.\n"
    
    user_prompt += get_more_hints(natural_query)

    user_prompt += "\nSQL:"
    print(user_prompt)
    messages.append({"role": "user", "content": user_prompt})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response_str = completion.choices[0].message.content
    #messages.append({"role": "assistant", "content": response_str})

    return response_str


def get_more_hints(natural_query):
    hint = []
    if 1 < len(natural_query.split()) < 4 and contains_any(natural_query, ["도서", "서적", "책"]):
        hint.append("If search keyword has two or more words, consider to split it into multiple keywords.")

    if contains_any(natural_query, ["비싼", "재미있는", "재밌는", "저렴한", "좋은"]):
        hint.append("Words that describe the character of a book may not be keywords.")

    if re.search(r"\b신간\b", natural_query):
        hint.append('In Korean, the word "신간" means "new book", so it probably won\'t be included in the title or intro_book.')

    else:
        if not contains_any(natural_query, ["구간", "부터", "순서", "순으로", "옛날", "오래된", "정렬"]):
            hint.append("Unless otherwise specified, it sorts in reverse order of pubdate.")
    
        if not contains_any(natural_query, [" 다 ", "다알려줘", "다찾아", "모두", "모든", "싹다", "싹 다", "전부", "하나도 빼놓지 말고"]):
            hint.append("Unless otherwise specified, it limits to 10.")

    if contains_any(natural_query, ["자바", "Java", "java"]) and not contains_any(natural_query, ["자바스크립트", "JavaScript", "javascript"]):
        hint.append("When using Java as a keyword, it's a good idea to exclude JavaScript.")

    if "c++" in natural_query:
        hint.append('You can also get good results by searching for "C++" as well as "c++".')

    if "Java" in natural_query:
        hint.append('You can also get good results by searching for "자바" or "java" as well as "Java".')

    if contains_any(natural_query, ["교수", "근무", "대학교", "박사", "석사", "재직", "졸업", "출신"]) or re.search(r"대\b", natural_query):
        hint.append("Organization name can also be found in intro_author.")

    return '\n'.join(hint) 


def natural_chat(message):
    messages = [
        {"role": "system", "content": "당신은 위키북스 AI 상담원입니다. 독자의 질문에 친절히 답합니다."},
    ]
