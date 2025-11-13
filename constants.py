import os

"""БАЗОВЫЕ ПУТИ И ДИРЕКТОРИИ"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Базовая директория проекта
SOURCES_DIR = os.path.join(BASE_DIR, "sources")  # Папка с графическими ресурсами
MUSIC_DIR = os.path.join(BASE_DIR, "music")  # Папка с музыкой

# Создаем папки если они не существуют
os.makedirs(SOURCES_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

"""ОСНОВНЫЕ ПАРАМЕТРЫ ОКНА"""
WINDOW_WIDTH = 1200  # Ширина игрового окна
WINDOW_HEIGHT = 800  # Высота игрового окна

"""ФИЗИЧЕСКИЕ ПАРАМЕТРЫ"""
GRAVITY = 0.9  # Сила гравитации (ускорение падения)
JUMP_POWER = -17  # Начальная скорость прыжка (отрицательная - вверх)

"""ПАРАМЕТРЫ ИГРОКА"""
PLAYER_SPEED = 3  # Скорость движения игрока по горизонтали
PLAYER_MAX_HEALTH = 100  # Максимальное здоровье игрока
PLAYER_JUMP_BUFFER_MAX = 10  # Время буфера прыжка (для отзывчивого управления)

"""ПАРАМЕТРЫ БОССА"""
BOSS_SPEED = 2  # Базовая скорость движения босса
BOSS_MAX_HEALTH = 2000  # Максимальное здоровье босса
BOSS_JUMP_POWER = -15  # Сила прыжка босса
BOSS_JUMP_COOLDOWN_MAX = 60  # Время перезарядки прыжка босса
BOSS_MOVE_RANGE_LEFT = 10  # Левая граница движения босса
BOSS_MOVE_RANGE_RIGHT = WINDOW_WIDTH - 50  # Правая граница движения босса
BOSS_DAMAGE = 20  # Урон при столкновении с боссом
BOSS_DAMAGE_COOLDOWN_MAX = 100  # Перезарядка урона босса
BOSS_NAVIGATION_INTERVAL = 30  # Интервал пересчета навигации босса
BOSS_MAX_STUCK_TIME = 120  # Максимальное время застревания босса
BOSS_AGGRESSION_RANGE = 500  # Дистанция агрессии босса
BOSS_ATTACK_RANGE = 150  # Дистанция атаки босса
BOSS_CHASE_SPEED_BOOST = 3  # Увеличение скорости при преследовании

"""СИСТЕМА ПУЛЬ"""
BULLET_SPEED = 10  # Скорость движения пули
BULLET_COOLDOWN_MAX = 36  # Перезарядка между выстрелами
BULLET_DAMAGE = 200  # Урон одной пули

"""ПЛАТФОРМЫ И ОКРУЖЕНИЕ"""
# Данные для создания платформ (x, y, width, height)
PLATFORMS_DATA = [
    (200, 600, 300, 20), (600, 600, 200, 20), (100, 500, 200, 20),
    (500, 500, 150, 20), (800, 500, 180, 20), (300, 400, 250, 20),
    (650, 400, 120, 20), (150, 300, 180, 20), (500, 300, 200, 20),
    (800, 300, 150, 20), (350, 200, 100, 20), (700, 200, 120, 20),
]

# Визуальные параметры платформ
PLATFORM_COLOR_R = 200  # Красный компонент цвета платформ
PLATFORM_COLOR_G = 200  # Зеленый компонент цвета платформ
PLATFORM_COLOR_B = 100  # Синий компонент цвета платформ
PLATFORM_BORDER_COLOR_R = 255  # Красный компонент рамки платформ
PLATFORM_BORDER_COLOR_G = 255  # Зеленый компонент рамки платформ
PLATFORM_BORDER_COLOR_B = 255  # Синий компонент рамки платформ
PLATFORM_BORDER_WIDTH = 2  # Толщина рамки платформ

"""ПАРАМЕТРЫ ПРЫЖКОВ И НАВИГАЦИИ"""
MAX_JUMP_HORIZONTAL = 350  # Максимальное горизонтальное расстояние прыжка
MAX_JUMP_UP = 250  # Максимальная высота прыжка вверх
MAX_JUMP_DOWN = 200  # Максимальная высота прыжка вниз

"""ЦВЕТА ИНТЕРФЕЙСА ИГРОКА"""
PLAYER_LABEL_COLOR_R = 255  # Красный компонент цвета имени игрока
PLAYER_LABEL_COLOR_G = 255  # Зеленый компонент цвета имени игрока
PLAYER_LABEL_COLOR_B = 0  # Синий компонент цвета имени игрока
PLAYER_HEALTH_BG_COLOR_R = 50  # Красный компонент фона здоровья игрока
PLAYER_HEALTH_BG_COLOR_G = 50  # Зеленый компонент фона здоровья игрока
PLAYER_HEALTH_BG_COLOR_B = 50  # Синий компонент фона здоровья игрока
PLAYER_HEALTH_BAR_COLOR_R = 0  # Красный компонент полоски здоровья игрока
PLAYER_HEALTH_BAR_COLOR_G = 255  # Зеленый компонент полоски здоровья игрока
PLAYER_HEALTH_BAR_COLOR_B = 0  # Синий компонент полоски здоровья игрока
PLAYER_HEALTH_TEXT_COLOR_R = 255  # Красный компонент текста здоровья игрока
PLAYER_HEALTH_TEXT_COLOR_G = 255  # Зеленый компонент текста здоровья игрока
PLAYER_HEALTH_TEXT_COLOR_B = 255  # Синий компонент текста здоровья игрока

"""ЦВЕТА ИНТЕРФЕЙСА БОССА"""
BOSS_LABEL_COLOR_R = 255  # Красный компонент надписи босса
BOSS_LABEL_COLOR_G = 0  # Зеленый компонент надписи босса
BOSS_LABEL_COLOR_B = 0  # Синий компонент надписи босса
BOSS_HEALTH_BG_COLOR_R = 50  # Красный компонент фона здоровья босса
BOSS_HEALTH_BG_COLOR_G = 50  # Зеленый компонент фона здоровья босса
BOSS_HEALTH_BG_COLOR_B = 50  # Синий компонент фона здоровья босса
BOSS_HEALTH_BAR_COLOR_R = 255  # Красный компонент полоски здоровья босса
BOSS_HEALTH_BAR_COLOR_G = 0  # Зеленый компонент полоски здоровья босса
BOSS_HEALTH_BAR_COLOR_B = 0  # Синий компонент полоски здоровья босса
BOSS_HEALTH_TEXT_COLOR_R = 255  # Красный компонент текста здоровья босса
BOSS_HEALTH_TEXT_COLOR_G = 255  # Зеленый компонент текста здоровья босса
BOSS_HEALTH_TEXT_COLOR_B = 255  # Синий компонент текста здоровья босса

"""ПАРАМЕТРЫ ПАУЗЫ И МЕНЮ"""
PAUSE_BUTTON_COLOR_R = 255  # Красный компонент кнопки паузы
PAUSE_BUTTON_COLOR_G = 255  # Зеленый компонент кнопки паузы
PAUSE_BUTTON_COLOR_B = 0  # Синий компонент кнопки паузы
PAUSE_BUTTON_ALPHA = 200  # Прозрачность кнопки паузы
PAUSE_OVERLAY_ALPHA = 180  # Прозрачность затемнения при паузе

"""ФАЙЛЫ РЕСУРСОВ"""
PLAYER_IMAGES = ["Pers_1.jpg", "Pers_2.jpg", "Pers_3.jpg"]  # Спрайты анимации игрока
BOSS_IMAGES = ["boss_stop.jpg", "boss_left.jpg", "boss_right.jpg"]  # Спрайты босса
BULLET_IMAGE = "bullet.jpg"  # Изображение пули

"""Пути к звукам"""
SOUNDS_DIR = "sounds"
BULLET_SOUND = "bullet_shot.mp3"

"""РАЗМЕРЫ ГРАФИЧЕСКИХ ЭЛЕМЕНТОВ"""
PLAYER_SPRITE_WIDTH = 40  # Ширина спрайта игрока
PLAYER_SPRITE_HEIGHT = 60  # Высота спрайта игрока
BOSS_SPRITE_WIDTH = 100  # Ширина спрайта босса
BOSS_SPRITE_HEIGHT = 120  # Высота спрайта босса
BULLET_SPRITE_SIZE = 20  # Размер спрайта пули

"""ТАЙМЕРЫ И ИНТЕРВАЛЫ"""
GAME_LOOP_INTERVAL = 16  # Интервал игрового цикла (60 FPS)
PLAYER_ANIMATION_INTERVAL = 200  # Интервал анимации игрока (5 FPS)
BOSS_ANIMATION_INTERVAL = 16  # Интервал анимации босса (60 FPS)

"""СИСТЕМА НАГРАД"""
CREDITS_REWARD = 200  # Количество кредитов за победу над боссом
LEVEL_UP_REWARD = 1  # Количество уровней за победу над боссом

"""КОНСТАНТЫ ДЛЯ GUI И СТИЛЕЙ"""
BUTTON_STYLE_SHEET = """
    QPushButton {
        background-color: #6c757d;
        color: white;
        font-weight: bold;
        border: none;
        padding: 5px;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #5a6268;
    }
