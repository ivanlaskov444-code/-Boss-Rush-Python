import sys  # Импорт системных функций
from PyQt6 import QtWidgets, QtGui, QtCore  # Импорт компонентов PyQt6 для GUI
from start_ui import Ui_StartWindow  # Импорт интерфейса стартового окна
from register_ui import Ui_RegisterWindow  # Импорт интерфейса окна регистрации
from login_ui import Ui_EntranceWindow  # Импорт интерфейса окна входа
from database import Database  # Импорт класса для работы с базой данных
from main_menu_ui import Ui_MainMenuWindow  # Импорт интерфейса главного меню
from profile_ui import Ui_ProfileWindow  # Импорт интерфейса профиля
from game_engine import GameWindow  # Импорт игрового окна
from shop_ui import Ui_ShopWindow  # Импорт интерфейса магазина
from constants import * # Импортируем все константы

class ProfileWindow(QtWidgets.QMainWindow, Ui_ProfileWindow):
    def __init__(self, player_data, db, main_menu_window):
        super().__init__()  # Вызов конструктора родительского класса
        self.setupUi(self)  # Инициализация интерфейса из файла дизайнера
        self.player_data = player_data  # Сохранение данных игрока
        self.db = db  # Сохранение объекта базы данных
        self.main_menu_window = main_menu_window  # Сохранение ссылки на главное меню

        self.load_player_data()  # Загрузка данных игрока при создании окна

        self.select_photo_btn.clicked.connect(self.select_photo)  # Подключение кнопки выбора фото
        self.close_btn.clicked.connect(self.close_profile)  # Подключение кнопки закрытия

    def load_player_data(self):
        try:  # Начало блока обработки ошибок
            player_id = self.player_data[0]  # Получение ID игрока из данных
            full_player_data = self.db.get_player_full_data(player_id)  # Получение полных данных игрока из БД

            if full_player_data:  # Проверка что данные получены
                nickname = full_player_data[1]  # Извлечение ника игрока
                password = full_player_data[2]  # Извлечение пароля игрока
                credits = full_player_data[3]  # Извлечение количества монет
                level = full_player_data[4]  # Извлечение уровня игрока

                self.nickname_value.setText(nickname)  # Установка ника в интерфейс
                self.password_value.setText(password)  # Установка пароля в интерфейс
                self.credits_value.setText(UI_TEXTS['coins'].format(credits))  # Установка монет в интерфейс
                self.level_value.setText(UI_TEXTS['level'].format(level))  # Установка уровня в интерфейс

                photo_data = self.db.get_player_photo(player_id)  # Получение фото игрока из БД
                if photo_data:  # Проверка что фото существует
                    self.display_photo(photo_data)  # Отображение фото

        except Exception as e:  # Обработка исключений
            print(f"Ошибка при загрузке данных профиля: {e}")  # Вывод ошибки в консоль
            QtWidgets.QMessageBox.critical(self, WINDOW_TITLES['error'], UI_TEXTS['profile_load_error'])  # Показ ошибки пользователю

    def select_photo(self):
        try:  # Начало блока обработки ошибок
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                WINDOW_TITLES['select_photo'],
                "",
                FILE_FILTERS['images']
            )

            if file_path:  # Проверка что файл выбран
                with open(file_path, 'rb') as file:  # Открытие файла в бинарном режиме
                    photo_data = file.read()  # Чтение данных файла

                success = self.db.update_player_photo(self.player_data[0], photo_data)  # Сохранение фото в БД
                if success:  # Проверка успешности сохранения
                    self.display_photo(photo_data)  # Отображение нового фото
                else:  # Если сохранение не удалось
                    QtWidgets.QMessageBox.warning(self, WINDOW_TITLES['warning'], UI_TEXTS['photo_save_error'])  # Показ предупреждения

        except Exception as e:  # Обработка исключений
            print(f"Ошибка при выборе фото: {e}")  # Вывод ошибки в консоль
            QtWidgets.QMessageBox.critical(self, WINDOW_TITLES['error'], UI_TEXTS['photo_load_error'])  # Показ ошибки пользователю

    def display_photo(self, photo_data):
        try:  # Начало блока обработки ошибок
            pixmap = QtGui.QPixmap()  # Создание объекта изображения
            pixmap.loadFromData(photo_data)  # Загрузка изображения из данных

            scaled_pixmap = pixmap.scaled(  # Масштабирование изображения
                PHOTO_SIZE,  # Ширина
                PHOTO_SIZE,  # Высота
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,  # Сохранение пропорций
                QtCore.Qt.TransformationMode.SmoothTransformation  # Сглаживание
            )
            self.photo_label.setPixmap(scaled_pixmap)  # Установка изображения в метку

        except Exception as e:  # Обработка исключений
            print(f"Ошибка при отображении фото: {e}")  # Вывод ошибки в консоль
            self.photo_label.setText(UI_TEXTS['photo_error'])  # Установка текста ошибки

    def close_profile(self):
        self.close()  # Закрытие окна профиля

