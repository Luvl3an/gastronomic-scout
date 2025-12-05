import sqlite3


class Database:
    def __init__(self, db_path='restaurants.db'):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def search_restaurants(self, mood_keywords):
        """Поиск ресторанов по ключевым словам настроения"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Разбиваем ключевые слова
        keywords = [keyword.strip().lower() for keyword in mood_keywords.split(',')]
        keywords = [k for k in keywords if k]

        if not keywords:
            return []

        # Создаем условия для поиска
        conditions = []
        params = []

        for keyword in keywords:
            conditions.append('''
                (LOWER(name) LIKE ? OR 
                 LOWER(cuisine) LIKE ? OR 
                 LOWER(atmosphere) LIKE ? OR 
                 LOWER(description) LIKE ? OR
                 LOWER(tags) LIKE ?)
            ''')
            like_pattern = f'%{keyword}%'
            params.extend([like_pattern] * 5)

        where_clause = ' OR '.join(conditions)

        query = f'''
            SELECT * FROM restaurants 
            WHERE {where_clause}
            ORDER BY rating DESC
        '''

        cursor.execute(query, params)
        results = cursor.fetchall()

        # Преобразуем в словари
        restaurants = []
        for row in results:
            # Безопасная обработка тегов
            tags_str = str(row[10]) if row[10] is not None else ""
            tags_list = [tag.strip() for tag in tags_str.split(',')] if tags_str else []

            restaurant = {
                'id': row[0],
                'name': row[1],
                'cuisine': row[2],
                'price_range': row[3],
                'atmosphere': row[4],
                'description': row[5],
                'address': row[6],
                'latitude': float(row[7]) if row[7] is not None else 55.7558,
                'longitude': float(row[8]) if row[8] is not None else 37.6173,
                'rating': float(row[9]) if row[9] is not None else 0,
                'tags': tags_list
            }
            restaurants.append(restaurant)

        conn.close()
        return restaurants

    def get_all_restaurants(self):
        """Получить все рестораны"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM restaurants ORDER BY rating DESC')
        results = cursor.fetchall()

        restaurants = []
        for row in results:
            tags_str = str(row[10]) if row[10] is not None else ""
            tags_list = [tag.strip() for tag in tags_str.split(',')] if tags_str else []

            restaurant = {
                'id': row[0],
                'name': row[1],
                'cuisine': row[2],
                'price_range': row[3],
                'atmosphere': row[4],
                'description': row[5],
                'address': row[6],
                'latitude': float(row[7]) if row[7] is not None else 55.7558,
                'longitude': float(row[8]) if row[8] is not None else 37.6173,
                'rating': float(row[9]) if row[9] is not None else 0,
                'tags': tags_list
            }
            restaurants.append(restaurant)

        conn.close()
        return restaurants