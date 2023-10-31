import re

def validate_and_correct_sql(sql, dialect="SQLite"):
    if dialect == "SQLite":
        # SQLite에서 INFORMATION_SCHEMA.COLUMNS 또는 information_schema.columns가 발견되면 PRAGMA로 변경
        if re.search(r"INFORMATION_SCHEMA\.COLUMNS", sql, re.IGNORECASE):
            table_name_match = re.search(r"TABLE_NAME\s*=\s*'(\w+)'", sql, re.IGNORECASE)
            if table_name_match:
                table_name = table_name_match.group(1)
                return f"PRAGMA table_info({table_name});"
        
        # SELECT sql from sqlite_master WHERE type='table' AND name='table_name' 패턴 감지 및 변경
        sqlite_master_match = re.search(r"SELECT sql from sqlite_master WHERE type='table' AND name='(\w+)'", sql, re.IGNORECASE)
        if sqlite_master_match:
            table_name = sqlite_master_match.group(1)
            return f"PRAGMA table_info({table_name});"
        
        # SELECT COLUMN_NAME FROM pragma_table_info('table_name') 패턴 감지
        pragma_match = re.search(r"SELECT COLUMN_NAME FROM pragma_table_info\('(\w+)'\);", sql)
        if pragma_match:
            table_name = pragma_match.group(1)
            return f"PRAGMA table_info({table_name});"

        # LIMIT 절의 위치를 올바르게 조정하는 코드 추가
        if re.search(r"LIMIT \d+\s*ORDER BY", sql, re.IGNORECASE):
            # LIMIT 부분을 추출
            limit_match = re.search(r"LIMIT (\d+)", sql, re.IGNORECASE)
            if limit_match:
                limit_val = limit_match.group(1)
                # 원래의 LIMIT 부분과 마지막의 세미콜론 제거
                sql = re.sub(r"LIMIT \d+", "", sql, re.IGNORECASE).strip().rstrip(";")
                # ORDER BY 절 뒤에 LIMIT 부분을 추가하고 마지막에 세미콜론 추가
                sql = sql + f" LIMIT {limit_val};"
    
    return sql


def add_ean_and_url_columns(sql_query):
    """
    Add the 'ean' and 'url' columns to the SQL SELECT statement if they're not already present. 
    The resulting columns will be aliased as '_ean' and '_url'.
    """

    # Specific query pattern for series list: Do not add for this specific pattern
    series_list_query_pattern = r"^\s*SELECT\s+series\s+FROM\s+books\s+GROUP\s+BY\s+series"
    if re.match(series_list_query_pattern, sql_query, re.IGNORECASE):
        return sql_query

    # Check if the query contains 'DISTINCT', if so just pass
    if re.search(r"SELECT\s+DISTINCT", sql_query, re.IGNORECASE):
        if not re.search(r"SELECT DISTINCT.+title", sql_query, re.IGNORECASE):
            return sql_query
    
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