class MainMenuWindow(QtWidgets.QMainWindow, Ui_MainMenuWindow):
    def __init__(self, player_data, db):
        super().__init__()  # Вызов конструктора родительского класса
        self.setupUi(self)  # Инициализация интерфейса из файла дизайнера
        self.player_data = player_data  # Сохранение данных игрока
        self.db = db  # Сохранение объекта базы данных
        self.profile_window = None  # Инициализация переменной для окна профиля
        self.shop_window = None  # Инициализация переменной для окна магазина

        self.player_info_label.setText(UI_TEXTS['player'].format(player_data[1]))  # Установка информации об игроке
        self.play_btn.clicked.connect(self.start_game)  # Подключение кнопки начала игры
        self.shop_btn.clicked.connect(self.open_shop)  # Подключение кнопки магазина
        self.profile_btn.clicked.connect(self.open_profile)  # Подключение кнопки профиля
        self.exit_btn.clicked.connect(self.close)  # Подключение кнопки выхода

    def open_shop(self):
        try:  # Начало блока обработки ошибок
            self.shop_window = ShopWindow(self.player_data, self.db, self)  # Создание окна магазина
            self.shop_window.show()  # Показ окна магазина
        except Exception as e:  # Обработка исключений
            print(f"Ошибка при открытии магазина: {e}")  # Вывод ошибки в консоль
            QtWidgets.QMessageBox.critical(self, WINDOW_TITLES['error'], UI_TEXTS['shop_open_error'])  # Показ ошибки пользователю

    def start_game(self):
        self.game_window = GameWindow(self.player_data, self.db, self)  # Создание игрового окна
        self.game_window.show()  # Показ игрового окна
        self.close()  # Закрытие главного меню

    def open_profile(self):
        self.profile_window = ProfileWindow(self.player_data, self.db, self)  # Создание окна профиля
        self.profile_window.show()  # Показ окна профиля

class EntranceWindow(QtWidgets.QMainWindow, Ui_EntranceWindow):
    def __init__(self, start_window, db):
        super().__init__()  # Вызов конструктора родительского класса
        self.setupUi(self)  # Инициализация интерфейса из файла дизайнера
        self.start_window = start_window  # Сохранение ссылки на стартовое окно
        self.db = db  # Сохранение объекта базы данных
        self.error_label.hide()  # Скрытие метки ошибки
        self.create_account_btn.clicked.connect(self.handle_login)  # Подключение кнопки входа
        self.cancel_btn.clicked.connect(self.go_back)  # Подключение кнопки отмены

    def handle_login(self):
        login = self.login_input.text()  # Получение текста из поля логина
        password = self.password_input.text()  # Получение текста из поля пароля

        if not login or not password:  # Проверка заполнения полей
            self.error_label.setText(UI_TEXTS['fill_fields'])  # Установка текста ошибки
            self.error_label.show()  # Показ метки ошибки
            return  # Выход из функции

        success, message, player_data = self.db.login_player(login, password)  # Попытка входа в БД

        if success:  # Если вход успешен
            self.error_label.hide()  # Скрытие метки ошибки
            self.main_menu = MainMenuWindow(player_data, self.db)  # Создание главного меню
            self.main_menu.show()  # Показ главного меню
            self.close()  # Закрытие окна входа
        else:  # Если вход не удался
            self.error_label.setText(message)  # Установка текста ошибки
            self.error_label.show()  # Показ метки ошибки

    def go_back(self):
        self.start_window.show()  # Показ стартового окна
        self.close()  # Закрытие текущего окна

