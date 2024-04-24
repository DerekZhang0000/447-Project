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

@app.route('/get_military_ships', methods=['GET'])
def get_military_ships():
    connection = sqlite3.connect('boats.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT *
                      FROM 'Military Ship'""")
    rows = cursor.fetchall()
    connection.close()
    return render_template('result.html', rows=rows)

@app.route('/count_military_ships_by_builder', methods=['GET'])
def count_military_ships_by_builder():
    connection = sqlite3.connect('boats.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT b.'Company Name', COUNT(ms.'Ship Name')
                      FROM 'Military Ship' AS ms
                      JOIN Builder b ON ms.Builder = b.'Company Name'
                      GROUP BY b.'Company Name'""")
    rows = cursor.fetchall()
    connection.close()
    return render_template('result.html', rows=rows)


@app.route('/list_all_ships_and_dates', methods=['GET'])
def list_all_ships_and_dates():
    connection = sqlite3.connect('boats.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT s.'Ship Name', COALESCE(s.'Construction Date', ms.'Construction Date') AS 'Construction Date'
                      FROM Ship AS s
                      LEFT JOIN 'Military Ship' AS ms ON s.'Ship Name' = ms.'Ship Name'
                      UNION
                      SELECT ms.'Ship Name', ms.'Construction Date'
                      FROM 'Military Ship' AS ms
                      WHERE ms.'Ship Name' NOT IN (SELECT s.'Ship Name' FROM Ship s)""")
    rows = cursor.fetchall()
    connection.close()
    return render_template('result.html', rows=rows)


@app.route('/query_specific_location', methods=['POST'])
def query_specific_location():
    location = request.form['location']
    connection = sqlite3.connect('boats.db')
    cursor = connection.cursor()
    cursor.execute(f"""SELECT ms.'Ship Name', Builder
                       FROM 'Military Ship' AS ms
                       WHERE ms.'Deployment Location' = '{location}'""")
    rows = cursor.fetchall()
    connection.close()
    return render_template('result.html', rows=rows)

@app.route('/query_specific_date', methods=['POST'])
def query_specific_date():
    date = request.form['date']
    connection = sqlite3.connect('boats.db')
    cursor = connection.cursor()
    cursor.execute(f"""SELECT ms.'Ship Name', Type
                       FROM 'Military Ship' AS ms
                       WHERE ms.'Commission Date' = '{date}'""")
    rows = cursor.fetchall()
    connection.close()
    return render_template('result.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)