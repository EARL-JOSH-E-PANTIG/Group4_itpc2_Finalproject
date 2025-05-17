from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}


def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Database connection failed: {e}")
        return None


@app.route('/api/games', methods=['GET'])
def get_games():
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(games)


@app.route('/api/games/<string:title>', methods=['GET'])
def get_game(title):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM games WHERE title = %s", (title,))
    game = cursor.fetchone()
    cursor.close()
    connection.close()
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(game)


@app.route('/api/games', methods=['POST'])
def add_game():
    data = request.json
    required = ['title', 'platform', 'play_status', 'hours_played', 'rating']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO games (title, platform, play_status, hours_played, rating) VALUES (%s, %s, %s, %s, %s)",
            (data['title'], data['platform'], data['play_status'], data['hours_played'], data['rating'])
        )
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Game added successfully'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/games/<string:title>', methods=['PUT'])
def update_game(title):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        updates = []
        values = []
        for key in ['platform', 'play_status', 'hours_played', 'rating']:
            if key in data:
                updates.append(f"{key} = %s")
                values.append(data[key])
        if not updates:
            return jsonify({'error': 'No valid fields to update'}), 400
        values.append(title)

        cursor = connection.cursor()
        query = f"UPDATE games SET {', '.join(updates)} WHERE title = %s"
        cursor.execute(query, tuple(values))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Game not found'}), 404

        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Game updated successfully'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/games/<string:title>', methods=['DELETE'])
def delete_game(title):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM games WHERE title = %s", (title,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Game not found'}), 404
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Game deleted successfully'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)