class RegisterWindow(QtWidgets.QMainWindow, Ui_RegisterWindow):
    def __init__(self, start_window, db):
        super().__init__()  # Вызов конструктора родительского класса
        self.setupUi(self)  # Инициализация интерфейса из файла дизайнера
        self.start_window = start_window  # Сохранение ссылки на стартовое окно
        self.db = db  # Сохранение объекта базы данных
        self.error_label.hide()  # Скрытие метки ошибки
        self.create_account_btn.clicked.connect(self.handle_register)  # Подключение кнопки регистрации
        self.cancel_btn.clicked.connect(self.go_back)  # Подключение кнопки отмены

    def handle_register(self):
        login = self.login_input.text()  # Получение текста из поля логина
        password = self.password_input.text()  # Получение текста из поля пароля
        confirm = self.confirm_password_input.text()  # Получение текста из поля подтверждения пароля

        if password != confirm:  # Проверка совпадения паролей
            self.error_label.setText(UI_TEXTS['passwords_not_match'])  # Установка текста ошибки
            self.error_label.show()  # Показ метки ошибки
            return  # Выход из функции

        if not login or not password:  # Проверка заполнения полей
            self.error_label.setText(UI_TEXTS['fill_fields'])  # Установка текста ошибки
            self.error_label.show()  # Показ метки ошибки
            return  # Выход из функции

        if len(login) < MIN_LOGIN_LENGTH:  # Проверка минимальной длины логина
            self.error_label.setText(UI_TEXTS['login_too_short'])  # Установка текста ошибки
            self.error_label.show()  # Показ метки ошибки
            return  # Выход из функции

        if len(password) < MIN_PASSWORD_LENGTH:  # Проверка минимальной длины пароля
            self.error_label.setText(UI_TEXTS['password_too_short'])  # Установка текста ошибки
            self.error_label.show()  # Показ метки ошибки
            return  # Выход из функции

        success, message = self.db.register_player(login, password)  # Попытка регистрации в БД

        if success:  # Если регистрация успешна
            self.error_label.hide()  # Скрытие метки ошибки
            QtWidgets.QMessageBox.information(self, UI_TEXTS['success'], UI_TEXTS['account_created'])  # Показ сообщения об успехе
            self.go_back()  # Возврат к стартовому окну
        else:  # Если регистрация не удалась
            self.error_label.setText(message)  # Установка текста ошибки
            self.error_label.show()  # Показ метки ошибки

    def go_back(self):
        self.start_window.show()  # Показ стартового окна
        self.close()  # Закрытие текущего окна

class StartWindow(QtWidgets.QMainWindow, Ui_StartWindow):
    def __init__(self, db):
        super().__init__()  # Вызов конструктора родительского класса
        self.setupUi(self)  # Инициализация интерфейса из файла дизайнера
        self.Login.clicked.connect(self.open_login)  # Подключение кнопки входа
        self.Register.clicked.connect(self.open_register)  # Подключение кнопки регистрации
        self.db = db  # Сохранение объекта базы данных

    def open_login(self):
        self.loginog_window = EntranceWindow(self, self.db)  # Создание окна входа
        self.loginog_window.show()  # Показ окна входа
        self.hide()  # Скрытие текущего окна

    def open_register(self):
        self.register_window = RegisterWindow(self, self.db)  # Создание окна регистрации
        self.register_window.show()  # Показ окна регистрации
        self.hide()  # Скрытие текущего окна

