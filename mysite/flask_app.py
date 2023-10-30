from flask import Flask, render_template, request, jsonify
import database
import llm
import sql_utils

app = Flask(__name__)

schemas = database.get_all_tables_schema()

@app.route('/')
def index():
    return render_template('chat.html')


def generateSQL(natural_query):
    sql = llm.generateSQL(schemas, natural_query)
    if not sql:
        sql = "SELECT isbn, title, author, pubdate, url"
        sql += " FROM books"
        sql += " WHERE title LIKE '%" + natural_query + "%'"
        sql += " ORDER BY pubdate DESC;"
    
    validated_sql = sql_utils.validate_and_correct_sql(sql)

    return validated_sql


@app.route('/generate_sql', methods=['POST'])
def generate_sql_endpoint():
    message = request.form.get('message')
    validated_sql = generateSQL(message)
    return jsonify({"sql": validated_sql})


@app.route('/execute_sql', methods=['POST'])
def execute_sql():
    sql = request.form.get('sql')
    enhanced_sql = sql_utils.add_ean_and_url_columns(sql)
    result_data = getbooklist(enhanced_sql)

    if result_data["status"] == "failure":
        return jsonify({"result": f"<div class='error'>{result_data['message']}</div>"})

    elif not result_data["booklist"]:
        return jsonify({"result": f"<div class='no-result'>{result_data['message']}</div>"})

    else:
        ol_list = create_html_output(result_data)
        result_data["result"] = ol_list

    return jsonify(result_data)


def create_html_output(result_data):
    def linkify_column(value):
        return f'<a href="{value}">{value}</a>' if value else value
                
    def shorten(s, size=50):
        if len(s) > size:
            s = s[:size] + '...'
        return s
                
    def highlight_title(value):
        return f'⟪{value}⟫'
            
    column_indices = {name: index for index, name in enumerate(result_data['column_names'])}
    title_column_index = column_indices.get('title')
    url_column_index = column_indices.get('url')
    _url_column_index = column_indices.get('_url')
    pages_column_index = column_indices.get('pages')
    price_column_index = column_indices.get('price')
    ean_index = column_indices.get('ean')
    _ean_index = column_indices.get('_ean')
        
    list_items = []
    for row in result_data["booklist"]:
        thumbnail_html = ""
        # If 'ean' is not present, we check '_ean'
        ean = row[ean_index] if ean_index is not None and row[ean_index] else row[_ean_index] if _ean_index is not None else None
        # If 'url' is not present, we check '_url'
        url = row[url_column_index] if url_column_index is not None and row[url_column_index] else row[_url_column_index] if _url_column_index is not None else None
        
        if ean:
            thumbnail_url = f"https://wikibook.co.kr/images/cover/s/{ean}.jpg"
            if url:
                thumbnail_html = f'<a href="{url}"><img src="{thumbnail_url}" alt="Book cover" style="max-width: 50px; margin-right: 10px;"></a>'
            else:
                thumbnail_html = f'<img src="{thumbnail_url}" alt="Book cover" style="max-width: 50px; margin-right: 10px;">'
        
        # Process columns
        processed_values = []
        for idx, col in enumerate(row):
            col_value = ""
            if idx == title_column_index:
                col_value = highlight_title(col)
            elif idx == url_column_index:
                col_value = linkify_column(col)
            elif idx == pages_column_index:
                col_value = f"{col}쪽"
            elif idx == price_column_index:
                col_value = f"{col}원"
            elif idx in [_ean_index, _url_column_index]:  # Skip the enhanced _EAN and _URL values
                continue
            else:
                col_value = shorten(str(col))
            
            processed_values.append(col_value)
        
        list_items.append('<li>' + thumbnail_html + ', '.join(processed_values) + '</li>')

    return "<ol>" + ''.join(list_items) + "</ol>"


def getbooklist(query):
    try:
        booklist, columns_desc = database.execute_select_query(query)

        if booklist:
            column_names = [desc[0] for desc in columns_desc]
            return {
                "status": "success",
                "booklist": booklist,
                "column_names": column_names
            }
        else:
            return {
                "status": "success",
                "message": "결과가 없습니다.",
                "booklist": [],
                "column_names": []
            }
    except:
        return {
            "status": "failure",
            "message": f"질의에 실패했습니다. {str(e)}",
            "booklist": [],
            "column_names": []
        }

    return result

if __name__ == '__main__':
    app.run(debug=True)
