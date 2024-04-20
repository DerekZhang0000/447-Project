from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    query_string = request.form['query']
    connection = sqlite3.connect('boats.db')
    cursor = connection.cursor()
    cursor.execute(query_string)
    rows = cursor.fetchall()
    connection.close()
    return render_template('result.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)