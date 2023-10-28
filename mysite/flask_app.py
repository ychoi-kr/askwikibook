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
    url_column_index = column_names.index('url')

    result += '<br><br>결과:<br>'
    result += "<ol>"

    def linkify_column(value):
        return f'<a href="{value}">{value}</a>' if value else value

    def shorten(s):
        size = 50
        if len(s) > size:
            s = s[:size] + '...'
        return s

    for row in booklist:
        result += "<li>"
        result += ', '.join([linkify_column(col) if idx == url_column_index else shorten(str(col)) for idx, col in enumerate(row)])
        result += "</li>"

    result += "</ol>"
    return result

if __name__ == '__main__':
    app.run(debug=True)