"""

"""РАЗМЕРЫ И ШРИФТЫ ДЛЯ ИНТЕРФЕЙСА"""
PHOTO_SIZE = 100  # Размер фото профиля в пикселях
FONT_SIZE_LARGE = 24  # Большой размер шрифта
FONT_SIZE_MEDIUM = 12  # Средний размер шрифта
FONT_SIZE_SMALL = 10  # Малый размер шрифта
MIN_LOGIN_LENGTH = 3  # Минимальная длина логина
MIN_PASSWORD_LENGTH = 4  # Минимальная длина пароля

"""ТЕКСТЫ ДЛЯ ИНТЕРФЕЙСА"""
UI_TEXTS = {
    # Профиль
    'player': "Игрок: {}",
    'coins': "{} монет",
    'level': "Уровень {}",
    'photo_error': "Ошибка\nфото",

    # Ошибки
    'fill_fields': "Заполните все поля!",
    'passwords_not_match': "Пароли не совпадают!",
    'login_too_short': "Логин должен быть не менее 3 символов!",
    'password_too_short': "Пароль должен быть не менее 4 символов!",
    'profile_load_error': "Не удалось загрузить данные профиля",
    'photo_load_error': "Ошибка при загрузке фото",
    'photo_save_error': "Не удалось сохранить фото",
    'shop_open_error': "Не удалось открыть магазин",
    'purchase_error': "Ошибка при покупке товара",
    'apply_error': "Ошибка при применении предмета",
    'balance_update_error': "Ошибка при обновлении баланса",
    'window_close_error': "Ошибка при закрытии окна",
    'game_critical_error': "Критическая ошибка",
    'game_launch_error': "Не удалось запустить игру",

    # Успешные операции
    'account_created': "Аккаунт создан!",
    'success': "Успех",

    # Магазин
    'balance': "Ваш баланс: {} монет",
    'price': "Цена: {} монет",
    'bought': "Куплено",
    'apply': "Применить",
    'buy': "Купить",
    'applied': "Применено",

    # Игра
    'boss': "БОСС",
    'dead': "МЕРТВ",
    'pause': "ПАУЗА",
    'resume': "Продолжить",
    'main_menu': "В главное меню",
    'restart': "Начать заново",
    'play_again': "Сыграть еще",
    'next_level': "Следующий уровень",
    'you_lose': "YOU LOSE",
    'you_win': "YOU WIN!",
    'level_development': "Следующий уровень в разработке",
    'info': "Информация"
}

"""ЗАГОЛОВКИ ОКОН И ДИАЛОГОВ"""
WINDOW_TITLES = {
    'select_photo': "Выберите фото",
    'error': "Ошибка",
    'warning': "Предупреждение",
    'shop': "Магазин",
    'profile': "Профиль"
}

"""ФИЛЬТРЫ ФАЙЛОВ"""
FILE_FILTERS = {
    'images': "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
}

"""СТИЛИ КНОПОК"""
BUTTON_STYLES = {
    'bought': "background-color: lightgray; color: black;",
    'apply': "background-color: green; color: white; font-weight: bold;",
    'buy': "background-color: blue; color: white; font-weight: bold;",
    'default': BUTTON_STYLE_SHEET
}

"""КАТЕГОРИИ МАГАЗИНА"""
SHOP_CATEGORIES = ['player', 'weapon', 'bonus']