class ShopWindow(QtWidgets.QMainWindow, Ui_ShopWindow):
    def __init__(self, player_data, db, main_menu_window):
        super().__init__()  # Вызов конструктора родительского класса
        self.setupUi(self)  # Инициализация интерфейса из файла дизайнера
        self.player_data = player_data  # Сохранение данных игрока
        self.db = db  # Сохранение объекта базы данных
        self.main_menu_window = main_menu_window  # Сохранение ссылки на главное меню

        self.close_btn.clicked.connect(self.close_shop)  # Подключение кнопки закрытия
        self.close_btn.setStyleSheet(BUTTON_STYLE_SHEET)  # Установка стиля кнопки

        self.load_shop_items()  # Загрузка товаров магазина

    def load_shop_items(self):
        try:  # Начало блока обработки ошибок
            player_id = self.player_data[0]  # Получение ID игрока
            full_data = self.db.get_player_full_data(player_id)  # Получение полных данных игрока
            if full_data:  # Проверка что данные получены
                credits = full_data[3]  # Извлечение количества монет
                self.balance_label.setText(UI_TEXTS['balance'].format(credits))  # Установка баланса

            purchased_items = self.db.get_player_purchases(player_id)  # Получение купленных товаров
            purchased_ids = [item[0] for item in purchased_items]  # Создание списка ID купленных товаров

            categories = {  # Словарь категорий товаров
                'player': self.player_tab,  # Категория игрока
                'weapon': self.weapon_tab,  # Категория оружия
                'bonus': self.bonus_tab  # Категория бонусов
            }

            for category, tab in categories.items():  # Цикл по всем категориям
                self.setup_category_tab(category, tab, purchased_ids)  # Настройка вкладки категории

        except Exception as e:  # Обработка исключений
            print(f"Ошибка при загрузке магазина: {e}")  # Вывод ошибки в консоль

    def setup_category_tab(self, category, tab, purchased_ids):
        try:  # Начало блока обработки ошибок
            if tab.layout():  # Проверка существующего layout
                QtWidgets.QWidget().setLayout(tab.layout())  # Удаление старого layout

            layout = QtWidgets.QVBoxLayout(tab)  # Создание вертикального layout

            items = self.db.get_shop_items(category)  # Получение товаров категории

            for item in items:  # Цикл по всем товарам
                item_id, name, description, price, emoji, _, effect_type, effect_value = item  # Распаковка данных товара

                item_widget = QtWidgets.QWidget()  # Создание виджета товара
                item_layout = QtWidgets.QHBoxLayout(item_widget)  # Создание горизонтального layout

                emoji_label = QtWidgets.QLabel(emoji)  # Создание метки с эмодзи
                emoji_label.setFont(QtGui.QFont("Arial", FONT_SIZE_LARGE))  # Установка большого шрифта
                item_layout.addWidget(emoji_label)  # Добавление эмодзи в layout

                info_widget = QtWidgets.QWidget()  # Создание виджета информации
                info_layout = QtWidgets.QVBoxLayout(info_widget)  # Создание вертикального layout

                name_label = QtWidgets.QLabel(name)  # Создание метки названия
                name_label.setFont(QtGui.QFont("Arial", FONT_SIZE_MEDIUM, QtGui.QFont.Weight.Bold))  # Установка жирного шрифта
                info_layout.addWidget(name_label)  # Добавление названия в layout

                desc_label = QtWidgets.QLabel(description)  # Создание метки описания
                desc_label.setFont(QtGui.QFont("Arial", FONT_SIZE_SMALL))  # Установка малого шрифта
                info_layout.addWidget(desc_label)  # Добавление описания в layout

                price_label = QtWidgets.QLabel(UI_TEXTS['price'].format(price))  # Создание метки цены
                price_label.setFont(QtGui.QFont("Arial", FONT_SIZE_SMALL, QtGui.QFont.Weight.Bold))  # Установка жирного шрифта
                info_layout.addWidget(price_label)  # Добавление цены в layout

                item_layout.addWidget(info_widget)  # Добавление информации в layout товара

                buttons_widget = QtWidgets.QWidget()  # Создание виджета кнопок
                buttons_layout = QtWidgets.QVBoxLayout(buttons_widget)  # Создание вертикального layout

                if item_id in purchased_ids:  # Проверка куплен ли товар
                    buy_btn = QtWidgets.QPushButton(UI_TEXTS['bought'])  # Создание кнопки "Куплено"
                    buy_btn.setEnabled(False)  # Отключение кнопки
                    buy_btn.setStyleSheet("background-color: lightgray; color: black;")  # Установка серого стиля
                    buttons_layout.addWidget(buy_btn)  # Добавление кнопки в layout

                    apply_btn = QtWidgets.QPushButton(UI_TEXTS['apply'])  # Создание кнопки "Применить"
                    apply_btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")  # Установка зеленого стиля
                    apply_btn.clicked.connect(lambda checked, iid=item_id, btn=apply_btn: self.apply_item(iid, btn))  # Подключение функции
                    buttons_layout.addWidget(apply_btn)  # Добавление кнопки в layout
                else:  # Если товар не куплен
                    buy_btn = QtWidgets.QPushButton(UI_TEXTS['buy'])  # Создание кнопки "Купить"
                    buy_btn.setStyleSheet("background-color: blue; color: white; font-weight: bold;")  # Установка синего стиля
                    buy_btn.clicked.connect(lambda checked, iid=item_id, btn=buy_btn: self.buy_item(iid, btn))  # Подключение функции
                    buttons_layout.addWidget(buy_btn)  # Добавление кнопки в layout

                item_layout.addWidget(buttons_widget)  # Добавление кнопок в layout товара
                layout.addWidget(item_widget)  # Добавление товара в основной layout

                line = QtWidgets.QFrame()  # Создание разделительной линии
                line.setFrameShape(QtWidgets.QFrame.Shape.HLine)  # Установка горизонтальной линии
                line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)  # Установка стиля линии
                layout.addWidget(line)  # Добавление линии в layout

            tab.setLayout(layout)  # Установка layout для вкладки

        except Exception as e:  # Обработка исключений
            print(f"Ошибка при настройке вкладки {category}: {e}")  # Вывод ошибки в консоль

    def buy_item(self, item_id, buy_btn):
        try:  # Начало блока обработки ошибок
            player_id = self.player_data[0]  # Получение ID игрока
            success, message = self.db.purchase_item(player_id, item_id)  # Покупка товара в БД

            if success:  # Если покупка успешна
                buy_btn.setText(UI_TEXTS['bought'])  # Изменение текста кнопки
                buy_btn.setEnabled(False)  # Отключение кнопки
                buy_btn.setStyleSheet("background-color: lightgray; color: black;")  # Установка серого стиля

                apply_btn = QtWidgets.QPushButton("Применить")  # Создание кнопки "Применить"
                apply_btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")  # Установка зеленого стиля
                apply_btn.clicked.connect(lambda: self.apply_item(item_id, apply_btn))  # Подключение функции

                parent_widget = buy_btn.parent()  # Получение родительского виджета
                if parent_widget:  # Проверка существования родителя
                    layout = parent_widget.layout()  # Получение layout
                    if layout:  # Проверка существования layout
                        layout.addWidget(apply_btn)  # Добавление кнопки в layout

                self.update_balance()  # Обновление баланса

            else:  # Если покупка не удалась
                QtWidgets.QMessageBox.warning(self, WINDOW_TITLES['warning'], message)  # Показ предупреждения

        except Exception as e:  # Обработка исключений
            print(f"Ошибка при покупке: {e}")  # Вывод ошибки в консоль
            QtWidgets.QMessageBox.critical(self, WINDOW_TITLES['error'], UI_TEXTS['purchase_error'])  # Показ ошибки пользователю

    def apply_item(self, item_id, apply_btn):
        try:  # Начало блока обработки ошибок
            apply_btn.setText(UI_TEXTS['applied'])  # Изменение текста кнопки
            apply_btn.setEnabled(False)  # Отключение кнопки
            apply_btn.setStyleSheet("background-color: lightgray; color: black;")  # Установка серого стиля
        except Exception as e:  # Обработка исключений
            print(f"Ошибка при применении предмета: {e}")  # Вывод ошибки в консоль
            QtWidgets.QMessageBox.critical(self, WINDOW_TITLES['error'], UI_TEXTS['apply_error'])  # Показ ошибки пользователю

    def update_balance(self):
        try:  # Начало блока обработки ошибок
            player_id = self.player_data[0]  # Получение ID игрока
            full_data = self.db.get_player_full_data(player_id)  # Получение данных игрока
            if full_data:  # Проверка что данные получены
                credits = full_data[3]  # Извлечение количества монет
                self.balance_label.setText(f"Ваш баланс: {credits} монет")  # Обновление баланса
        except Exception as e:  # Обработка исключений
            print(f"Ошибка при обновлении баланса: {e}")  # Вывод ошибки в консоль

    def close_shop(self):
        self.close()  # Закрытие окна магазина

def main():
    app = QtWidgets.QApplication(sys.argv)  # Создание приложения
    db = Database()  # Создание объекта базы данных
    start_window = StartWindow(db)  # Создание стартового окна
    start_window.show()  # Показ стартового окна
    sys.exit(app.exec())  # Запуск главного цикла приложения

if __name__ == '__main__':
    main()  # Вызов главной функции