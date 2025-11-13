import os
import sys
import random
import traceback
from PyQt6 import QtWidgets, QtCore, QtGui
from constants import *  # Импортируем все константы
from sound_manager import SoundManager
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.multimedia.*=false' # Перенаправляем stderr чтобы скрыть ошибки FFmpeg

"""Основной класс игрового окна"""
class GameWindow(QtWidgets.QMainWindow):

    def __init__(self, player_data, db, main_menu_window=None):
        super().__init__()
        self.player_data = player_data  # Данные игрока из БД
        self.db = db  # Для работы с БД
        self.main_menu_window = main_menu_window  # Ссылка на главное меню
        self.sound_manager = SoundManager()

        try:
            self.initialize_game_state()  # Настройка состояния игры
            self.setup_game_window()  # Настройка окна
            self.create_game_scene()  # Создание игровой сцены
            self.create_game_objects()  # Создание игровых объектов
            self.setup_ui_elements()  # Настройка UI
            self.setup_game_mechanics()  # Настройка механик
            self.show()  # Показать окно
        except Exception as e:
            self.handle_critical_error("Создание игрового окна", e)

    def initialize_game_state(self):
        """Настройка начального состояния игры"""
        # Состояние игрока
        self.player_alive = True  # Флаг, что игрок жив
        self.player_health = PLAYER_MAX_HEALTH  # Текущее здоровье игрока
        self.player_max_health = PLAYER_MAX_HEALTH  # Максимальное здоровье игрока

        # Состояние босса
        self.boss_alive = True  # Флаг, что босс жив
        self.boss_health = BOSS_MAX_HEALTH  # Текущее здоровье босса
        self.boss_max_health = BOSS_MAX_HEALTH  # Максимальное здоровье босса

        # Игровые флаги
        self.game_paused = False  # Флаг паузы игры
        self.Examination_level_update = False  # Флаг проверки обновления уровня

        # Состояния управления игроком
        self.moving_left = False  # Флаг движения влево клавиша A
        self.moving_right = False  # Флаг движения вправо клавиша D
        self.is_walking = False  # Флаг ходьбы анимация
        self.facing_right = True  # Направление взгляда игрока (True - направо, False - налево)
        self.is_jumping = False  # Флаг прыжка игрока
        self.player_velocity_y = 0  # Вертикальная скорость игрока для гравитации
        self.on_ground = True  # Флаг, что игрок стоит на земле, платформе
        self.jump_buffer = 0  # Счетчик буфера прыжка
        self.jump_buffer_max = PLAYER_JUMP_BUFFER_MAX  # Максимальное значение буфера прыжка

        # Система пуль
        self.bullets = []  # Список для хранения всех пуль на экране
        self.bullet_cooldown = 0  # Таймер перезарядки между выстрелами
        self.bullet_cooldown_max = BULLET_COOLDOWN_MAX  # Максимальное время перезарядки
        self.bullet_damage = BULLET_DAMAGE  # Урон одной пули

        # Система босса
        self.boss_direction = 1  # Направление движения босса (1 - вправо, -1 - влево)
        self.boss_move_range_left = BOSS_MOVE_RANGE_LEFT  # Левая граница движения босса
        self.boss_move_range_right = BOSS_MOVE_RANGE_RIGHT  # Правая граница движения босса
        self.boss_facing_right = True  # Направление взгляда босса (True - направо, False - налево)
        self.boss_damage = BOSS_DAMAGE  # Урон босса при столкновении
        self.boss_damage_cooldown = 0  # Таймер перезарядки урона босса
        self.boss_damage_cooldown_max = BOSS_DAMAGE_COOLDOWN_MAX  # Максимальное время перезарядки урона

        # Физика босса
        self.boss_velocity_y = 0  # Вертикальная скорость босса для гравитации
        self.boss_on_ground = False  # Флаг, что босс стоит на земле, платформе
        self.boss_jump_cooldown = 0  # Таймер перезарядки прыжка босса
        self.boss_jump_cooldown_max = BOSS_JUMP_COOLDOWN_MAX  # Максимальное время перезарядки прыжка
        self.boss_jump_power = BOSS_JUMP_POWER  # Сила прыжка босса

        # Навигация босса
        self.boss_target_x = None  # Целевая позиция X для босса
        self.boss_target_y = None  # Целевая позиция Y для босса
        self.boss_state = "chasing"  # Текущее состояние босса ("chasing" - преследование)
        self.boss_navigation_timer = 0  # Таймер для обновления навигации босса
        self.boss_navigation_interval = BOSS_NAVIGATION_INTERVAL  # Интервал обновления навигации (из констант)
        self.boss_last_platform = None  # Последняя платформа, на которой был босс
        self.boss_stuck_timer = 0  # Таймер застревания босса
        self.boss_max_stuck_time = BOSS_MAX_STUCK_TIME  # Максимальное время застревания



    def setup_game_window(self):
        """Настройка основного окна игры"""
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)  # Фиксированный размер окна
        self.center_window()  # Центрирование окна на экране
        self.setWindowTitle("Boss Rush")
        self.setStyleSheet("background-color: black;")  # Черный фон окна

    def center_window(self):
        """Центрирование окна на экране"""
        try:
            screen = QtWidgets.QApplication.primaryScreen()  # Получение информации об экране
            screen_rect = screen.availableGeometry()  # Получаем геометрию экрана
            x = (screen_rect.width() - WINDOW_WIDTH) // 2  # Расчет позиции X для центрирования
            y = (screen_rect.height() - WINDOW_HEIGHT) // 2  # Расчет позиции Y для центрирования
            self.move(x, y)  # Перемещение окна в рассчитанную позицию
        except Exception as e:
            print(f"Ошибка при центрировании окна: {e}")

    def create_game_scene(self):
        """Создание игровой сцены"""
        self.game_scene = QtWidgets.QGraphicsScene()  # Создание объекта QGraphicsScene
        self.game_scene.setSceneRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)  # Установка размеров сцены
        self.game_scene.setBackgroundBrush(QtGui.QColor(0, 0, 0))  # Установка черного цвета фона сцены

        self.game_view = QtWidgets.QGraphicsView(self.game_scene)  # Создание вида для отображения сцены
        self.game_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Отключение горизонтальной полосы прокрутки
        self.game_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Отключение вертикальной полосы прокрутки
        self.setCentralWidget(self.game_view)  # Установка вида как центрального виджета

        self.game_view.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)  # Разрешаем игровому полю реагировать на нажатия клавиш
        self.game_view.setFocus()  # Передаем фокус на игровое поле

    def setup_game_mechanics(self):
        """Настройка игровой механики"""
        self.setup_timers()
        self.prev_player_y = self.player.y() if hasattr(self, 'player') else 0
        self.initialize_platform_map()

    def setup_timers(self):
        """Настройка игровых таймеров"""
        # Основной игровой таймер
        self.game_timer = QtCore.QTimer()
        self.game_timer.timeout.connect(self.game_loop)  # При срабатывании вызывает game_loop
        self.game_timer.start(16)  # 60 кадров в секунду

        # Таймер анимации игрока меняет кадры ходьбы
        self.animation_timer = QtCore.QTimer()
        self.animation_timer.timeout.connect(self.update_animation)  # Вызывает смену кадра
        self.animation_timer.start(200)  # 5 кадров в секунду

        # Таймер анимации босса
        self.boss_animation_timer = QtCore.QTimer()
        self.boss_animation_timer.timeout.connect(self.update_boss_animation)  # Вызывает смену кадра
        self.boss_animation_timer.start(16)  # 60 кадров в секунду

    def handle_critical_error(self, context, error):
        """Показывает сообщение об ошибке и выходит из игры"""
        error_msg = f"Критическая ошибка в {context}: {str(error)}"
        print(error_msg)  # Печатаем в консоль
        traceback.print_exc()  # Печатаем полную ошибку

        # Показываем окно с ошибкой пользователю
        QtWidgets.QMessageBox.critical(
            None,  # Без родительского окна
            "Критическая ошибка",  # Заголовок окна
            f"Не удалось запустить игру: {str(error)}"  # Текст ошибки
        )

    def create_game_objects(self):
        """Создание игровых объектов"""
        self.create_environment()  # Создание пол, платформы
        self.load_game_assets()  # Загрузка картинок
        self.create_characters()  # Создание игрока, босса

    def create_environment(self):
        """Создание игрового окружения"""
        self.create_floor()  # Создание пола
        self.create_platforms()  # Создание платформ

    def create_floor(self):
        """Создание пола"""
        line_height = 43  # Высота линии пола
        self.floor_line = QtWidgets.QGraphicsRectItem(0, 0, WINDOW_WIDTH, line_height)  # Создание прямоугольника для пола
        self.floor_line.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 0)))  # Установка желтого цвета пола

        floor_y = WINDOW_HEIGHT - line_height  # Расчет Y координаты пола
        self.floor_line.setPos(0, floor_y)  # Устанавливаем позицию пола на сцене
        self.game_scene.addItem(self.floor_line)  # Добавляем пол на сцену
        self.FLOOR_Y = floor_y  # Сохранение Y координаты пола

    def create_platforms(self):
        """Создание платформ"""
        self.platforms = []  # Пустой список для хранения платформ

        # Используем данные из констант PLATFORMS_DATA
        for platform_data in PLATFORMS_DATA:  # Перебираем данные платформ из констант
            x, y, width, height = platform_data  # Распаковываем данные платформы
            platform = self.create_single_platform(x, y, width, height)  # Создаем платформу
            self.platforms.append(platform)  # Добавляем созданную платформу в список

    def create_single_platform(self, x, y, width, height):
        """Создание одной платформы"""
        platform = QtWidgets.QGraphicsRectItem(0, 0, width, height)  # Создание прямоугольника для платформы
        color = QtGui.QColor(200, 200, 100)  # Желтоватый цвет

        platform.setBrush(QtGui.QBrush(color))  # Установка цвета заливки платформы
        platform.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 2))  # Создаем белую рамку толщиной 2 пикселя
        platform.setPos(x, y)  # Установка позиции платформы на сцене
        self.game_scene.addItem(platform)  # Добавление платформы на сцену
        return platform  # Возврат созданной платформы

    def setup_game_window(self):
        """Настройка основного окна игры"""
        self.setFixedSize(WINDOW_WIDTH,
                          WINDOW_HEIGHT)  # Устанавливаем фиксированный размер окна (ширина и высота из констант)
        self.center_window()  # Вызываем метод для центрирования окна на экране
        self.setWindowTitle("Boss Rush")  # Устанавливаем заголовок окна
        self.setStyleSheet("background-color: black;")  # Устанавливаем черный цвет фона окна через CSS

    def center_window(self):
        """Центрирование окна на экране"""
        try:
            screen = QtWidgets.QApplication.primaryScreen()  # Получаем информацию об основном экране
            screen_rect = screen.availableGeometry()  # Получаем прямоугольник доступной геометрии экрана
            x = (screen_rect.width() - WINDOW_WIDTH) // 2  # Вычисляем координату X для центрирования окна
            y = (screen_rect.height() - WINDOW_HEIGHT) // 2  # Вычисляем координату Y для центрирования окна
            self.move(x, y)  # Перемещаем окно в вычисленную позицию
        except Exception as e:
            print(f"Ошибка при центрировании окна: {e}")  # Выводим ошибку в консоль если что-то пошло не так

    def create_game_scene(self):
        """Создание игровой сцены"""
        self.game_scene = QtWidgets.QGraphicsScene()  # Создаем объект сцены для размещения графических элементов
        self.game_scene.setSceneRect(0, 0, WINDOW_WIDTH,
                                     WINDOW_HEIGHT)  # Устанавливаем размеры сцены
        self.game_scene.setBackgroundBrush(QtGui.QColor(0, 0, 0))  # Устанавливаем черный цвет фона сцены

        self.game_view = QtWidgets.QGraphicsView(self.game_scene)  # Создаем вид view для отображения сцены
        self.game_view.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Отключаем горизонтальную полосу прокрутки
        self.game_view.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Отключаем вертикальную полосу прокрутки
        self.setCentralWidget(self.game_view)  # Устанавливаем вид как центральный виджет главного окна

        self.game_view.setFocusPolicy(
            QtCore.Qt.FocusPolicy.StrongFocus)  # Устанавливаем политику фокуса для обработки клавиатуры
        self.game_view.setFocus()  # Устанавливаем фокус на вид, чтобы он мог получать события клавиатуры

    def create_game_objects(self):
        """Создание игровых объектов"""
        self.create_environment()  # Вызываем метод создания игрового окружения
        self.load_game_assets()  # Вызываем метод загрузки игровых ресурсов (картинки)
        self.create_characters()  # Вызываем метод создания персонажей (игрок и босс)

    def create_environment(self):
        """Создание игрового окружения"""
        self.create_floor()  # Вызываем метод создания пола
        self.create_platforms()  # Вызываем метод создания платформ

    def create_floor(self):
        """Создание пола"""
        line_height = 43  # Задаем высоту линии пола в пикселях
        self.floor_line = QtWidgets.QGraphicsRectItem(0, 0, WINDOW_WIDTH,
                                                      line_height)  # Создаем прямоугольный элемент для пола
        self.floor_line.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 0)))  # Устанавливаем желтый цвет заливки для пола

        floor_y = WINDOW_HEIGHT - line_height  # Вычисляем Y-координату пола внизу окна
        self.floor_line.setPos(0, floor_y)  # Устанавливаем позицию пола на сцене
        self.game_scene.addItem(self.floor_line)  # Добавляем пол на игровую сцену
        self.FLOOR_Y = floor_y  # Сохраняем Y-координату пола в переменную

    def create_platforms(self):
        """Создание платформ"""
        self.platforms = []  # Создаем пустой список для хранения всех платформ
        # Данные для создания платформ: кортежи (x, y, width, height)
        platforms_data = [
            (200, 600, 300, 20), (600, 600, 200, 20), (100, 500, 200, 20),  # Три платформы с координатами и размерами
            (500, 500, 150, 20), (800, 500, 180, 20), (300, 400, 250, 20),  # Еще три платформы
            (650, 400, 120, 20), (150, 300, 180, 20), (500, 300, 200, 20),  # Еще три платформы
            (800, 300, 150, 20), (350, 200, 100, 20), (700, 200, 120, 20),  # Последние три платформы
        ]

        # Создание каждой платформы по данным из списка
        for x, y, width, height in platforms_data:  # Перебираем каждый кортеж с данными платформы
            platform = self.create_single_platform(x, y, width, height)  # Вызываем метод создания одной платформы
            self.platforms.append(platform)  # Добавляем созданную платформу в список

    def create_single_platform(self, x, y, width, height):
        """Создание одной платформы"""
        platform = QtWidgets.QGraphicsRectItem(0, 0, width, height)  # Создаем прямоугольный элемент для платформы
        color = QtGui.QColor(200, 200, 100)  # Создаем цвет для платформы желтоватый

        platform.setBrush(QtGui.QBrush(color))  # Устанавливаем цвет заливки платформы
        platform.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 2))  # Устанавливаем белую рамку толщиной 2 пикселя
        platform.setPos(x, y)  # Устанавливаем позицию платформы на сцене
        self.game_scene.addItem(platform)  # Добавляем платформу на игровую сцену
        return platform  # Возвращаем созданную платформу

    def load_game_assets(self):
        """Загрузка игровых ресурсов"""
        self.load_player_animations()  # Вызываем метод загрузки анимаций игрока
        self.load_bullet_image()  # Вызываем метод загрузки изображения пули
        self.load_boss_animations()  # Вызываем метод загрузки анимаций босса

    def load_player_animations(self):
        """Загрузка анимаций игрока"""
        self.walk_frames = []  # Создаем пустой список для кадров анимации ходьбы
        self.current_frame = 0  # Устанавливаем текущий кадр анимации начальный кадр
        self.is_walking = False  # Флаг, указывающий идет ли игрок для анимации
        self.facing_right = True  # Флаг, указывающий направление взгляда игрока вправо

        assets_loaded = False  # Флаг, указывающий были ли загружены ресурсы

        for filename in PLAYER_IMAGES:  # Перебираем все имена файлов с изображениями игрока
            filepath = os.path.join(SOURCES_DIR, filename)  # Формируем полный путь к файлу
            if os.path.exists(filepath):  # Проверяем существует ли файл
                try:
                    pixmap = QtGui.QPixmap(filepath)  # Загружаем изображение из файла
                    pixmap = pixmap.scaled(PLAYER_SPRITE_WIDTH,  PLAYER_SPRITE_HEIGHT,
                                           QtCore.Qt.AspectRatioMode.KeepAspectRatio)  # Масштабируем изображение
                    self.walk_frames.append(pixmap)  # Добавляем кадр в список анимации
                    assets_loaded = True  # Устанавливаем флаг что ресурсы загружены
                except Exception as e:
                    print(f"Ошибка загрузки {filepath}: {e}")  # Выводим ошибку если загрузка не удалась
            else:
                print(f"Файл не найден: {filepath}")  # Сообщаем если файл не найден

        if not assets_loaded:  # Если ни один файл не загрузился
            self.create_fallback_player_animation()  # Создаем запасную анимацию

    def create_fallback_player_animation(self):
        """Создание запасной анимации игрока"""
        self.walk_frames = []  # Создаем пустой список для кадров анимации
        colors = [  # Список цветов для запасной анимации
            QtGui.QColor(255, 255, 255), QtGui.QColor(200, 200, 255),  # Белый и светло-синий
            QtGui.QColor(255, 255, 255), QtGui.QColor(255, 200, 200)  # Белый и светло-красный
        ]

        for color in colors:  # Перебираем все цвета в списке
            pixmap = QtGui.QPixmap(60, 80)  # Создаем пустое изображение размером 60x80
            pixmap.fill(color)  # Заполняем изображение текущим цветом
            self.walk_frames.append(pixmap)  # Добавляем созданное изображение в список анимации

    def load_boss_animations(self):
        """Загрузка анимаций босса"""
        self.boss_frames = []  # Создаем пустой список для кадров анимации босса
        self.boss_current_frame = 0  # Устанавливаем текущий кадр анимации босса (начальный кадр)
        self.boss_animation_counter = 0  # Счетчик для управления скоростью анимации босса
        self.boss_facing_right = True  # Флаг, указывающий направление взгляда босса (вправо)

        boss_loaded = False  # Флаг, указывающий были ли загружены ресурсы босса

        for boss_file in BOSS_IMAGES:  # Перебираем все имена файлов с изображениями босса
            filepath = os.path.join(SOURCES_DIR, boss_file)  # Формируем полный путь к файлу босса
            if os.path.exists(filepath):  # Проверяем существует ли файл
                try:
                    pixmap = QtGui.QPixmap(filepath)  # Загружаем изображение босса из файла
                    pixmap = pixmap.scaled(100, 120,
                                           QtCore.Qt.AspectRatioMode.KeepAspectRatio)  # Масштабируем изображение босса
                    self.boss_frames.append(pixmap)  # Добавляем кадр в список анимации босса
                    boss_loaded = True  # Устанавливаем флаг, что ресурсы босса загружены
                except Exception as e:
                    print(f"Ошибка загрузки {filepath}: {e}")  # Выводим ошибку если загрузка не удалась
            else:
                print(f"Файл не найден: {filepath}")  # Сообщаем если файл босса не найден

        if not boss_loaded:  # Если ни один файл босса не загрузился
            self.create_fallback_boss_animation()  # Создаем запасную анимацию босса

    def create_fallback_boss_animation(self):
        """Создание запасной анимации босса"""
        self.boss_frames = []  # Создаем пустой список для кадров анимации босса
        for i in range(3):  # Создаем 3 кадра анимации
            pixmap = QtGui.QPixmap(100, 120)  # Создаем пустое изображение размером 100x120 для босса
            color = QtGui.QColor(200 + i * 10, 0, 0)  # Создаем цвет с небольшим изменением для каждого кадра
            pixmap.fill(color)  # Заполняем изображение созданным цветом

            painter = QtGui.QPainter(pixmap)  # Создаем объект для рисования на изображении
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 0)))  # Устанавливаем желтый цвет для глаз
            painter.drawEllipse(30, 40, 15, 15)  # Рисуем левый глаз
            painter.drawEllipse(55, 40, 15, 15)  # Рисуем правый глаз

            painter.setBrush(QtGui.QBrush(QtGui.QColor(100, 0, 0)))  # Устанавливаем темно-красный цвет для рта
            painter.drawEllipse(40, 70, 20, 10)  # Рисуем рот

            painter.setBrush(QtGui.QBrush(QtGui.QColor(150, 0, 0)))  # Устанавливаем красный цвет для рук
            if i == 1:  # Для второго кадра анимации
                painter.drawRect(25, 100, 15, 20)  # Рисуем левую руку в одном положении
                painter.drawRect(60, 110, 15, 10)  # Рисуем правую руку в одном положении
            elif i == 2:  # Для третьего кадра анимации
                painter.drawRect(25, 110, 15, 10)  # Рисуем левую руку в другом положении
                painter.drawRect(60, 100, 15, 20)  # Рисуем правую руку в другом положении
            else:  # Для первого кадра анимации
                painter.drawRect(25, 110, 15, 10)  # Рисуем левую руку в нейтральном положении
                painter.drawRect(60, 110, 15, 10)  # Рисуем правую руку в нейтральном положении
            painter.end()  # Заканчиваем рисование
            self.boss_frames.append(pixmap)  # Добавляем созданное изображение в список анимации босса

    def load_bullet_image(self):
        """Загрузка изображения пули"""
        self.bullet_pixmap = None  # Инициализируем переменную для изображения пули как None

        filepath = os.path.join(SOURCES_DIR, BULLET_IMAGE)  # Формируем полный путь к файлу пули
        if os.path.exists(filepath):  # Проверяем существует ли файл пули
            try:
                self.bullet_pixmap = QtGui.QPixmap(filepath)  # Загружаем изображение пули из файла
                self.bullet_pixmap = self.bullet_pixmap.scaled(20, 20,
                                                               QtCore.Qt.AspectRatioMode.KeepAspectRatio)  # Масштабируем изображение пули
            except Exception as e:
                print(f"Ошибка загрузки пули: {e}")  # Выводим ошибку если загрузка не удалась
                self.create_fallback_bullet()  # Создаем запасное изображение пули
        else:
            print(f"Файл пули не найден: {filepath}")  # Сообщаем если файл пули не найден
            self.create_fallback_bullet()  # Создаем запасное изображение пули

    def create_fallback_bullet(self):
        """Создание запасного изображения пули"""
        self.bullet_pixmap = QtGui.QPixmap(20, 20)  # Создаем пустое изображение размером 20x20 для пули
        self.bullet_pixmap.fill(QtGui.QColor(255, 255, 0))  # Заполняем изображение желтым цветом

        painter = QtGui.QPainter(self.bullet_pixmap)  # Создаем объект для рисования на изображении пули
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))  # Устанавливаем красный цвет для внутренней части
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 2))  # Устанавливаем белую рамку толщиной 2 пикселя
        painter.drawEllipse(2, 2, 16, 16)  # Рисуем эллипс (круг) внутри пули
        painter.end()  # Заканчиваем рисование

    def create_characters(self):
        """Создание персонажей игры"""
        self.create_player()  # Вызываем метод создания игрока
        self.create_boss()  # Вызываем метод создания босса

    def create_player(self):
        """Создание игрока"""
        self.player = QtWidgets.QGraphicsPixmapItem()  # Создаем графический элемент для отображения картинки игрока

        if self.walk_frames:  # Проверяем есть ли загруженные анимации игрока
            self.player.setPixmap(
                self.walk_frames[0])  # Устанавливаем первую картинку из анимации как изображение игрока
        else:
            self.create_fallback_player()  # Создаем простого игрока если анимаций нет

        player_x = 100  # Устанавливаем начальную позицию игрока по X
        player_y = self.FLOOR_Y - 80  # Вычисляем позицию игрока по Y
        self.player.setPos(player_x, player_y)  # Устанавливаем позицию игрока на сцене
        self.game_scene.addItem(self.player)  # Добавляем игрока на игровую сцену
        self.START_Y = player_y  # Сохраняем стартовую позицию игрока по Y

        self.create_player_ui()  # Вызываем метод создания интерфейса для игрока

    def create_fallback_player(self):
        """Создание запасного игрока"""
        pixmap = QtGui.QPixmap(60, 80)  # Создаем пустое изображение размером 60x80
        pixmap.fill(QtGui.QColor(255, 255, 255))  # Заполняем изображение белым цветом
        self.player.setPixmap(pixmap)  # Устанавливаем это изображение как изображение игрока

    def create_player_ui(self):
        """Создание UI игрока"""
        player_name = self.player_data[
            1] if self.player_data else "Игрок"  # Берем имя игрока из данных или используем "Игрок" по умолчанию

        # Метка имени игрока
        self.player_label = QtWidgets.QGraphicsTextItem(player_name)  # Создаем текстовый элемент с именем игрока
        self.player_label.setDefaultTextColor(QtGui.QColor(
            PLAYER_LABEL_COLOR_R,
            PLAYER_LABEL_COLOR_G,
            PLAYER_LABEL_COLOR_B
        ))  # Устанавливаем желтый цвет текста
        self.player_label.setScale(1)  # Устанавливаем масштаб текста (нормальный размер)
        self.game_scene.addItem(self.player_label)  # Добавляем текстовый элемент на сцену

        # Создаем полоску здоровья
        self.create_player_health_bar()  # Вызываем метод создания полоски здоровья игрока
        # Обновляем позиции всех элементов интерфейса
        self.update_player_ui_positions()  # Вызываем метод обновления позиций UI игрока

    def create_player_health_bar(self):
        """Создание полоски здоровья игрока"""
        # Фон здоровья
        self.player_health_background = QtWidgets.QGraphicsRectItem(0, 0, 102,
                                                                    12)  # Создаем прямоугольник для фона полоски здоровья
        self.player_health_background.setBrush(
            QtGui.QBrush(QtGui.QColor(50, 50, 50)))  # Устанавливаем серый цвет заливки фона
        self.player_health_background.setPen(
            QtGui.QPen(QtGui.QColor(200, 200, 200), 1))  # Устанавливаем белую рамку толщиной 1 пиксель
        self.game_scene.addItem(self.player_health_background)  # Добавляем фон полоски здоровья на сцену

        # Сама полоска здоровья
        self.player_health_bar = QtWidgets.QGraphicsRectItem(1, 1, 100,
                                                             10)  # Создаем прямоугольник для самой полоски здоровья
        self.player_health_bar.setBrush(
            QtGui.QBrush(QtGui.QColor(0, 255, 0)))  # Устанавливаем зеленый цвет заливки полоски здоровья
        self.game_scene.addItem(self.player_health_bar)  # Добавляем полоску здоровья на сцену

        # Текст полоски здоровья
        self.player_health_text = QtWidgets.QGraphicsTextItem(
            f"{self.player_health}/{self.player_max_health}")  # Создаем текстовый элемент с цифрами здоровья
        self.player_health_text.setDefaultTextColor(QtGui.QColor(255, 255, 255))  # Устанавливаем белый цвет текста
        self.player_health_text.setScale(0.8)  # Устанавливаем масштаб текста (80% от нормального размера)
        self.game_scene.addItem(self.player_health_text)  # Добавляем текст здоровья на сцену

    def create_boss(self):
        """Создание босса"""
        self.boss = QtWidgets.QGraphicsPixmapItem()  # Создаем элемент для картинки босса

        if self.boss_frames:  # Если есть анимации босса
            self.boss.setPixmap(self.boss_frames[0])  # Ставим первую картинку
        else:
            self.create_fallback_boss()  # Иначе создаем простого босса

        boss_x = WINDOW_WIDTH // 2 - 50  # Позиция босса по X (центр экрана)
        boss_y = self.FLOOR_Y - 120  # Позиция босса по Y (120 пикселей над полом)
        self.boss.setPos(boss_x, boss_y)  # Устанавливаем позицию
        self.game_scene.addItem(self.boss)  # Добавляем босса на сцену

        self.create_boss_ui()  # Создаем интерфейс для босса

    def create_fallback_boss(self):
        """Создание запасного босса"""
        pixmap = QtGui.QPixmap(100, 120)  # Создаем изображение 100x120
        pixmap.fill(QtGui.QColor(255, 0, 0))  # Красный цвет

        painter = QtGui.QPainter(pixmap)  # Создаем painter для рисования
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 0)))  # Желтый цвет для глаз
        painter.drawEllipse(30, 40, 15, 15)  # Левый глаз
        painter.drawEllipse(55, 40, 15, 15)  # Правый глаз

        painter.setBrush(QtGui.QBrush(QtGui.QColor(100, 0, 0)))  # Темно-красный для рта
        painter.drawEllipse(40, 70, 20, 10)  # Рот

        painter.setBrush(QtGui.QBrush(QtGui.QColor(150, 0, 0)))  # Красный для рук
        painter.drawRect(25, 110, 15, 10)  # Левая рука
        painter.drawRect(60, 110, 15, 10)  # Правая рука
        painter.end()  # Заканчиваем рисование

        self.boss.setPixmap(pixmap)  # Устанавливаем картинку боссу

    def create_boss_ui(self):
        """Создание UI босса"""
        # Метка босса
        self.boss_label = QtWidgets.QGraphicsTextItem(UI_TEXTS['boss'])  # Текст "БОСС"
        self.boss_label.setDefaultTextColor(QtGui.QColor(255, 0, 0))  # Красный цвет
        self.boss_label.setScale(1.5)  # Увеличиваем размер текста
        self.game_scene.addItem(self.boss_label)  # Добавляем на сцену

        # Полоска здоровья босса
        self.create_boss_health_bar()  # Создаем полоску здоровья
        self.update_boss_ui_positions()  # Обновляем позиции UI

    def create_boss_health_bar(self):
        """Создание полоски здоровья босса"""
        # Фон здоровья
        self.boss_health_background = QtWidgets.QGraphicsRectItem(0, 0, 202, 20)  # Прямоугольник для фона
        self.boss_health_background.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50)))  # Серый цвет
        self.boss_health_background.setPen(QtGui.QPen(QtGui.QColor(200, 200, 200), 2))  # Белая рамка
        self.game_scene.addItem(self.boss_health_background)  # Добавляем на сцену

        # Полоска здоровья
        self.boss_health_bar = QtWidgets.QGraphicsRectItem(1, 1, 200, 18)  # Прямоугольник для здоровья
        self.boss_health_bar.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))  # Красный цвет
        self.game_scene.addItem(self.boss_health_bar)  # Добавляем на сцену

        # Текст здоровья
        self.boss_health_text = QtWidgets.QGraphicsTextItem(
            f"{self.boss_health}/{self.boss_max_health}")  # Текст с здоровьем
        self.boss_health_text.setDefaultTextColor(QtGui.QColor(255, 255, 255))  # Белый цвет
        self.boss_health_text.setScale(1)  # Нормальный размер
        self.game_scene.addItem(self.boss_health_text)  # Добавляем на сцену

    def setup_ui_elements(self):
        """Настройка UI элементов"""
        self.create_pause_button()  # Создаем кнопку паузы
        self.create_pause_menu()  # Создаем меню паузы
        self.create_death_screen()  # Создаем экран смерти
        self.create_win_screen()  # Создаем экран победы

    def create_pause_button(self):
        """Создание кнопки паузы"""
        self.pause_button = QtWidgets.QGraphicsRectItem(0, 0, 50, 50)  # Прямоугольник для кнопки
        self.pause_button.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 0, 200)))  # Желтый полупрозрачный
        self.pause_button.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 2))  # Белая рамка
        self.pause_button.setPos(WINDOW_WIDTH - 60, 10)  # Позиция в правом верхнем углу
        self.pause_button.setZValue(1000)  # Высокий уровень (чтобы была поверх всего)
        self.game_scene.addItem(self.pause_button)  # Добавляем на сцену

        # Текст на кнопке
        self.pause_button_text = QtWidgets.QGraphicsTextItem("II")  # Текст "II"
        self.pause_button_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))  # Черный текст
        self.pause_button_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Weight.Bold))  # Большой жирный шрифт
        self.pause_button_text.setPos(WINDOW_WIDTH - 50, 15)  # Позиция текста
        self.pause_button_text.setZValue(1001)  # Уровень выше кнопки
        self.game_scene.addItem(self.pause_button_text)  # Добавляем на сцену

    def create_pause_menu(self):
        """Создание меню паузы"""
        self.pause_overlay = self.create_overlay()  # Создаем темный фон
        self.pause_overlay.setZValue(100)  # Уровень поверх игры

        # Заголовок "ПАУЗА"
        self.pause_title_text = self.create_text_item("ПАУЗА", 48, QtGui.QColor(255, 255, 255),
                                                      WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 150, 101)

        # Кнопки меню паузы
        self.create_pause_buttons()  # Создаем кнопки для меню паузы

    def create_overlay(self):
        """Создание темного полупрозрачного фона для меню"""
        overlay = QtWidgets.QGraphicsRectItem(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)  # Прямоугольник на все окно
        overlay.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 180)))  # Черный с прозрачностью
        overlay.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))  # Без рамки
        overlay.setPos(0, 0)  # Позиция в начале
        overlay.setVisible(False)  # Изначально не виден
        self.game_scene.addItem(overlay)  # Добавляем на сцену
        return overlay  # Возвращаем элемент

    def create_text_item(self, text, font_size, color, x, y, z_value):
        """Создание текстового элемента"""
        text_item = QtWidgets.QGraphicsTextItem(text)  # Создаем текст
        text_item.setDefaultTextColor(color)  # Устанавливаем цвет
        text_item.setFont(QtGui.QFont("Arial", font_size, QtGui.QFont.Weight.Bold))  # Шрифт
        text_item.setPos(x, y)  # Позиция
        text_item.setZValue(z_value)  # Уровень
        text_item.setVisible(False)  # Изначально не виден
        self.game_scene.addItem(text_item)  # Добавляем на сцену
        return text_item  # Возвращаем элемент

    def create_pause_buttons(self):
        """Создает кнопки для меню паузы"""
        # Кнопка "Продолжить"
        self.resume_button, self.resume_text = self.create_menu_button(
            "Продолжить", QtGui.QColor(0, 100, 0), WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50)

        # Кнопка "В главное меню"
        self.pause_main_menu_button, self.pause_main_menu_text = self.create_menu_button(
            "В главное меню", QtGui.QColor(150, 0, 150), WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20)

    def create_menu_button(self, text, color, x, y):
        """Создает одну кнопку для любого меню"""
        # Прямоугольник кнопки
        button = QtWidgets.QGraphicsRectItem(0, 0, 200, 50)  # Размер 200x50
        button.setBrush(QtGui.QBrush(color))  # Цвет кнопки
        button.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 2))  # Белая рамка
        button.setPos(x, y)  # Позиция
        button.setZValue(101)  # Уровень
        button.setVisible(False)  # Изначально не видна
        self.game_scene.addItem(button)  # Добавляем на сцену

        # Текст кнопки
        text_item = QtWidgets.QGraphicsTextItem(text)  # Создаем текст
        text_item.setDefaultTextColor(QtGui.QColor(255, 255, 255))  # Белый текст
        font_size = 14 if len(text) > 12 else 16  # Размер шрифта в зависимости от длины текста
        text_item.setFont(QtGui.QFont("Arial", font_size))  # Шрифт
        text_item.setPos(x + 10, y + 10)  # Позиция текста внутри кнопки
        text_item.setZValue(102)  # Уровень выше кнопки
        text_item.setVisible(False)  # Изначально не виден
        self.game_scene.addItem(text_item)  # Добавляем на сцену

        return button, text_item  # Возвращаем кнопку и текст

    def create_death_screen(self):
        """Создание экрана смерти"""
        self.death_overlay = self.create_overlay()  # Темный фон
        self.death_overlay.setZValue(100)  # Уровень поверх игры

        # Текст "YOU LOSE"
        self.you_lose_text = self.create_text_item("YOU LOSE", 48, QtGui.QColor(255, 0, 0),
                                                   WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 100, 101)

        # Кнопки для экрана смерти
        self.create_death_buttons()  # Создаем кнопки

    def create_death_buttons(self):
        """Создает кнопки для экрана смерти"""
        # Кнопка "Начать заново"
        self.restart_button, self.restart_text = self.create_menu_button(
            "Начать заново", QtGui.QColor(0, 100, 0), WINDOW_WIDTH // 2 - 220, WINDOW_HEIGHT // 2 - 20)

        # Кнопка "В главное меню"
        self.death_main_menu_button, self.death_main_menu_text = self.create_menu_button(
            "В главное меню", QtGui.QColor(150, 0, 150), WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT // 2 - 20)

    def create_win_screen(self):
        """Создание экрана победы"""
        self.win_overlay = self.create_overlay()  # Темный фон
        self.win_overlay.setZValue(100)  # Уровень поверх игры

        # Текст "YOU WIN!"
        self.you_win_text = self.create_text_item("YOU WIN!", 48, QtGui.QColor(0, 255, 0),
                                                  WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 100, 101)

        # Кнопки для экрана победы
        self.create_win_buttons()  # Создаем кнопки

    def create_win_buttons(self):
        """Создает кнопки для экрана победы"""
        # Кнопка "Сыграть еще"
        self.play_again_button, self.play_again_text = self.create_menu_button(
            "Сыграть еще", QtGui.QColor(0, 100, 0), WINDOW_WIDTH // 2 - 220, WINDOW_HEIGHT // 2 - 30)

        # Кнопка "Следующий уровень"
        self.next_level_button, self.next_level_text = self.create_menu_button(
            "Следующий уровень", QtGui.QColor(0, 0, 150), WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT // 2 - 30)

        # Кнопка "В главное меню"
        self.main_menu_button, self.main_menu_text = self.create_menu_button(
            "В главное меню", QtGui.QColor(150, 0, 150), WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50)

    def setup_game_mechanics(self):
        """Настройка игровой механики"""
        self.setup_timers()  # Настраиваем таймеры
        self.prev_player_y = self.player.y() if hasattr(self, 'player') else 0  # Запоминаем позицию игрока

    def setup_timers(self):
        """Настройка игровых таймеров"""
        # Основной игровой таймер
        self.game_timer = QtCore.QTimer()  # Создаем таймер
        self.game_timer.timeout.connect(self.game_loop)  # Подключаем к игровому циклу
        self.game_timer.start(GAME_LOOP_INTERVAL)  # Запускаем (60 раз в секунду)

        # Таймер анимации игрока
        self.animation_timer = QtCore.QTimer()  # Создаем таймер
        self.animation_timer.timeout.connect(self.update_animation)  # Подключаем к анимации
        self.animation_timer.start(PLAYER_ANIMATION_INTERVAL)  # Запускаем (5 раз в секунду)

        # Таймер анимации босса
        self.boss_animation_timer = QtCore.QTimer()  # Создаем таймер
        self.boss_animation_timer.timeout.connect(self.update_boss_animation)  # Подключаем к анимации
        self.boss_animation_timer.start(16)  # Запускаем (60 раз в секунду)

    def game_loop(self):
        """Основной игровой цикл"""
        if self.game_paused:  # Если игра на паузе
            return  # Выходим из цикла

        try:
            self.update_cooldowns()  # Обновляем перезарядки
            self.handle_player_movement()  # Обрабатываем движение игрока
            self.handle_jump()  # Обрабатываем прыжки
            self.update_bullets()  # Обновляем пули

            # Движение босса
            self.update_boss_gravity()  # Обновляем гравитацию босса
            self.check_boss_collisions()  # Проверяем столкновения босса
            self.update_boss_movement()  # Обновляем движение босса

            self.check_player_boss_collision()  # Проверяем столкновение с боссом
            self.check_collisions()  # Проверяем все столкновения
            self.update_ui_positions()  # Обновляем позиции UI

            if self.player_health <= 0 and self.player_alive:  # Если игрок умер
                self.player_die()  # Вызываем смерть игрока
            if self.boss_health <= 0 and self.boss_alive:  # Если босс умер
                self.boss_defeated()  # Вызываем победу над боссом

        except Exception as e:
            self.handle_critical_error("Игровой цикл", e)  # Обрабатываем ошибку

    def update_cooldowns(self):
        """Уменьшает все таймеры перезарядки на 1"""
        if self.boss_damage_cooldown > 0:  # Если таймер урона босса активен
            self.boss_damage_cooldown -= 1  # Уменьшаем на 1

        if self.jump_buffer > 0:  # Если буфер прыжка активен
            self.jump_buffer -= 1  # Уменьшаем на 1

        if self.bullet_cooldown > 0:  # Если перезарядка пули активна
            self.bullet_cooldown -= 1  # Уменьшаем на 1

    def handle_player_movement(self):
        """Обрабатывает движение игрока влево-вправо"""
        if not self.player_alive:  # Если игрок мертв
            return  # Не двигаем

        new_x = self.player.x()  # Запоминаем текущую позицию X

        if self.moving_left and not self.moving_right:  # Если движемся влево
            new_x = max(0, new_x - PLAYER_SPEED)  # Двигаем влево

        elif self.moving_right and not self.moving_left:  # Если движемся вправо
            new_x = min(WINDOW_WIDTH - 60, new_x + PLAYER_SPEED)  # Двигаем вправо

        self.player.setX(new_x)  # Устанавливаем новую позицию

    def handle_jump(self):
        """Обрабатывает прыжки и гравитацию"""
        if not self.player_alive:  # Если игрок мертв
            return  # Не обрабатываем прыжки

        if not self.on_ground:  # Если игрок в воздухе
            self.player_velocity_y += GRAVITY  # Добавляем гравитацию
            new_y = self.player.y() + self.player_velocity_y  # Вычисляем новую позицию Y
            self.player.setY(new_y)  # Устанавливаем новую позицию

        if self.jump_buffer > 0 and self.on_ground:  # Если буфер прыжка и на земле
            self.is_jumping = True  # Начинаем прыжок
            self.player_velocity_y = JUMP_POWER  # Устанавливаем силу прыжка
            self.on_ground = False  # Больше не на земле
            self.jump_buffer = 0  # Сбрасываем буфер

    def check_collisions(self):
        """Проверяет столкновения игрока с полом и платформами"""
        if not self.player_alive:  # Если игрок мертв
            return False  # Возвращаем False

        try:
            player_rect = self.player.sceneBoundingRect()  # Получаем границы игрока
            current_y = self.player.y()  # Запоминаем текущую позицию Y

            if self.check_floor_collision(player_rect):  # Проверяем столкновение с полом
                return True  # Было столкновение

            platform_collision = self.check_platform_collisions(player_rect, current_y)  # Проверяем платформы
            self.prev_player_y = current_y  # Сохраняем позицию для следующего кадра
            return platform_collision  # Возвращаем результат

        except Exception as e:
            print(f"Ошибка при проверке коллизий: {e}")  # Выводим ошибку
            return False  # Возвращаем False

    def check_floor_collision(self, player_rect):
        """Проверяет, стоит ли игрок на полу"""
        floor_rect = self.floor_line.sceneBoundingRect()  # Получаем границы пола

        # Проверяем условия столкновения с полом
        if (player_rect.bottom() >= floor_rect.top() and  # Низ игрока на уровне верха пола
                player_rect.top() < floor_rect.bottom() and  # Верх игрока выше низа пола
                self.player_velocity_y >= 0):  # Игрок падает вниз

            self.player.setY(floor_rect.top() - player_rect.height())  # Ставим игрока на пол
            self.player_velocity_y = 0  # Сбрасываем скорость
            self.on_ground = True  # Теперь на земле
            self.is_jumping = False  # Не в прыжке
            return True  # Было столкновение

        return False  # Не было столкновения

    def check_platform_collisions(self, player_rect, current_y):
        """Проверяет столкновения со всеми платформами"""
        found_platform = False  # Флаг нахождения платформы

        for platform in self.platforms:  # Перебираем все платформы
            platform_rect = platform.sceneBoundingRect()  # Получаем границы платформы

            if self.is_colliding_with_platform(player_rect, platform_rect, current_y):  # Проверяем столкновение
                self.player.setY(platform_rect.top() - player_rect.height())  # Ставим игрока на платформу
                self.player_velocity_y = 0  # Сбрасываем скорость
                self.on_ground = True  # Теперь на земле
                self.is_jumping = False  # Не в прыжке
                found_platform = True  # Нашли платформу
                break  # Выходим из цикла

        if not found_platform:  # Если не нашли платформу
            self.on_ground = False  # Не на земле

        return found_platform  # Возвращаем результат

    def is_colliding_with_platform(self, player_rect, platform_rect, current_y):
        """Проверяет столкновение с конкретной платформой"""
        player_bottom = player_rect.bottom()  # Низ игрока
        prev_player_bottom = self.prev_player_y + player_rect.height()  # Низ в предыдущем кадре

        # Игрок находится над платформой
        is_above = (player_bottom >= platform_rect.top() - 5 and  # Близко к верху платформы
                    player_bottom <= platform_rect.top() + 25 and  # Но не слишком далеко
                    player_rect.top() < platform_rect.bottom() and  # Верх игрока выше низа платформы
                    player_rect.right() > platform_rect.left() + 5 and  # Правый край справее левого края платформы
                    player_rect.left() < platform_rect.right() - 5 and  # Левый край левее правого края платформы
                    self.player_velocity_y >= 0)  # Игрок падает вниз

        # Игрок прошел сквозь платформу сверху вниз
        passed_through = (prev_player_bottom <= platform_rect.top() and  # В предыдущем кадре был над платформой
                          player_bottom >= platform_rect.top() and  # В текущем кадре на/под платформой
                          player_rect.right() > platform_rect.left() + 5 and  # В пределах платформы по X
                          player_rect.left() < platform_rect.right() - 5 and  # В пределах платформы по X
                          self.player_velocity_y > 0)  # Игрок двигался вниз

        return is_above or passed_through  # Возвращаем результат

    def update_bullets(self):
        """Обновляет все пули на экране"""
        bullets_to_remove = []  # Список пуль для удаления

        for i, bullet_data in enumerate(self.bullets):  # Перебираем все пули
            bullet = bullet_data['item']  # Получаем саму пулю
            direction = bullet_data['direction']  # Получаем направление

            new_x = bullet.x() + (BULLET_SPEED * direction)  # Вычисляем новую позицию X
            bullet.setX(new_x)  # Устанавливаем новую позицию
            bullet_data['x'] = new_x  # Обновляем данные

            if self.check_bullet_boss_collision(bullet):  # Проверяем попадание в босса
                bullets_to_remove.append(i)  # Добавляем в список на удаление
                continue  # Переходим к следующей пуле

            if new_x < -50 or new_x > WINDOW_WIDTH + 50:  # Если пуля вышла за экран
                bullets_to_remove.append(i)  # Добавляем в список на удаление

        for i in sorted(bullets_to_remove, reverse=True):  # Удаляем пули с конца
            bullet_data = self.bullets[i]  # Получаем данные пули
            self.game_scene.removeItem(bullet_data['item'])  # Удаляем со сцены
            self.bullets.pop(i)  # Удаляем из списка

    def check_bullet_boss_collision(self, bullet):
        """Проверяем, столкнулась ли пуля с боссом"""
        if not hasattr(self, 'boss') or not self.boss or self.boss_health <= 0 or not self.boss_alive:
            return False  # Если босса нет или он мертв

        bullet_rect = bullet.sceneBoundingRect()  # Получаем границы пули
        boss_rect = self.boss.sceneBoundingRect()  # Получаем границы босса

        if bullet_rect.intersects(boss_rect):  # Если пуля пересекается с боссом
            self.boss_health -= self.bullet_damage  # Отнимаем здоровье
            self.update_boss_health_display()  # Обновляем полоску здоровья

            if self.boss_health <= 0:  # Если здоровье закончилось
                self.boss_health = 0  # Устанавливаем 0
                self.boss_defeated()  # Вызываем победу
            return True  # Пуля попала

        return False  # Пуля не попала

    def create_bullet(self):
        """Создает новую пулю когда игрок стреляет"""
        if self.bullet_cooldown > 0 or not self.player_alive:  # Если перезарядка или игрок мертв
            return  # Выходим

        bullet = QtWidgets.QGraphicsPixmapItem()  # Создаем элемент для пули

        if self.bullet_pixmap:  # Если есть изображение пули
            bullet.setPixmap(self.bullet_pixmap)  # Устанавливаем изображение
        else:
            pixmap = QtGui.QPixmap(20, 20)  # Создаем изображение
            pixmap.fill(QtGui.QColor(255, 255, 0))  # Желтый цвет
            bullet.setPixmap(pixmap)  # Устанавливаем изображение

        player_center_y = self.player.y() + 30  # Центр игрока по высоте

        if self.facing_right:  # Если смотрит направо
            bullet_x = self.player.x() + 40  # Пуля справа от игрока
        else:
            bullet_x = self.player.x() - 20  # Пуля слева от игрока

        bullet.setPos(bullet_x, player_center_y)  # Устанавливаем позицию
        self.game_scene.addItem(bullet)  # Добавляем на сцену

        self.bullets.append({  # Добавляем в список пуль
            'item': bullet,  # Сама пуля
            'direction': 1 if self.facing_right else -1,  # Направление
            'x': bullet_x,  # Позиция X
            'y': player_center_y  # Позиция Y
        })

        self.bullet_cooldown = self.bullet_cooldown_max  # Запускаем перезарядку

        self.sound_manager.play_bullet_sound()


    def update_boss_gravity(self):
        """Обновление гравитации для босса"""
        if not self.boss_alive:  # Если босс мертв
            return  # Выходим

        if not self.boss_on_ground:  # Если босс в воздухе
            self.boss_velocity_y += GRAVITY  # Добавляем гравитацию
            new_y = self.boss.y() + self.boss_velocity_y  # Вычисляем новую позицию Y
            self.boss.setY(new_y)  # Устанавливаем новую позицию

    def check_boss_collisions(self):
        """Проверка коллизий босса с полом и платформами"""
        if not self.boss_alive:  # Если босс мертв
            return False  # Возвращаем False

        boss_rect = self.boss.sceneBoundingRect()  # Получаем границы босса
        current_y = self.boss.y()  # Запоминаем позицию Y

        floor_rect = self.floor_line.sceneBoundingRect()  # Получаем границы пола
        if (boss_rect.bottom() >= floor_rect.top() and  # Низ босса на уровне верха пола
                boss_rect.top() < floor_rect.bottom() and  # Верх босса выше низа пола
                self.boss_velocity_y >= 0):  # Босс падает вниз

            self.boss.setY(floor_rect.top() - boss_rect.height())  # Ставим босса на пол
            self.boss_velocity_y = 0  # Сбрасываем скорость
            self.boss_on_ground = True  # Теперь на земле
            return True  # Было столкновение

        for platform in self.platforms:  # Перебираем платформы
            platform_rect = platform.sceneBoundingRect()  # Получаем границы платформы

            if (boss_rect.bottom() >= platform_rect.top() - 10 and  # Близко к верху платформы
                    boss_rect.bottom() <= platform_rect.top() + 20 and  # Но не слишком далеко
                    boss_rect.right() > platform_rect.left() + 20 and  # В пределах платформы по X
                    boss_rect.left() < platform_rect.right() - 20 and  # В пределах платформы по X
                    self.boss_velocity_y >= 0):  # Босс падает вниз

                self.boss.setY(platform_rect.top() - boss_rect.height())  # Ставим на платформу
                self.boss_velocity_y = 0  # Сбрасываем скорость
                self.boss_on_ground = True  # Теперь на земле
                return True  # Было столкновение

        self.boss_on_ground = False  # Не на земле
        return False  # Не было столкновения

    def check_player_boss_collision(self):
        """Проверяем, столкнулся ли игрок с боссом"""
        if not self.player_alive:  # Если игрок мертв
            return False  # Возвращаем False
        if not hasattr(self, 'boss') or not self.boss or not self.boss_alive:  # Если босса нет
            return False  # Возвращаем False

        player_rect = self.player.sceneBoundingRect()  # Получаем границы игрока
        boss_rect = self.boss.sceneBoundingRect()  # Получаем границы босса

        danger_zone = 70  # Опасная зона вокруг босса

        player_center = player_rect.center()  # Центр игрока
        boss_center = boss_rect.center()  # Центр босса

        distance_x = abs(player_center.x() - boss_center.x())  # Расстояние по X
        distance_y = abs(player_center.y() - boss_center.y())  # Расстояние по Y

        if distance_x < danger_zone and distance_y < danger_zone:  # Если игрок близко к боссу
            if self.boss_damage_cooldown <= 0:  # Если перезарядка урона прошла
                self.player_take_damage(self.boss_damage)  # Наносим урон игроку
                self.boss_damage_cooldown = self.boss_damage_cooldown_max  # Запускаем перезарядку
            return True  # Было столкновение

        return False  # Не было столкновения

    def player_take_damage(self, damage):
        """Наносит урон игроку"""
        if not self.player_alive:  # Если игрок мертв
            return  # Выходим

        self.player_health -= damage  # Отнимаем здоровье

        if self.player_health <= 0:  # Если здоровье закончилось
            self.player_health = 0  # Устанавливаем 0
            self.player_die()  # Вызываем смерть игрока
        else:
            self.update_player_health_display()  # Обновляем полоску здоровья

    def player_die(self):
        """Обработка смерти игрока"""
        if not self.player_alive:  # Если игрок уже мертв
            return  # Выходим

        self.player_health = 0  # Устанавливаем здоровье 0
        self.player_alive = False  # Помечаем игрока мертвым

        dead_pixmap = QtGui.QPixmap(40, 60)  # Создаем изображение мертвого игрока
        dead_pixmap.fill(QtGui.QColor(100, 100, 100))  # Серый цвет

        painter = QtGui.QPainter(dead_pixmap)  # Создаем painter для рисования
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 3))  # Красная линия
        painter.drawLine(10, 10, 30, 50)  # Диагональная линия
        painter.drawLine(30, 10, 10, 50)  # Диагональная линия
        painter.end()  # Заканчиваем рисование

        self.player.setPixmap(dead_pixmap)  # Устанавливаем изображение мертвого игрока
        self.player_label.setPlainText(UI_TEXTS['dead'])  # Меняем текст на "МЕРТВ"
        self.player_label.setDefaultTextColor(QtGui.QColor(255, 0, 0))  # Красный цвет

        self.moving_left = False  # Сбрасываем движение влево
        self.moving_right = False  # Сбрасываем движение вправо
        self.is_walking = False  # Сбрасываем ходьбу

        self.show_death_screen()  # Показываем экран смерти

    def boss_defeated(self):
        """Обработка победы над боссом"""
        try:
            player_id = self.player_data[0]  # Получаем ID игрока

            credits_success = self.db.add_credits(player_id, CREDITS_REWARD)  # Добавляем кредиты
            if not self.Examination_level_update:  # Если уровень еще не обновлялся
                level_success = self.db.add_level(player_id, LEVEL_UP_REWARD)  # Добавляем уровень
                self.Examination_level_update = True  # Помечаем что обновили

            self.boss_alive = False  # Помечаем босса мертвым
            self.hide_boss()  # Скрываем босса
            self.show_win_screen()  # Показываем экран победы

        except Exception as e:
            print(f"Ошибка при обработке победы над боссом: {e}")  # Выводим ошибку

    def hide_boss(self):
        """Скрытие босса и его UI"""
        self.boss.setVisible(False)  # Скрываем босса
        self.boss_label.setVisible(False)  # Скрываем надпись босса
        self.boss_health_background.setVisible(False)  # Скрываем фон здоровья
        self.boss_health_bar.setVisible(False)  # Скрываем полоску здоровья
        self.boss_health_text.setVisible(False)  # Скрываем текст здоровья

    def update_animation(self):
        """Обновление анимации игрока"""
        if not self.walk_frames or not self.player_alive:  # Если нет анимаций или игрок мертв
            return  # Выходим

        if (self.moving_left or self.moving_right) and not (
                self.moving_left and self.moving_right):  # Если двигается в одну сторону
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)  # Переходим к следующему кадру
        else:
            self.current_frame = 0  # Показываем первый кадр (стояние)

        current_pixmap = self.walk_frames[self.current_frame]  # Получаем текущий кадр

        if not self.facing_right:  # Если смотрит налево
            mirrored = current_pixmap.transformed(QtGui.QTransform().scale(-1, 1))  # Отражаем по горизонтали
            self.player.setPixmap(mirrored)  # Устанавливаем отраженное изображение
        else:
            self.player.setPixmap(current_pixmap)  # Устанавливаем обычное изображение

    def update_boss_animation(self):
        """Обновление анимации босса"""
        if not self.boss_frames or not self.boss_alive:  # Если нет анимаций или босс мертв
            return  # Выходим

        self.boss_animation_counter += 1  # Увеличиваем счетчик анимации
        if self.boss_animation_counter >= 10:  # Каждые 10 вызовов
            self.boss_current_frame = (self.boss_current_frame + 1) % len(
                self.boss_frames)  # Переходим к следующему кадру
            self.boss_animation_counter = 0  # Сбрасываем счетчик

            current_pixmap = self.boss_frames[self.boss_current_frame]  # Получаем текущий кадр
            if not self.boss_facing_right:  # Если смотрит налево
                mirrored = current_pixmap.transformed(QtGui.QTransform().scale(-1, 1))  # Отражаем по горизонтали
                self.boss.setPixmap(mirrored)  # Устанавливаем отраженное изображение
            else:
                self.boss.setPixmap(current_pixmap)  # Устанавливаем обычное изображение

    def update_ui_positions(self):
        """Обновление позиций UI элементов"""
        self.update_player_ui_positions()  # Обновляем UI игрока
        self.update_boss_ui_positions()  # Обновляем UI босса

    def update_player_ui_positions(self):
        """Обновление позиций UI игрока"""
        if not self.player_alive:  # Если игрок мертв
            return  # Выходим

        player_x = self.player.x()  # Позиция игрока X
        player_y = self.player.y()  # Позиция игрока Y

        self.player_label.setPos(player_x, player_y - 70)  # Имя над игроком
        self.update_player_health_display()  # Обновляем здоровье

    def update_player_health_display(self):
        """Обновление отображения здоровья игрока"""
        if not self.player_alive:  # Если игрок мертв
            return  # Выходим

        player_x = self.player.x()  # Позиция игрока X
        player_y = self.player.y()  # Позиция игрока Y

        self.player_health_background.setPos(player_x - 1, player_y - 30)  # Фон здоровья
        self.player_health_bar.setPos(player_x, player_y - 29)  # Полоска здоровья

        health_width = (self.player_health / self.player_max_health) * 100  # Ширина полоски
        self.player_health_bar.setRect(0, 0, health_width, 10)  # Устанавливаем ширину

        if self.player_health < 30:  # Если мало здоровья
            color = QtGui.QColor(255, 0, 0)  # Красный цвет
        elif self.player_health < 60:  # Если среднее здоровье
            color = QtGui.QColor(255, 165, 0)  # Оранжевый цвет
        else:  # Если много здоровья
            color = QtGui.QColor(0, 255, 0)  # Зеленый цвет

        self.player_health_bar.setBrush(QtGui.QBrush(color))  # Устанавливаем цвет

        if hasattr(self, 'player_health_text'):  # Если есть текст здоровья
            self.player_health_text.setPlainText(f"{self.player_health}/{self.player_max_health}")  # Обновляем текст
            self.player_health_text.setPos(player_x, player_y - 45)  # Позиция текста

    def toggle_pause(self):
        """Включает или выключает паузу"""
        if not self.player_alive or not self.boss_alive:  # Если игрок или босс мертв
            return  # Пауза не работает

        self.game_paused = not self.game_paused  # Меняем состояние паузы

        if self.game_paused:  # Если включили паузу
            self.show_pause_menu()  # Показываем меню паузы
            self.game_timer.stop()  # Останавливаем игровой цикл
            self.animation_timer.stop()  # Останавливаем анимацию игрока
            self.boss_animation_timer.stop()  # Останавливаем анимацию босса
        else:  # Если выключили паузу
            self.hide_pause_menu()  # Прячем меню паузы
            self.game_timer.start(16)  # Запускаем игровой цикл
            self.animation_timer.start(200)  # Запускаем анимацию игрока
            self.boss_animation_timer.start(16)  # Запускаем анимацию босса

    def show_pause_menu(self):
        """Показывает меню паузы"""
        self.pause_overlay.setVisible(True)  # Показываем темный фон
        self.pause_title_text.setVisible(True)  # Показываем текст "ПАУЗА"
        self.resume_button.setVisible(True)  # Показываем кнопку "Продолжить"
        self.resume_text.setVisible(True)  # Показываем текст кнопки
        self.pause_main_menu_button.setVisible(True)  # Показываем кнопку "В главное меню"
        self.pause_main_menu_text.setVisible(True)  # Показываем текст кнопки

    def hide_pause_menu(self):
        """Прячет меню паузы"""
        self.pause_overlay.setVisible(False)  # Прячем темный фон
        self.pause_title_text.setVisible(False)  # Прячем текст "ПАУЗА"
        self.resume_button.setVisible(False)  # Прячем кнопку "Продолжить"
        self.resume_text.setVisible(False)  # Прячем текст кнопки
        self.pause_main_menu_button.setVisible(False)  # Прячем кнопку "В главное меню"
        self.pause_main_menu_text.setVisible(False)  # Прячем текст кнопки

    def show_death_screen(self):
        """Показывает экран смерти"""
        self.death_overlay.setVisible(True)  # Темный фон
        self.you_lose_text.setVisible(True)  # Текст "YOU LOSE"
        self.restart_button.setVisible(True)  # Кнопка "Начать заново"
        self.restart_text.setVisible(True)  # Текст кнопки
        self.death_main_menu_button.setVisible(True)  # Кнопка "В главное меню"
        self.death_main_menu_text.setVisible(True)  # Текст кнопки

    def hide_death_screen(self):
        """Скрыть экран смерти"""
        self.death_overlay.setVisible(False)  # Прячем фон
        self.you_lose_text.setVisible(False)  # Прячем текст
        self.restart_button.setVisible(False)  # Прячем кнопку
        self.restart_text.setVisible(False)  # Прячем текст кнопки
        self.death_main_menu_button.setVisible(False)  # Прячем кнопку
        self.death_main_menu_text.setVisible(False)  # Прячем текст кнопки

    def show_win_screen(self):
        """Показывает экран победы"""
        self.win_overlay.setVisible(True)  # Темный фон
        self.you_win_text.setVisible(True)  # Текст "YOU WIN!"
        self.play_again_button.setVisible(True)  # Кнопка "Сыграть еще"
        self.play_again_text.setVisible(True)  # Текст кнопки
        self.next_level_button.setVisible(True)  # Кнопка "Следующий уровень"
        self.next_level_text.setVisible(True)  # Текст кнопки
        self.main_menu_button.setVisible(True)  # Кнопка "В главное меню"
        self.main_menu_text.setVisible(True)  # Текст кнопки

    def hide_win_screen(self):
        """Прячет экран победы"""
        self.win_overlay.setVisible(False)  # Прячем фон
        self.you_win_text.setVisible(False)  # Прячем текст
        self.play_again_button.setVisible(False)  # Прячем кнопку
        self.play_again_text.setVisible(False)  # Прячем текст кнопки
        self.next_level_button.setVisible(False)  # Прячем кнопку
        self.next_level_text.setVisible(False)  # Прячем текст кнопки
        self.main_menu_button.setVisible(False)  # Прячем кнопку
        self.main_menu_text.setVisible(False)  # Прячем текст кнопки

    def keyPressEvent(self, event):
        """Вызывается когда нажимают клавишу"""
        if not self.player_alive:  # Если игрок мертв
            if event.key() == QtCore.Qt.Key.Key_Escape:  # Если нажали ESC
                self.close()  # Закрываем игру
            return  # Выходим

        try:
            if event.key() == QtCore.Qt.Key.Key_Escape:  # Если нажали ESC
                self.toggle_pause()  # Включаем/выключаем паузу

            elif event.key() == QtCore.Qt.Key.Key_A:  # Если нажали A
                self.moving_left = True  # Движемся влево
                self.facing_right = False  # Смотрим налево
                self.is_walking = not self.moving_right  # Ходим если не движемся вправо

            elif event.key() == QtCore.Qt.Key.Key_D:  # Если нажали D
                self.moving_right = True  # Движемся вправо
                self.facing_right = True  # Смотрим направо
                self.is_walking = not self.moving_left  # Ходим если не движемся влево

            elif event.key() == QtCore.Qt.Key.Key_Space:  # Если нажали ПРОБЕЛ
                self.jump_buffer = self.jump_buffer_max  # Включаем буфер прыжка

            elif event.key() == QtCore.Qt.Key.Key_Return or event.key() == QtCore.Qt.Key.Key_Enter:  # Если нажали ENTER
                self.create_bullet()  # Стреляем

        except Exception as e:
            print(f"Ошибка при обработке нажатия клавиши: {e}")  # Выводим ошибку

    def keyReleaseEvent(self, event):
        """Вызывается когда отпускают клавишу"""
        if not self.player_alive:  # Если игрок мертв
            return  # Выходим

        try:
            if event.key() == QtCore.Qt.Key.Key_A:  # Если отпустили A
                self.moving_left = False  # Не движемся влево
                if self.moving_right:  # Если все еще движемся вправо
                    self.facing_right = True  # Смотрим направо
                    self.is_walking = True  # Ходим
                else:
                    self.is_walking = False  # Не ходим

            elif event.key() == QtCore.Qt.Key.Key_D:  # Если отпустили D
                self.moving_right = False  # Не движемся вправо
                if self.moving_left:  # Если все еще движемся влево
                    self.facing_right = False  # Смотрим налево
                    self.is_walking = True  # Ходим
                else:
                    self.is_walking = False  # Не ходим

        except Exception as e:
            print(f"Ошибка при обработке отпускания клавиши: {e}")  # Выводим ошибку

    def mousePressEvent(self, event):
        """Вызывается когда кликают мышкой"""
        pos = self.game_view.mapToScene(event.pos())  # Преобразуем координаты мыши

        # Проверяем клик по кнопке паузы
        pause_button_rect = self.pause_button.sceneBoundingRect()  # Границы кнопки паузы
        if pause_button_rect.contains(pos) and self.player_alive and self.boss_alive:  # Если кликнули по кнопке
            self.toggle_pause()  # Включаем/выключаем паузу
            return  # Выходим

        # Если игра на паузе
        if self.game_paused:
            resume_rect = self.resume_button.sceneBoundingRect()  # Границы кнопки "Продолжить"
            if resume_rect.contains(pos):  # Если кликнули по кнопке
                self.toggle_pause()  # Выключаем паузу
                return  # Выходим

            pause_main_menu_rect = self.pause_main_menu_button.sceneBoundingRect()  # Границы кнопки "В главное меню"
            if pause_main_menu_rect.contains(pos):  # Если кликнули по кнопке
                self.return_to_main_menu()  # Возвращаемся в главное меню
                return  # Выходим

        # Если игрок мертв
        if not self.player_alive and self.restart_button.isVisible():
            restart_rect = self.restart_button.sceneBoundingRect()  # Границы кнопки "Начать заново"
            if restart_rect.contains(pos):  # Если кликнули по кнопке
                self.restart_game()  # Перезапускаем игру
                return  # Выходим

            death_main_menu_rect = self.death_main_menu_button.sceneBoundingRect()  # Границы кнопки "В главное меню"
            if death_main_menu_rect.contains(pos):  # Если кликнули по кнопке
                self.return_to_main_menu_from_death()  # Возвращаемся в главное меню
                return  # Выходим

        # Если босс мертв (победа)
        elif not self.boss_alive and self.play_again_button.isVisible():
            play_again_rect = self.play_again_button.sceneBoundingRect()  # Границы кнопки "Сыграть еще"
            if play_again_rect.contains(pos):  # Если кликнули по кнопке
                self.restart_game()  # Перезапускаем игру
                return  # Выходим

            next_level_rect = self.next_level_button.sceneBoundingRect()  # Границы кнопки "Следующий уровень"
            if next_level_rect.contains(pos):  # Если кликнули по кнопке
                self.next_level()  # Переходим на следующий уровень
                return  # Выходим

            main_menu_rect = self.main_menu_button.sceneBoundingRect()  # Границы кнопки "В главное меню"
            if main_menu_rect.contains(pos):  # Если кликнули по кнопке
                self.return_to_main_menu()  # Возвращаемся в главное меню
                return  # Выходим

    def restart_game(self):
        """Полностью перезапускает игру"""
        try:
            self.hide_death_screen()  # Прячем экран смерти
            self.hide_win_screen()  # Прячем экран победы

            # Сбрасываем состояние игрока
            self.player_health = PLAYER_MAX_HEALTH  # Полное здоровье
            self.player_max_health = PLAYER_MAX_HEALTH  # Максимальное здоровье
            self.player_alive = True  # Игрок жив

            # Сбрасываем состояние босса
            self.boss_health = BOSS_MAX_HEALTH  # Полное здоровье босса
            self.boss_max_health = BOSS_MAX_HEALTH  # Максимальное здоровье босса
            self.boss_alive = True  # Босс жив

            # Сбрасываем управление
            self.moving_left = False  # Не движемся влево
            self.moving_right = False  # Не движемся вправо
            self.is_walking = False  # Не ходим
            self.facing_right = True  # Смотрим направо
            self.is_jumping = False  # Не в прыжке
            self.player_velocity_y = 0  # Сбрасываем скорость
            self.on_ground = True  # На земле
            self.jump_buffer = 0  # Сбрасываем буфер прыжка
            self.boss_damage_cooldown = 0  # Сбрасываем перезарядку урона

            # Восстанавливаем позиции
            self.player.setPos(100, self.START_Y)  # Позиция игрока
            boss_x = max(10, min(WINDOW_WIDTH - 110, WINDOW_WIDTH // 2 - 50))  # Позиция босса X
            boss_y = self.FLOOR_Y - 120  # Позиция босса Y
            self.boss.setPos(boss_x, boss_y)  # Устанавливаем позицию босса

            # Восстанавливаем видимость
            self.boss.setVisible(True)  # Показываем босса
            self.boss_label.setVisible(True)  # Показываем надпись
            self.boss_health_background.setVisible(True)  # Показываем фон здоровья
            self.boss_health_bar.setVisible(True)  # Показываем полоску здоровья
            self.boss_health_text.setVisible(True)  # Показываем текст здоровья

            # Восстанавливаем анимацию
            if self.walk_frames:  # Если есть анимации
                self.player.setPixmap(self.walk_frames[0])  # Ставим первый кадр

            # Восстанавливаем интерфейс
            player_name = self.player_data[1] if self.player_data else "Игрок"  # Имя игрока
            self.player_label.setPlainText(player_name)  # Устанавливаем имя
            self.player_label.setDefaultTextColor(QtGui.QColor(255, 255, 0))  # Желтый цвет
            self.boss_label.setPlainText("БОСС")  # Надпись босса
            self.boss_label.setDefaultTextColor(QtGui.QColor(255, 0, 0))  # Красный цвет
            self.player_health_bar.setBrush(QtGui.QBrush(QtGui.QColor(
                PLAYER_HEALTH_BAR_COLOR_R,
                PLAYER_HEALTH_BAR_COLOR_G,
                PLAYER_HEALTH_BAR_COLOR_B
            )))  # Зеленая полоска

            # Очищаем пули
            for bullet_data in self.bullets:  # Перебираем все пули
                self.game_scene.removeItem(bullet_data['item'])  # Удаляем со сцены
            self.bullets = []  # Очищаем список

            # Сбрасываем направление босса
            self.boss_direction = 1  # Движение направо
            self.boss_facing_right = True  # Смотрит направо
            self.boss_velocity_y = 0  # Сбрасываем скорость
            self.boss_on_ground = False  # Не на земле
            self.boss_jump_cooldown = 0  # Сбрасываем перезарядку прыжка

            # Обновляем интерфейс
            self.update_player_health_display()  # Обновляем здоровье игрока
            self.update_boss_health_display()  # Обновляем здоровье босса

        except Exception as e:
            print(f"Ошибка при перезапуске игры: {e}")  # Выводим ошибку

    def next_level(self):
        """Переход на следующий уровень"""
        try:
            message_box = QtWidgets.QMessageBox(self)  # Создаем окно сообщения
            message_box.setWindowTitle("Информация")  # Устанавливаем заголовок
            message_box.setText("Следующий уровень в разработке")  # Устанавливаем текст
            message_box.setIcon(QtWidgets.QMessageBox.Icon.Information)  # Устанавливаем иконку
            message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)  # Добавляем кнопку OK

            message_box.exec()  # Показываем сообщение

        except Exception as e:
            print(f"Ошибка при переходе на следующий уровень: {e}")  # Выводим ошибку
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Произошла ошибка при обработке запроса")  # Показываем ошибку

    def return_to_main_menu(self):
        """Возврат в главное меню из паузы или победы"""
        try:
            self.hide_pause_menu()  # Прячем меню паузы
            self.game_paused = False  # Выключаем паузу

            if self.main_menu_window:  # Если есть ссылка на главное меню
                self.main_menu_window.show()  # Показываем главное меню
                self.close()  # Закрываем игровое окно
            else:
                self.create_new_main_menu()  # Создаем новое главное меню

        except Exception as e:
            print(f"Ошибка при возврате в главное меню: {e}")  # Выводим ошибку

    def return_to_main_menu_from_death(self):
        """Возврат в главное меню с экрана смерти"""
        try:
            self.hide_death_screen()  # Прячем экран смерти

            if self.main_menu_window:  # Если есть ссылка на главное меню
                self.main_menu_window.show()  # Показываем главное меню
                self.close()  # Закрываем игровое окно
            else:
                self.create_new_main_menu()  # Создаем новое главное меню

        except Exception as e:
            print(f"Ошибка при возврате в главное меню с экрана смерти: {e}")  # Выводим ошибку

    def create_new_main_menu(self):
        """Создает новое окно главного меню"""
        try:
            self.close()  # Закрываем текущее окно

            import sys
            from PyQt6 import QtWidgets
            from main_menu_ui import Ui_MainMenuWindow

            # Создаем класс главного меню
            class MainMenuWindow(QtWidgets.QMainWindow, Ui_MainMenuWindow):
                def __init__(self, player_data, db):
                    super().__init__()
                    self.game_window = None  # Пока нет игрового окна
                    self.setupUi(self)  # Настраиваем интерфейс
                    self.player_data = player_data  # Данные игрока
                    self.db = db  # База данных
                    self.player_info_label.setText(f"Игрок: {player_data[1]}")  # Показываем имя игрока
                    self.play_btn.clicked.connect(self.start_game)  # Кнопка "Играть"
                    self.shop_btn.clicked.connect(self.open_shop)  # Кнопка "Магазин"
                    self.profile_btn.clicked.connect(self.open_profile)  # Кнопка "Профиль"
                    self.exit_btn.clicked.connect(self.close)  # Кнопка "Выход"

                def start_game(self):
                    """Запускает новую игру"""
                    from game_engine import GameWindow
                    self.game_window = GameWindow(self.player_data, self.db, self)  # Создаем игровое окно
                    self.game_window.show()  # Показываем игру
                    self.close()  # Закрываем главное меню

                def open_shop(self):
                    """Открывает магазин"""
                    QtWidgets.QMessageBox.information(self, "Магазин", "Магазин скоро будет!")

                def open_profile(self):
                    """Открывает профиль"""
                    QtWidgets.QMessageBox.information(self, "Профиль", "Профиль скоро будет!")

            # Создаем и показываем главное меню
            self.main_menu = MainMenuWindow(self.player_data, self.db)
            self.main_menu.show()

        except Exception as e:
            print(f"Ошибка при создании главного меню: {e}")  # Выводим ошибку

    def closeEvent(self, event):
        """Вызывается когда закрывают окно игры"""
        try:
            if hasattr(self, 'game_timer'):  # Проверяем существует ли таймер
                self.game_timer.stop()

            if hasattr(self, 'animation_timer'):
                self.animation_timer.stop()

            if hasattr(self, 'boss_animation_timer'):
                self.boss_animation_timer.stop()

            event.accept()
        except Exception as e:
            print(f"Ошибка при закрытии окна: {e}")
            event.accept()

    def handle_critical_error(self, context, error):
        """Показывает сообщение об ошибке и выходит из игры"""
        error_msg = f"Критическая ошибка в {context}: {str(error)}"  # Формируем сообщение
        print(error_msg)  # Печатаем в консоль
        traceback.print_exc()  # Печатаем трассировку ошибки

        QtWidgets.QMessageBox.critical(  # Показываем окно ошибки
            None,  # Без родительского окна
            "Критическая ошибка",  # Заголовок
            f"Не удалось запустить игру: {str(error)}"  # Текст ошибки
        )

    def update_boss_ui_positions(self):
        """Обновление позиций UI босса"""
        if not hasattr(self, 'boss') or not self.boss or not self.boss_alive:  # Если босса нет
            return  # Выходим

        boss_x = self.boss.x()  # Позиция босса X
        boss_y = self.boss.y()  # Позиция босса Y

        self.boss_label.setPos(boss_x, boss_y - 80)  # Надпись над боссом
        self.update_boss_health_display()  # Обновляем здоровье

    def update_boss_health_display(self):
        """Обновление отображения здоровья босса"""
        if not hasattr(self, 'boss') or not self.boss or not self.boss_alive:  # Если босса нет
            return  # Выходим

        boss_x = self.boss.x()  # Позиция босса X
        boss_y = self.boss.y()  # Позиция босса Y

        self.boss_health_background.setPos(boss_x - 1, boss_y - 50)  # Фон здоровья
        self.boss_health_bar.setPos(boss_x, boss_y - 49)  # Полоска здоровья

        health_width = (self.boss_health / self.boss_max_health) * 200  # Ширина полоски
        self.boss_health_bar.setRect(0, 0, health_width, 18)  # Устанавливаем ширину

        if hasattr(self, 'boss_health_text'):  # Если есть текст здоровья
            self.boss_health_text.setPlainText(f"{self.boss_health}/{self.boss_max_health}")  # Обновляем текст
            self.boss_health_text.setPos(boss_x + 70, boss_y - 50)  # Позиция текста

    def update_boss_movement(self):
        """Умное движение босса"""
        if not hasattr(self, 'boss') or not self.boss or self.boss_health <= 0 or not self.boss_alive:
            return  # Если босса нет или он мертв

        if self.boss_jump_cooldown > 0:  # Если перезарядка прыжка
            self.boss_jump_cooldown -= 1  # Уменьшаем на 1

        self.boss_navigation_timer += 1  # Увеличиваем таймер навигации

        player_x, player_y = self.player.x(), self.player.y()  # Позиция игрока
        boss_x, boss_y = self.boss.x(), self.boss.y()  # Позиция босса

        player_platform = self.get_platform_at_position(player_x, player_y)  # Платформа игрока
        boss_platform = self.get_platform_at_position(boss_x, boss_y)  # Платформа босса

        if self.boss_navigation_timer >= self.boss_navigation_interval:  # Если пора обновить навигацию
            self.calculate_boss_target(player_x, player_y, boss_x, boss_y, player_platform,
                                       boss_platform)  # Вычисляем цель
            self.boss_navigation_timer = 0  # Сбрасываем таймер

        if self.boss_target_x is not None:  # Если есть цель
            self.execute_boss_movement(boss_x, boss_y, player_x, player_y, boss_platform)  # Выполняем движение

    def get_platform_at_position(self, x, y):
        """Определяет, на какой платформе находится объект"""
        object_bottom = y + 60  # Низ объекта

        for platform in self.platforms:  # Перебираем платформы
            platform_rect = platform.sceneBoundingRect()  # Границы платформы
            if (object_bottom >= platform_rect.top() - 5 and  # Над платформой
                    object_bottom <= platform_rect.top() + 10 and  # Близко к платформе
                    x + 40 > platform_rect.left() and  # В пределах платформы по X
                    x < platform_rect.right()):  # В пределах платформы по X
                return platform  # Возвращаем платформу

        floor_rect = self.floor_line.sceneBoundingRect()  # Границы пола
        if object_bottom >= floor_rect.top() - 5 and object_bottom <= floor_rect.top() + 10:  # Над полом
            return self.floor_line  # Возвращаем пол

        return None  # Не на платформе

    def calculate_boss_target(self, player_x, player_y, boss_x, boss_y, player_platform, boss_platform):
        """Вычисляет целевую позицию для босса"""
        if (player_platform == boss_platform or  # На одной платформе
                (player_platform == self.floor_line and boss_platform == self.floor_line)):  # Оба на полу
            self.boss_target_x = player_x  # Цель - игрок по X
            self.boss_target_y = player_y  # Цель - игрок по Y
            self.boss_state = "chasing"  # Состояние - преследование
            return

        if player_platform and boss_platform:  # Если есть информация о платформах
            player_height = player_platform.sceneBoundingRect().y()  # Высота платформы игрока
            boss_height = boss_platform.sceneBoundingRect().y()  # Высота платформы босса
            height_difference = boss_height - player_height  # Разница высот

            if height_difference > 100:  # Если босс значительно выше
                self.immediate_descent_to_player(player_x, player_y, boss_platform)  # Немедленный спуск
                return
            elif height_difference < -100:  # Если игрок значительно выше
                self.find_platform_to_reach_player(player_x, player_y, boss_platform)  # Ищем платформу для подъема
                return

        self.boss_target_x = player_x  # Цель - игрок по X
        self.boss_target_y = player_y  # Цель - игрок по Y
        self.boss_state = "chasing"  # Состояние - преследование

    def immediate_descent_to_player(self, player_x, player_y, boss_platform):
        """Немедленный спуск к игроку когда босс выше"""
        if boss_platform and boss_platform != self.floor_line:  # Если босс на платформе
            self.boss_target_x = player_x  # Цель - игрок по X
            self.boss_target_y = self.FLOOR_Y - 120  # Цель - низ экрана
            self.boss_state = "jumping"  # Состояние - прыжок

            if self.boss_on_ground and self.boss_jump_cooldown <= 0:  # Если может прыгнуть
                self.jump_towards_player(player_x)  # Прыгаем к игроку
        else:
            self.boss_target_x = player_x  # Цель - игрок по X
            self.boss_target_y = player_y  # Цель - игрок по Y
            self.boss_state = "chasing"  # Состояние - преследование

    def jump_towards_player(self, player_x):
        """Прыжок в направлении игрока"""
        direction = 1 if player_x > self.boss.x() else -1  # Направление к игроку

        self.boss_velocity_y = self.boss_jump_power  # Устанавливаем силу прыжка
        self.boss_on_ground = False  # Больше не на земле
        self.boss_jump_cooldown = self.boss_jump_cooldown_max  # Запускаем перезарядку

        air_move = direction * 30  # Движение в воздухе
        new_x = self.boss.x() + air_move  # Новая позиция X
        new_x = max(BOSS_MOVE_RANGE_LEFT, min(BOSS_MOVE_RANGE_RIGHT, new_x))  # Проверяем границы
        self.boss.setX(new_x)  # Устанавливаем новую позицию

    def find_platform_to_reach_player(self, player_x, player_y, boss_platform):
        """Находит платформу для подъема к игроку"""
        best_platform = None  # Лучшая платформа
        min_distance = float('inf')  # Минимальное расстояние

        for platform in self.platforms:  # Перебираем платформы
            platform_rect = platform.sceneBoundingRect()  # Границы платформы

            if (platform_rect.y() < boss_platform.sceneBoundingRect().y() and  # Выше текущей
                    abs(platform_rect.center().x() - player_x) < 400):  # Не слишком далеко

                distance = abs(platform_rect.center().x() - player_x)  # Расстояние до игрока
                if distance < min_distance:  # Если ближе
                    min_distance = distance  # Обновляем минимальное расстояние
                    best_platform = platform  # Обновляем лучшую платформу

        if best_platform:  # Если нашли платформу
            platform_rect = best_platform.sceneBoundingRect()  # Границы платформы
            self.boss_target_x = platform_rect.center().x()  # Цель - центр платформы по X
            self.boss_target_y = platform_rect.y() - 100  # Цель - над платформой
            self.boss_state = "navigating"  # Состояние - навигация
        else:
            self.boss_target_x = player_x  # Цель - игрок по X
            self.boss_target_y = self.FLOOR_Y - 120  # Цель - низ экрана
            self.boss_state = "chasing"  # Состояние - преследование

    def execute_boss_movement(self, boss_x, boss_y, player_x, player_y, boss_platform):
        """Выполняет движение босса к цели"""
        if self.boss_target_x is None:  # Если нет цели
            return  # Выходим

        direction = 1 if self.boss_target_x > boss_x else -1  # Направление к цели

        current_speed = BOSS_SPEED  # Базовая скорость
        if self.boss_health < 601:  # Если мало здоровья
            current_speed = BOSS_SPEED + BOSS_CHASE_SPEED_BOOST  # Увеличиваем скорость

        # ПРОСТАЯ ЛОГИКА: Если босс выше игрока, двигаться влево или вправо
        # Сравниваем НИЗЫ спрайтов
        boss_bottom = boss_y + 120
        player_bottom = player_y + 60

        # Если босс выше игрока
        if boss_bottom < player_bottom - 50:
            # Когда босс выше, он должен двигаться к КРАЮ платформы для спуска
            if boss_platform and boss_platform != self.floor_line:
                platform_rect = boss_platform.sceneBoundingRect()

                # Определяем к какому краю ближе двигаться
                distance_to_left = abs(boss_x - platform_rect.left())
                distance_to_right = abs(boss_x - platform_rect.right())

                # Двигаться к ближайшему краю
                if distance_to_left < distance_to_right:
                    direction = -1  # Влево к краю
                else:
                    direction = 1  # Вправо к краю
            else:
                # Если на полу, просто двигаться влево
                direction = -1

            new_x = boss_x + direction * current_speed
            new_x = max(BOSS_MOVE_RANGE_LEFT, min(BOSS_MOVE_RANGE_RIGHT, new_x))

            if self.is_safe_position(new_x, boss_y, boss_platform):
                self.boss.setX(new_x)
                self.boss_direction = direction
                self.boss_facing_right = (direction > 0)

            return

        # Обычная логика движения
        if self.boss_state == "chasing":  # Если преследуем
            self.chase_target(boss_x, direction, current_speed, boss_platform)  # Преследуем цель
        elif self.boss_state == "navigating":  # Если навигация
            self.navigate_to_platform(boss_x, boss_y, direction, current_speed, boss_platform)  # Навигация к платформе
        elif self.boss_state == "jumping":  # Если прыжок
            if self.boss_on_ground and self.boss_jump_cooldown <= 0:  # Если может прыгнуть
                self.jump_towards_player(player_x)  # Прыгаем к игроку

        # Атакующие прыжки когда близко к игроку
        if (abs(player_x - boss_x) < 150 and  # Если близко к игроку
                self.boss_on_ground and  # На земле
                self.boss_jump_cooldown <= 0 and  # Может прыгнуть
                random.random() < 0.02):  # 2% шанс
            self.boss_velocity_y = self.boss_jump_power - 5  # Прыжок
            self.boss_on_ground = False  # Больше не на земле
            self.boss_jump_cooldown = self.boss_jump_cooldown_max  # Перезарядка

    def chase_target(self, boss_x, direction, current_speed, boss_platform):
        """Преследование цели по горизонтали"""
        new_x = boss_x + direction * current_speed  # Новая позиция X

        new_x = max(10, min(WINDOW_WIDTH - 110, new_x))  # Проверяем границы

        if self.is_safe_position(new_x, self.boss.y(), boss_platform):  # Если позиция безопасна
            self.boss.setX(new_x)  # Устанавливаем новую позицию
            self.boss_direction = direction  # Обновляем направление
            self.boss_facing_right = (direction > 0)  # Обновляем взгляд

    def navigate_to_platform(self, boss_x, boss_y, direction, current_speed, boss_platform):
        """Навигация к целевой платформе"""
        new_x = boss_x + direction * current_speed  # Новая позиция X
        new_x = max(10, min(WINDOW_WIDTH - 110, new_x))  # Проверяем границы

        if self.is_safe_position(new_x, boss_y, boss_platform):  # Если позиция безопасна
            self.boss.setX(new_x)  # Устанавливаем новую позицию
            self.boss_direction = direction  # Обновляем направление
            self.boss_facing_right = (direction > 0)  # Обновляем взгляд

        # Прыгаем если близко к цели
        target_platform = self.get_platform_at_position(self.boss_target_x, self.boss_target_y)  # Целевая платформа
        if (target_platform and  # Если есть целевая платформа
                self.boss_on_ground and  # На земле
                self.boss_jump_cooldown <= 0 and  # Может прыгнуть
                abs(boss_x - self.boss_target_x) < 200):  # Если близко к цели
            self.jump_towards_target(direction)  # Прыгаем к цели

    def jump_towards_target(self, direction):
        """Прыжок в направлении цели"""
        self.boss_velocity_y = self.boss_jump_power  # Сила прыжка
        self.boss_on_ground = False  # Больше не на земле
        self.boss_jump_cooldown = self.boss_jump_cooldown_max  # Перезарядка

        air_move = direction * 40  # Движение в воздухе
        new_x = self.boss.x() + air_move  # Новая позиция X
        new_x = max(10, min(WINDOW_WIDTH - 110, new_x))  # Проверяем границы
        self.boss.setX(new_x)  # Устанавливаем новую позицию

    def is_safe_position(self, x, y, platform):
        """Проверяет, безопасна ли позиция (не упадем)"""
        if platform == self.floor_line:  # Если на полу
            return True  # Безопасно

        if not platform:  # Если нет информации о платформе
            return True  # Считаем безопасным

        platform_rect = platform.sceneBoundingRect()  # Границы платформы
        # Проверяем остаемся ли на платформе
        return (x + 50 > platform_rect.left() + 15 and  # Не уйдем с левого края
                x < platform_rect.right() - 15)  # Не уйдем с правого края

    def analyze_environment(self):
        """Анализирует окружение и возвращает информацию о платформах"""
        platforms_info = []  # Список для информации о платформах

        for i, platform in enumerate(self.platforms):  # Перебираем платформы
            rect = platform.sceneBoundingRect()  # Границы платформы
            platforms_info.append({  # Добавляем информацию
                'id': i,  # ID платформы
                'x': rect.x(),  # Позиция X
                'y': rect.y(),  # Позиция Y
                'width': rect.width(),  # Ширина
                'height': rect.height(),  # Высота
                'center_x': rect.center().x(),  # Центр по X
                'center_y': rect.center().y(),  # Центр по Y
                'top': rect.top(),  # Верх
                'right': rect.right(),  # Право
                'left': rect.left()  # Лево
            })

        # Добавляем пол как платформу
        floor_rect = self.floor_line.sceneBoundingRect()  # Границы пола
        platforms_info.append({  # Добавляем информацию о поле
            'id': 'floor',  # ID пола
            'x': floor_rect.x(),  # Позиция X
            'y': floor_rect.y(),  # Позиция Y
            'width': floor_rect.width(),  # Ширина
            'height': floor_rect.height(),  # Высота
            'center_x': floor_rect.center().x(),  # Центр по X
            'center_y': floor_rect.center().y(),  # Центр по Y
            'top': floor_rect.top(),  # Верх
            'right': floor_rect.right(),  # Право
            'left': floor_rect.left()  # Лево
        })

        return platforms_info  # Возвращаем информацию

    def can_reach_platform(self, from_platform, to_platform):
        """Проверяет, может ли босс допрыгнуть до платформы"""
        if not from_platform or not to_platform:  # Если нет информации о платформах
            return False  # Не может

        # Вычисляем расстояние между платформами
        distance_x = abs(to_platform['center_x'] - from_platform['center_x'])  # Расстояние по X
        distance_y = from_platform['top'] - to_platform['top']  # Расстояние по Y (положительное - цель ниже)

        max_jump_horizontal = 400  # Максимальное горизонтальное расстояние прыжка
        max_jump_up = 300  # Максимальная высота прыжка вверх
        max_jump_down = 250  # Максимальная высота прыжка вниз

        if distance_x > max_jump_horizontal:  # Если слишком далеко по горизонтали
            return False  # Не может

        if distance_y > 0:  # Если цель ниже
            return distance_y < max_jump_down  # Проверяем дистанцию вниз
        else:  # Если цель выше
            return abs(distance_y) < max_jump_up  # Проверяем дистанцию вверх

    def find_best_platform_to_reach_player(self):
        """Находит лучшую платформу для достижения игрока"""
        player_x, player_y = self.player.x(), self.player.y()  # Позиция игрока
        boss_x, boss_y = self.boss.x(), self.boss.y()  # Позиция босса
        platforms_info = self.analyze_environment()  # Информация о платформах

        player_platform = None  # Платформа игрока
        min_distance_to_player = float('inf')  # Минимальное расстояние

        for platform in platforms_info:  # Перебираем платформы
            # Проверяем находится ли игрок над платформой
            if (player_y + 60 >= platform['top'] - 5 and  # Над платформой
                    player_y + 60 <= platform['top'] + 15 and  # Близко к платформе
                    player_x + 40 > platform['left'] and  # В пределах платформы по X
                    player_x < platform['right']):  # В пределах платформы по X

                distance = abs(platform['center_x'] - player_x)  # Расстояние до игрока
                if distance < min_distance_to_player:  # Если ближе
                    min_distance_to_player = distance  # Обновляем минимальное расстояние
                    player_platform = platform  # Обновляем платформу игрока

        boss_platform = None  # Платформа босса
        for platform in platforms_info:  # Перебираем платформы
            if (boss_y + 120 >= platform['top'] - 5 and  # Над платформой
                    boss_y + 120 <= platform['top'] + 15 and  # Близко к платформе
                    boss_x + 100 > platform['left'] and  # В пределах платформы по X
                    boss_x < platform['right']):  # В пределах платформы по X
                boss_platform = platform  # Нашли платформу босса
                break  # Выходим

        return player_platform, boss_platform  # Возвращаем платформы

    def find_path_to_player(self):
        """Находит путь от босса к игроку через платформы"""
        boss_platform = self.find_boss_platform()  # Платформа босса
        player_platform = self.find_player_platform()  # Платформа игрока

        if boss_platform is None or player_platform is None:  # Если нет информации о платформах
            return []  # Путь не найден

        if boss_platform == player_platform:  # Если на одной платформе
            return [player_platform]  # Путь - текущая платформа

        boss_platform_rect = boss_platform.sceneBoundingRect()  # Границы платформы босса
        player_platform_rect = player_platform.sceneBoundingRect()  # Границы платформы игрока

        if self.can_reach_platform_direct(boss_platform, player_platform):  # Если может допрыгнуть напрямую
            return [player_platform]  # Путь - платформа игрока

        # Ищем промежуточные платформы
        platforms_by_distance = sorted(  # Сортируем платформы по расстоянию до игрока
            self.platforms,
            key=lambda p: abs(p.sceneBoundingRect().center().x() - player_platform_rect.center().x())
        )

        for platform in platforms_by_distance:  # Перебираем платформы
            platform_info = self.get_platform_info(platform)  # Информация о платформе
            if (platform != boss_platform and  # Не текущая платформа босса
                    platform != player_platform and  # Не платформа игрока
                    self.can_reach_platform_direct(boss_platform, platform) and  # Может допрыгнуть до промежуточной
                    self.can_reach_platform_direct(platform, player_platform)):  # Может допрыгнуть до игрока
                return [platform, player_platform]  # Путь через промежуточную платформу

        return []  # Путь не найден

    def find_boss_platform(self):
        """Находит платформу, на которой стоит босс"""
        boss_rect = self.boss.sceneBoundingRect()  # Границы босса
        boss_bottom = boss_rect.bottom()  # Низ босса

        for platform in self.platforms:  # Перебираем платформы
            platform_rect = platform.sceneBoundingRect()  # Границы платформы
            # Проверяем стоит ли босс на платформе
            if (abs(boss_bottom - platform_rect.top()) < 5 and  # Близко к верху платформы
                    boss_rect.right() > platform_rect.left() + 10 and  # В пределах платформы по X
                    boss_rect.left() < platform_rect.right() - 10):  # В пределах платформы по X
                return platform  # Возвращаем платформу

        floor_rect = self.floor_line.sceneBoundingRect()  # Границы пола
        if abs(boss_bottom - floor_rect.top()) < 5:  # Если на полу
            return self.floor_line  # Возвращаем пол

        return None  # Не на платформе

    def find_player_platform(self):
        """Находит платформу, на которой стоит игрок"""
        player_rect = self.player.sceneBoundingRect()  # Границы игрока
        player_bottom = player_rect.bottom()  # Низ игрока

        for platform in self.platforms:  # Перебираем платформы
            platform_rect = platform.sceneBoundingRect()  # Границы платформы
            if (abs(player_bottom - platform_rect.top()) < 5 and  # Близко к верху платформы
                    player_rect.right() > platform_rect.left() + 10 and  # В пределах платформы по X
                    player_rect.left() < platform_rect.right() - 10):  # В пределах платформы по X
                return platform  # Возвращаем платформу

        floor_rect = self.floor_line.sceneBoundingRect()  # Границы пола
        if abs(player_bottom - floor_rect.top()) < 5:  # Если на полу
            return self.floor_line  # Возвращаем пол

        return None  # Не на платформе

    def can_reach_platform_direct(self, from_platform, to_platform):
        """Проверяет, может ли босс допрыгнуть до платформы напрямую"""
        if from_platform is None or to_platform is None:  # Если нет информации
            return False  # Не может

        from_rect = from_platform.sceneBoundingRect()  # Границы исходной платформы
        to_rect = to_platform.sceneBoundingRect()  # Границы целевой платформы

        # Проверяем границы экрана
        if (from_rect.left() < 10 or from_rect.right() > WINDOW_WIDTH - 10 or  # Исходная платформа за границами
                to_rect.left() < 10 or to_rect.right() > WINDOW_WIDTH - 10):  # Целевая платформа за границами
            return False  # Не может

        distance_x = abs(to_rect.center().x() - from_rect.center().x())  # Расстояние по X
        distance_y = from_rect.top() - to_rect.top()  # Расстояние по Y (положительное - цель ниже)

        max_jump_horizontal = 250  # Максимальное горизонтальное расстояние
        max_jump_up = 180  # Максимальная высота прыжка вверх
        max_jump_down = 100  # Максимальная высота прыжка вниз

        if distance_x > max_jump_horizontal:  # Если слишком далеко по горизонтали
            return False  # Не может

        if distance_y > 0:  # Если цель ниже
            return distance_y < max_jump_down  # Проверяем дистанцию вниз
        else:  # Если цель выше
            return abs(distance_y) < max_jump_up  # Проверяем дистанцию вверх

    def get_platform_info(self, platform):
        """Получает информацию о платформе"""
        rect = platform.sceneBoundingRect()  # Границы платформы
        return {  # Возвращаем информацию
            'id': id(platform),  # ID платформы
            'x': rect.x(),  # Позиция X
            'y': rect.y(),  # Позиция Y
            'width': rect.width(),  # Ширина
            'height': rect.height(),  # Высота
            'center_x': rect.center().x(),  # Центр по X
            'center_y': rect.center().y(),  # Центр по Y
            'top': rect.top(),  # Верх
            'right': rect.right(),  # Право
            'left': rect.left()  # Лево
        }

    def chase_player_directly(self, distance_x, abs_distance_x):
        """Прямое преследование игрока на той же платформе"""
        direction = 1 if distance_x > 0 else -1  # Направление к игроку

        current_speed = BOSS_SPEED  # Базовая скорость
        if self.boss_health < 601:  # Если мало здоровья
            current_speed = BOSS_SPEED + 2  # Увеличиваем скорость

        if abs_distance_x > 80:  # Если далеко от игрока
            new_x = self.boss.x() + direction * current_speed  # Новая позиция X
            new_x = max(10, min(WINDOW_WIDTH - 110, new_x))  # Проверяем границы
            self.boss.setX(new_x)  # Устанавливаем позицию
            self.boss_direction = direction  # Обновляем направление
            self.boss_facing_right = (direction > 0)  # Обновляем взгляд

        elif (self.boss_on_ground and  # Если на земле
              self.boss_jump_cooldown <= 0 and  # Может прыгнуть
              random.random() < 0.01):  # 1% шанс прыжка

            self.boss_velocity_y = self.boss_jump_power - 5  # Прыжок
            self.boss_on_ground = False  # Больше не на земле
            self.boss_jump_cooldown = self.boss_jump_cooldown_max  # Перезарядка

    def chase_player_across_platforms(self, player_platform, boss_platform, distance_x, distance_y):
        """Преследование игрока через платформы"""
        player_rect = player_platform.sceneBoundingRect()  # Границы платформы игрока
        boss_rect = boss_platform.sceneBoundingRect()  # Границы платформы босса

        direction = 1 if distance_x > 0 else -1  # Направление к игроку

        # Если босс на земле, а игрок на платформе
        if (boss_platform == self.floor_line and  # Босс на полу
                player_platform != self.floor_line and  # Игрок на платформе
                self.boss_on_ground and  # Босс на земле
                self.boss_jump_cooldown <= 0):  # Может прыгнуть

            self.boss_velocity_y = self.boss_jump_power  # Прыжок
            self.boss_on_ground = False  # Больше не на земле
            self.boss_jump_cooldown = self.boss_jump_cooldown_max  # Перезарядка
            self.boss.setX(self.boss.x() + direction * 30)  # Движение в воздухе
            return

        # Если оба на платформах, но разных
        if (boss_platform != self.floor_line and  # Босс на платформе
                player_platform != self.floor_line and  # Игрок на платформе
                self.boss_on_ground and  # Босс на земле
                self.boss_jump_cooldown <= 0):  # Может прыгнуть

            height_diff = boss_rect.top() - player_rect.top()  # Разница высот
            if abs(height_diff) < 150:  # Если разница высот небольшая
                self.boss_velocity_y = self.boss_jump_power  # Прыжок
                self.boss_on_ground = False  # Больше не на земле
                self.boss_jump_cooldown = self.boss_jump_cooldown_max  # Перезарядка
                self.boss.setX(self.boss.x() + direction * 25)  # Движение в воздухе
                return

        # Если не прыгаем, двигаемся к краю платформы
        boss_x = self.boss.x()  # Позиция босса X
        new_x = boss_x + direction * BOSS_SPEED  # Новая позиция X

        if self.is_position_safe(new_x, self.boss.y(), boss_platform):  # Если позиция безопасна
            self.boss.setX(new_x)  # Устанавливаем позицию
            self.boss_direction = direction  # Обновляем направление
            self.boss_facing_right = (direction > 0)  # Обновляем взгляд

    def is_position_safe(self, x, y, platform):
        """Проверяет, безопасна ли позиция (не упадем с платформы)"""
        if platform == self.floor_line:  # Если на полу
            return True  # Безопасно

        platform_rect = platform.sceneBoundingRect()  # Границы платформы
        # Проверяем остаемся ли на платформе
        return (x + 40 > platform_rect.left() + 10 and  # Не уйдем с левого края
                x < platform_rect.right() - 10)  # Не уйдем с правого края

    def find_multi_level_path(self):
        """Находит многоуровневый путь к игроку через платформы"""
        player_platform, boss_platform = self.find_best_platform_to_reach_player()  # Платформы игрока и босса

        if not player_platform or not boss_platform:  # Если нет информации
            return []  # Путь не найден

        if player_platform['id'] == boss_platform['id']:  # Если на одной платформе
            return [player_platform]  # Путь - текущая платформа

        # Поиск пути с использованием алгоритма поиска в ширину (BFS)
        queue = [(boss_platform, [boss_platform])]  # Очередь для BFS
        visited = set()  # Посещенные платформы
        visited.add(boss_platform['id'])  # Добавляем стартовую платформу

        while queue:  # Пока очередь не пуста
            current_platform, path = queue.pop(0)  # Берем первую платформу из очереди

            if current_platform['id'] == player_platform['id']:  # Если достигли цели
                return path[1:]  # Возвращаем путь без стартовой платформы

            # Ищем все достижимые платформы
            for platform in self.analyze_environment():  # Перебираем все платформы
                if (platform['id'] not in visited and  # Если не посещали
                        self.can_reach_platform(current_platform, platform)):  # И можем достичь
                    visited.add(platform['id'])  # Добавляем в посещенные
                    new_path = path + [platform]  # Новый путь
                    queue.append((platform, new_path))  # Добавляем в очередь

        return []  # Путь не найден

    def advanced_chase(self, player_x, boss_x, player_y, boss_y, current_speed, direction):
        """Улучшенное преследование с поиском ближайшей платформы"""
        best_platform = self.find_closest_platform_in_direction(direction)  # Ближайшая платформа

        if best_platform:  # Если нашли платформу
            platform_direction = 1 if best_platform['center_x'] > boss_x else -1  # Направление к платформе
            new_x = boss_x + platform_direction * current_speed  # Новая позиция X

            if self.is_position_on_boss_platform(new_x):  # Если позиция на платформе
                new_x = max(10, min(WINDOW_WIDTH - 110, new_x))  # Проверяем границы
                self.boss.setX(new_x)  # Устанавливаем позицию
                self.boss_direction = platform_direction  # Обновляем направление
                self.boss_facing_right = (platform_direction > 0)  # Обновляем взгляд

                # Прыгаем на платформу если близко
                if (abs(boss_x - best_platform['center_x']) < 120 and  # Если близко к платформе
                        self.boss_on_ground and  # На земле
                        self.boss_jump_cooldown <= 0 and  # Может прыгнуть
                        self.can_reach_platform(self.boss_platform, best_platform)):  # Может достичь платформу
                    self.jump_to_platform(best_platform)  # Прыгаем на платформу
        else:
            # Простое преследование если не нашли платформу
            if abs(player_x - boss_x) > 50:  # Если далеко от игрока
                new_x = boss_x + direction * current_speed  # Новая позиция X
                new_x = max(10, min(WINDOW_WIDTH - 110, new_x))  # Проверяем границы
                self.boss.setX(new_x)  # Устанавливаем позицию
                self.boss_direction = direction  # Обновляем направление
                self.boss_facing_right = (direction > 0)  # Обновляем взгляд

    def find_closest_platform_in_direction(self, direction):
        """Находит ближайшую платформу в указанном направлении"""
        boss_x, boss_y = self.boss.x(), self.boss.y()  # Позиция босса
        platforms_info = self.analyze_environment()  # Информация о платформах

        best_platform = None  # Лучшая платформа
        min_distance = float('inf')  # Минимальное расстояние

        for platform in platforms_info:  # Перебираем платформы
            if platform['id'] == self.boss_platform['id']:  # Пропускаем текущую платформу
                continue

            platform_x = platform['center_x']  # Центр платформы по X
            distance = abs(platform_x - boss_x)  # Расстояние до платформы

            # Проверяем направление и достижимость
            if ((direction > 0 and platform_x > boss_x) or  # Если движемся вправо и платформа справа
                    (direction < 0 and platform_x < boss_x)):  # Или движемся влево и платформа слева

                if (distance < min_distance and  # Если ближе
                        self.can_reach_platform(self.boss_platform, platform)):  # И можем достичь
                    min_distance = distance  # Обновляем минимальное расстояние
                    best_platform = platform  # Обновляем лучшую платформу

        return best_platform  # Возвращаем лучшую платформу

    def jump_to_platform(self, target_platform):
        """Прыгает к указанной платформе"""
        if not self.boss_on_ground or self.boss_jump_cooldown > 0:  # Если не может прыгнуть
            return  # Выходим

        direction = 1 if target_platform['center_x'] > self.boss.x() else -1  # Направление к платформе

        # Рассчитываем силу прыжка в зависимости от разницы высот
        height_diff = self.boss_platform['top'] - target_platform['top']  # Разница высот
        jump_power = self.boss_jump_power  # Базовая сила прыжка

        # Корректируем силу прыжка
        if height_diff > 100:  # Цель значительно ниже
            jump_power = self.boss_jump_power + 5  # Увеличиваем силу
        elif height_diff < -100:  # Цель значительно выше
            jump_power = self.boss_jump_power - 8  # Уменьшаем силу
        elif height_diff < -50:  # Цель выше
            jump_power = self.boss_jump_power - 4  # Немного уменьшаем силу

        self.boss_velocity_y = jump_power  # Устанавливаем силу прыжка
        self.boss_on_ground = False  # Больше не на земле
        self.boss_jump_cooldown = self.boss_jump_cooldown_max  # Перезарядка

        air_move = direction * 45  # Движение в воздухе
        new_x = self.boss.x() + air_move  # Новая позиция X
        new_x = max(10, min(WINDOW_WIDTH - 110, new_x))  # Проверяем границы
        self.boss.setX(new_x)  # Устанавливаем позицию

    def handle_stuck_situation(self):
        """Обрабатывает ситуацию, когда босс застрял"""
        self.boss_path = []  # Сбрасываем путь
        self.boss_thinking_timer = self.boss_thinking_interval  # Принудительно запускаем пересчет
        self.boss_stuck_timer = 0  # Сбрасываем таймер застревания

        # Случайный прыжок чтобы попытаться выбраться
        if self.boss_on_ground and self.boss_jump_cooldown <= 0:  # Если может прыгнуть
            self.boss_velocity_y = self.boss_jump_power - 5  # Прыжок
            self.boss_on_ground = False  # Больше не на земле
            self.boss_jump_cooldown = self.boss_jump_cooldown_max  # Перезарядка

            air_move = random.choice([-1, 1]) * 30  # Случайное движение в воздухе
            new_x = self.boss.x() + air_move  # Новая позиция X
            new_x = max(10, min(WINDOW_WIDTH - 110, new_x))  # Проверяем границы
            self.boss.setX(new_x)  # Устанавливаем позицию

    def is_position_on_platform(self, rect, platform):
        """Проверяет, находится ли позиция на платформе"""
        platform_rect = platform.sceneBoundingRect()  # Границы платформы
        return (rect.bottom() >= platform_rect.top() - 5 and  # Над платформой
                rect.bottom() <= platform_rect.top() + 5 and  # Близко к платформе
                rect.right() > platform_rect.left() + 10 and  # В пределах платформы по X
                rect.left() < platform_rect.right() - 10)  # В пределах платформы по X

    def is_path_clear(self, start_x, start_y, end_x, end_y):
        """Проверяет, свободен ли путь между двумя точками"""
        check_distance = abs(end_x - start_x)  # Расстояние для проверки

        # Создаем тестовый прямоугольник для проверки коллизий
        test_rect = QtCore.QRectF(
            min(start_x, end_x),  # Левая граница
            min(start_y, end_y) - 50,  # Верхняя граница (немного выше)
            check_distance,  # Ширина
            100  # Высота проверяемой области
        )

        # Проверяем столкновения с платформами
        for platform in self.platforms:  # Перебираем платформы
            platform_rect = platform.sceneBoundingRect()  # Границы платформы
            if test_rect.intersects(platform_rect):  # Если пересекается с платформой
                return False  # Путь заблокирован

        return True  # Путь свободен

    def can_navigate_between(self, platform_a, platform_b):
        """Проверяет, можно ли перепрыгнуть с одной платформы на другую"""
        rect_a = platform_a['rect']  # Границы платформы A
        rect_b = platform_b['rect']  # Границы платформы B

        # Вычисляем расстояния
        distance_x = abs(rect_b.center().x() - rect_a.center().x())  # Расстояние по X
        distance_y = rect_a.top() - rect_b.top()  # Расстояние по Y (положительное - цель ниже)

        # Максимальные дистанции прыжка
        max_jump_horizontal = 300  # Максимальное горизонтальное расстояние
        max_jump_up = 200  # Максимальная высота прыжка вверх
        max_jump_down = 150  # Максимальная высота прыжка вниз

        if distance_x > max_jump_horizontal:  # Если слишком далеко по горизонтали
            return False  # Не может

        if distance_y > 0:  # Если цель ниже
            return distance_y < max_jump_down  # Проверяем дистанцию вниз
        else:  # Если цель выше
            return abs(distance_y) < max_jump_up  # Проверяем дистанцию вверх

    def find_platform_by_position(self, x, y):
        """Находит платформу по позиции объекта"""
        for platform in self.platform_map:  # Перебираем платформы в карте
            rect = platform['rect']  # Границы платформы
            # Проверяем, находится ли объект над платформой и близко к ней
            if (y + 100 >= rect.top() and  # Над платформой
                    y <= rect.bottom() and  # Не под платформой
                    x + 50 > rect.left() and  # В пределах платформы по X
                    x < rect.right()):  # В пределах платформы по X
                return platform  # Возвращаем платформу
        return None  # Не на платформе

