import sqlite3  # Импорт библиотеки для работы с SQLite базой данных
from datetime import datetime  # Импорт модуля для работы с датой и временем

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('space_shooter.db')  # Подключение к базе данных
        self.update_table_structure()  # Обновление структуры таблиц
        self.create_tables()  # Создание основных таблиц
        self.create_shop_tables()  # Создание таблиц для магазина

    def update_table_structure(self):
        cursor = self.conn.cursor()  # Создание курсора для выполнения SQL запросов
        try:
            cursor.execute("PRAGMA table_info(players)")  # Получение информации о структуре таблицы
            columns = [column[1] for column in cursor.fetchall()]  # Извлечение имен столбцов

            if 'photo' not in columns:  # Если столбца photo нет
                cursor.execute('ALTER TABLE players ADD COLUMN photo BLOB DEFAULT NULL')  # Добавляем столбец
                self.conn.commit()  # Сохранение изменений
                print("Структура таблицы обновлена - добавлен столбец photo")

        except Exception as e:
            print(f"Ошибка при обновлении структуры таблицы: {e}")

    def create_tables(self):
        cursor = self.conn.cursor()  # Создание курсора

        # Создание таблицы игроков в SQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                credits INTEGER DEFAULT 1000,
                level INTEGER DEFAULT 1,
                registration_date TEXT NOT NULL,
                photo BLOB DEFAULT NULL
            )
        ''')
        self.conn.commit()  # Сохранение изменений

    def register_player(self, login, password):
        cursor = self.conn.cursor()  # Создание курсора

        try:
            registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Текущая дата и время

            cursor.execute('''
                INSERT INTO players (login, password, credits, level, registration_date, photo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (login, password, 1000, 1, registration_date, None))

            self.conn.commit()  # Сохранение изменений
            return True, "Регистрация успешна!"  # Возврат успешного результата

        except sqlite3.IntegrityError:  # Ошибка если логин уже занят
            return False, "Логин уже занят!"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"

    def login_player(self, login, password):
        cursor = self.conn.cursor()  # Создание курсора

        cursor.execute('SELECT id, login, credits, level FROM players WHERE login = ? AND password = ?', (login, password))
        player = cursor.fetchone()  # Получение первой найденной записи

        if player:  # Если игрок найден
            return True, "Вход успешен!", player
        else:  # Если игрок не найден
            return False, "Неверный логин или пароль!", None

    def get_player_full_data(self, player_id):
        cursor = self.conn.cursor()  # Создание курсора

        cursor.execute('SELECT id, login, password, credits, level, registration_date, photo FROM players WHERE id = ?', (player_id,))
        player = cursor.fetchone()  # Получение записи
        return player  # Возврат данных игрока

    def add_credits(self, player_id, amount):
        cursor = self.conn.cursor()  # Создание курсора
        try:
            cursor.execute('UPDATE players SET credits = credits + ? WHERE id = ?', (amount, player_id))
            self.conn.commit()  # Сохранение изменений
            return True
        except Exception as e:
            print(f"Ошибка при добавлении монет: {e}")
            return False

    def add_level(self, player_id, levels=1):  # Добавить параметр levels
        cursor = self.conn.cursor()
        try:
            cursor.execute('UPDATE players SET level = level + ? WHERE id = ?', (levels, player_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при повышении уровня: {e}")
            return False

    def update_player_photo(self, player_id, photo_data):
        cursor = self.conn.cursor()  # Создание курсора
        try:
            cursor.execute('UPDATE players SET photo = ? WHERE id = ?', (photo_data, player_id))
            self.conn.commit()  # Сохранение изменений
            return True
        except Exception as e:
            print(f"Ошибка при обновлении фото: {e}")
            return False

    def get_player_photo(self, player_id):
        cursor = self.conn.cursor()  # Создание курсора
        try:
            cursor.execute('SELECT photo FROM players WHERE id = ?', (player_id,))
            result = cursor.fetchone()  # Получение результата
            return result[0] if result and result[0] else None  # Возврат фото или None
        except Exception as e:
            print(f"Ошибка при получении фото: {e}")
            return None

    def create_shop_tables(self):
        cursor = self.conn.cursor()  # Создание курсора

        # Создание таблицы товаров магазина
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shop_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price INTEGER NOT NULL,
                emoji TEXT NOT NULL,
                category TEXT NOT NULL,
                effect_type TEXT NOT NULL,
                effect_value INTEGER NOT NULL
            )
        ''')

        # Создание таблицы покупок игроков
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                purchase_date TEXT NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players (id),
                FOREIGN KEY (item_id) REFERENCES shop_items (id)
            )
        ''')

        self.conn.commit()  # Сохранение изменений
        self.initialize_shop_items()  # Заполнение магазина товарами

    def initialize_shop_items(self):
        cursor = self.conn.cursor()  # Создание курсора

        cursor.execute('SELECT COUNT(*) FROM shop_items')
        if cursor.fetchone()[0] == 0:  # Если товаров нет
            items = [
                ('Увеличение здоровья', '+50 к максимальному здоровью', 500, '❤️', 'player', 'health', 50),
                ('Ускорение бега', '+20% к скорости передвижения', 300, '⚡', 'player', 'speed', 20),
                ('Сильный прыжок', '+30% к силе прыжка', 250, '🦘', 'player', 'jump', 30),
                ('Усиленные пули', '+50% урона пуль', 600, '💥', 'weapon', 'damage', 50),
                ('Быстрая перезарядка', 'Скорострельность x2', 700, '🎯', 'weapon', 'fire_rate', 2),
                ('Тройной выстрел', 'Стреляет тремя пулями', 1000, '🔫', 'weapon', 'triple_shot', 1),
                ('Регенерация', '5 HP/сек когда стоишь', 900, '🛡️', 'bonus', 'regen', 5),
                ('Защитный щит', 'Бесплатный удар от босса', 750, '✨', 'bonus', 'shield', 1),
                ('Замедление времени', 'Замедляет босса на 5 сек', 1200, '⏰', 'bonus', 'slow_time', 5)
            ]

            for item in items:
                cursor.execute('INSERT INTO shop_items (name, description, price, emoji, category, effect_type, effect_value) VALUES (?, ?, ?, ?, ?, ?, ?)', item)

            self.conn.commit()  # Сохранение изменений
            print("Магазин заполнен товарами!")

    def get_shop_items(self, category=None):
        cursor = self.conn.cursor()  # Создание курсора

        if category:  # Если указана категория
            cursor.execute('SELECT * FROM shop_items WHERE category = ?', (category,))
        else:  # Если категория не указана
            cursor.execute('SELECT * FROM shop_items')

        return cursor.fetchall()  # Возврат всех найденных товаров

    def get_player_purchases(self, player_id):
        cursor = self.conn.cursor()  # Создание курсора
        cursor.execute('SELECT si.* FROM shop_items si JOIN player_purchases pp ON si.id = pp.item_id WHERE pp.player_id = ?', (player_id,))
        return cursor.fetchall()  # Возврат всех купленных товаров

    def purchase_item(self, player_id, item_id):
        cursor = self.conn.cursor()  # Создание курсора

        try:
            cursor.execute('SELECT price FROM shop_items WHERE id = ?', (item_id,))
            item_price = cursor.fetchone()[0]  # Извлечение цены

            cursor.execute('SELECT credits FROM players WHERE id = ?', (player_id,))
            player_credits = cursor.fetchone()[0]  # Извлечение баланса

            if player_credits >= item_price:  # Проверяем хватает ли денег
                cursor.execute('SELECT id FROM player_purchases WHERE player_id = ? AND item_id = ?', (player_id, item_id))

                if cursor.fetchone() is None:  # Если товар еще не куплен
                    cursor.execute('UPDATE players SET credits = credits - ? WHERE id = ?', (item_price, player_id))

                    purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute('INSERT INTO player_purchases (player_id, item_id, purchase_date) VALUES (?, ?, ?)', (player_id, item_id, purchase_date))

                    self.conn.commit()  # Сохранение изменений
                    return True, "Покупка успешна!"
                else:
                    return False, "Этот товар уже куплен!"
            else:
                return False, "Недостаточно монет!"

        except Exception as e:
            self.conn.rollback()  # Отмена изменений при ошибке
            return False, f"Ошибка при покупке: {str(e)}"

    def apply_item_effect(self, player_id, item_id):
        try:
            cursor = self.conn.cursor()  # Создание курсора
            cursor.execute('SELECT effect_type, effect_value FROM shop_items WHERE id = ?', (item_id,))
            result = cursor.fetchone()  # Получение результата

            if result:  # Если эффект найден
                effect_type, effect_value = result
                return True  # Возврат успеха
            return False  # Возврат ошибки

        except Exception as e:
            print(f"Ошибка при применении предмета: {e}")
            return False

    def close(self):
        self.conn.close()  # Закрытие соединения с базой данных