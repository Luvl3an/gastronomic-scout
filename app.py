from flask import Flask, render_template, request, jsonify
from database import Database
import os

app = Flask(__name__)
db = Database()

MOOD_CATEGORIES = {
    'романтика': ['романтичная', 'ужин', 'вино', 'свечи', 'тихая'],
    'быстро': ['быстрая', 'обед', 'бургеры', 'студенты', 'перекус'],
    'компания': ['дружеская', 'вечеринки', 'пиво', 'молодежь', 'шумная'],
    'семья': ['семейная', 'дети', 'традиции', 'уютно', 'обед'],
    'работа': ['работа', 'встречи', 'кофе', 'бесплатный wi-fi', 'тихая'],
    'экзотика': ['экзотичная', 'восток', 'азия', 'необычно', 'приключения'],
    'премиум': ['высокий', 'вип', 'дорого', 'роскошно', 'особый']
}

@app.route('/')
def index():
    return render_template('index.html', mood_categories=MOOD_CATEGORIES)

@app.route('/search', methods=['POST'])
def search_restaurants():
    try:
        data = request.get_json()
        mood_text = data.get('mood', '').strip().lower()

        if not mood_text:
            return jsonify({'error': 'Введите описание настроения'}), 400

        # Ищем рестораны по ключевым словам
        restaurants = db.search_restaurants(mood_text)

        return jsonify({
            'success': True,
            'results': restaurants,
            'count': len(restaurants)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/restaurants')
def get_all_restaurants():
    try:
        restaurants = db.get_all_restaurants()
        return jsonify({
            'success': True,
            'results': restaurants,
            'count': len(restaurants)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/mood-suggestions')
def get_mood_suggestions():
    """Возвращает подсказки для настроений"""
    suggestions = list(MOOD_CATEGORIES.keys())
    return jsonify({'suggestions': suggestions})

# Проверяем базу данных
if not os.path.exists('restaurants.db'):
    print("Инициализация базы данных...")
    from init_db import init_database
    init_database()

app.run(debug=True, host='0.0.0.0', port=5000)