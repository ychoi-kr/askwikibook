import openai
import os
import re

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

    sql = validate_and_correct_sql(response_str, dialect)
    sql = add_ean_and_url_columns(sql)
    return sql


def add_ean_and_url_columns(sql_query):
    """
    Add the 'ean' and 'url' columns to the SQL SELECT statement if they're not already present. 
    The resulting columns will be aliased as '_ean' and '_url'.
    """
    # Check if the query is a SELECT statement followed by a "FROM BOOKS" clause
    if re.search(r"FROM\s+BOOKS", sql_query, re.IGNORECASE):
        # If the query is selecting all columns (*), just pass
        if re.search(r"SELECT\s+\*\s+FROM", sql_query, re.IGNORECASE):
            return sql_query
        
        # If the query already contains 'ean' and 'url', just pass
        if re.search(r"\bean\b", sql_query, re.IGNORECASE) and re.search(r"\burl\b", sql_query, re.IGNORECASE):
            return sql_query
        
        # If 'ean' or 'url' are missing, add them with aliases '_ean' and '_url'
        if not re.search(r"\bean\b", sql_query, re.IGNORECASE):
            sql_query = re.sub(r"FROM", ", ean AS _ean FROM", sql_query, flags=re.IGNORECASE)
        if not re.search(r"\burl\b", sql_query, re.IGNORECASE):
            sql_query = re.sub(r"FROM", ", url AS _url FROM", sql_query, flags=re.IGNORECASE)

    return sql_query


def validate_and_correct_sql(sql, dialect="SQLite"):
    if dialect == "SQLite":
        # SQLite에서 INFORMATION_SCHEMA.COLUMNS 또는 information_schema.columns가 발견되면 PRAGMA로 변경
        if re.search(r"INFORMATION_SCHEMA\.COLUMNS", sql, re.IGNORECASE):
            table_name_match = re.search(r"TABLE_NAME\s*=\s*'(\w+)'", sql, re.IGNORECASE)
            if table_name_match:
                table_name = table_name_match.group(1)
                return f"PRAGMA table_info({table_name});"
        
        # SELECT COLUMN_NAME FROM pragma_table_info('table_name') 패턴 감지
        pragma_match = re.search(r"SELECT COLUMN_NAME FROM pragma_table_info\('(\w+)'\);", sql)
        if pragma_match:
            table_name = pragma_match.group(1)
            return f"PRAGMA table_info({table_name});"
    
    return sql


def natural_chat(message):
    messages = [
        {"role": "system", "content": "당신은 위키북스 AI 상담원입니다. 독자의 질문에 친절히 답합니다."},
    ]
