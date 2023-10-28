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


def getbooklist(query):
    result = '질의: ' + query
    booklist, columns_desc = database.execute_query(query)
    column_names = [desc[0] for desc in columns_desc]
    title_column_index = column_names.index('title')
    url_column_index = column_names.index('url')
    pages_column_index = column_names.index('pages')
    price_column_index = column_names.index('price')

    result += '<br><br>결과:<br>'
    result += "<ol>"

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
    
    for row in booklist:
        result += "<li>" 
        result += ', '.join([process_column(idx, col) for idx, col in enumerate(row)])
        result += "</li>"

    result += "</ol>"
    return result

if __name__ == '__main__':
    app.run(debug=True)
