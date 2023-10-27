import sqlite3

DATABASE_PATH = "/home/askwikibook/databases/books.db"

def execute_query(query):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    num_columns = len(cursor.description)
    return result, num_columns

def get_books_schema():
    columns, _ = execute_query("PRAGMA table_info(books);")
    return ',\n'.join([' '.join([column[1], column[2]]) for column in columns])

def get_all_tables_schema():
    # 모든 테이블 이름 얻기
    tables_data, _ = execute_query("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [table[0] for table in tables_data]

    all_schemas = {}

    # 각 테이블에 대한 스키마 얻기
    for table_name in table_names:
        columns, _ = execute_query(f"PRAGMA table_info({table_name});")
        schema = ',\n'.join([' '.join([column[1], column[2]]) for column in columns])
        all_schemas[table_name] = schema

    return all_schemas