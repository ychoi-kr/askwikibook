import re

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


def add_ean_and_url_columns(sql_query):
    """
    Add the 'ean' and 'url' columns to the SQL SELECT statement if they're not already present. 
    The resulting columns will be aliased as '_ean' and '_url'.
    """
    # Check if the query contains 'DISTINCT', if so just pass
    if re.search(r"SELECT\s+DISTINCT", sql_query, re.IGNORECASE):
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

