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
    booklist, num_columns = database.execute_query(query)

    result += '<br><br>결과:<br>'
    result += "<ol>"

    def shorten(s):
        size = 50
        if len(s) > size:
            s = s[:size] + '...'
        return s

    for row in booklist:
        result += "<li>" + ', '.join([shorten(str(col)) for col in row]) + "</li>"

    result += "</ol>"
    return result

if __name__ == '__main__':
    app.run(debug=True)
