from flask import Flask, render_template, request, jsonify
import database
import llm

app = Flask(__name__)

schemas = database.get_all_tables_schema()

@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/send_message', methods=['POST'])
def send_message():

    message = request.form.get('message')
    sql = generateSQL(message)
    result = getbooklist(sql)
    return jsonify({"message": result})


def generateSQL(natural_query):
    sql = llm.generateSQL(schemas, natural_query)
    if not sql:
        sql = "SELECT isbn, title, author, pubdate, url"
        sql += " FROM books"
        sql += " WHERE title LIKE '%" + natural_query + "%'"
        sql += " ORDER BY pubdate DESC;"
    return sql


@app.route('/generate_sql', methods=['POST'])
def generate_sql_endpoint():
    message = request.form.get('message')
    sql = generateSQL(message)
    return jsonify({"sql": sql})

@app.route('/execute_sql', methods=['POST'])
def execute_sql():
    sql = request.form.get('sql')
    return jsonify({"result": getbooklist(sql)})


def getbooklist(query):
    def linkify_column(value):
        return f'<a href="{value}">{value}</a>' if value else value

    def shorten(s):
        size = 50
        if len(s) > size:
            s = s[:size] + '...'
        return s

    def highlight_title(value):
        return f'⟪{value}⟫'

    def process_column(idx, col):
        if idx == title_column_index:
            return highlight_title(col)
        elif idx == url_column_index:
            return linkify_column(col)
        elif idx == pages_column_index:
            return f"{col}쪽"
        elif idx == price_column_index:
            return f"{col}원"
        else:
            return shorten(str(col))
    
    try:
        booklist, columns_desc = database.execute_select_query(query)

        if booklist:
            column_names = [desc[0] for desc in columns_desc]
            column_indices = {name: index for index, name in enumerate(column_names)}
            title_column_index = column_indices.get('title')
            url_column_index = column_indices.get('url')
            pages_column_index = column_indices.get('pages')
            price_column_index = column_indices.get('price')

            result = "<ol>"
        
            for row in booklist:
                result += "<li>" 
                result += ', '.join([process_column(idx, col) for idx, col in enumerate(row)])
                result += "</li>"
        
            result += "</ol>"
        else:
            result = "결과가 없습니다."
    except:
        result = "질의에 실패했습니다."

    return result

if __name__ == '__main__':
    app.run(debug=True)
