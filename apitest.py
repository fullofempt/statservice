from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)

# Создание таблицы для хранения данных, если она не существует
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        date DATE,
        other_info TEXT
    )
''')
conn.commit()
cur.close()

@app.route('/save_data', methods=['POST'])
def save_data():
    content = request.json
    name = content.get('name')
    date = content.get('date')
    other_info = content.get('other_info')

    cur = conn.cursor()
    cur.execute('''
        INSERT INTO data (name, date, other_info) VALUES (%s, %s, %s)
    ''', (name, date, other_info))
    conn.commit()
    cur.close()

    return jsonify({'message': 'Данные успешно сохранены'})

@app.route('/get_data', methods=['GET'])
def get_data():
    cur = conn.cursor()
    cur.execute('SELECT * FROM data')
    data = cur.fetchall()
    cur.close()

    data_list = []
    for row in data:
        data_list.append({
            'id': row[0],
            'name': row[1],
            'date': row[2].strftime('%Y-%m-%d'),
            'other_info': row[3]
        })

    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)
