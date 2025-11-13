# Основные методы инициализации:
def __init__(self, player_data, db, main_menu_window=None):
    # Конструктор класса, инициализирует игровое окно

def initialize_game_state(self):
    # Настройка начального состояния игры (здоровье, флаги, управление)

def setup_game_window(self):
    # Настройка основного окна игры (размер, заголовок, позиционирование)

def center_window(self):
    # Центрирование окна на экране

def create_game_scene(self):
    # Создание игровой сцены QGraphicsScene

def create_game_objects(self):
    # Создание игровых объектов (окружение, персонажи)

def setup_ui_elements(self):
    # Настройка UI элементов (кнопки, меню, экраны)

def setup_game_mechanics(self):
    # Настройка игровой механики (таймеры, физика)

# Методы создания игровых объектов:
def create_environment(self):
    # Создание игрового окружения (пол, платформы)

def create_floor(self):
    # Создание пола уровня

def create_platforms(self):
    # Создание всех платформ уровня

def create_single_platform(self, x, y, width, height):
    # Создание одной конкретной платформы

def load_game_assets(self):
    # Загрузка игровых ресурсов (анимации, изображения)

def load_player_animations(self):
    # Загрузка анимаций игрока

def create_fallback_player_animation(self):
    # Создание запасной анимации если файлы не найдены

def load_boss_animations(self):
    # Загрузка анимаций босса

def create_fallback_boss_animation(self):
    # Создание запасной анимации босса

def load_bullet_image(self):
    # Загрузка изображения пули

def create_fallback_bullet(self):
    # Создание запасного изображения пули

def create_characters(self):
    # Создание персонажей игры (игрок и босс)

def create_player(self):
    # Создание игрока и его UI

def create_fallback_player(self):
    # Создание запасного игрока если анимации не загружены

def create_player_ui(self):
    # Создание UI игрока (имя, здоровье)

def create_player_health_bar(self):
    # Создание полоски здоровья игрока

def create_boss(self):
    # Создание босса и его UI

def create_fallback_boss(self):
    # Создание запасного босса

def create_boss_ui(self):
    # Создание UI босса

def create_boss_health_bar(self):
    # Создание полоски здоровья босса

# Методы UI и интерфейса:
def create_pause_button(self):
    # Создание кнопки паузы

def create_pause_menu(self):
    # Создание меню паузы

def create_overlay(self):
    # Создание темного полупрозрачного фона для меню

def create_text_item(self, text, font_size, color, x, y, z_value):
    # Создание текстового элемента

def create_pause_buttons(self):
    # Создает кнопки для меню паузы

def create_menu_button(self, text, color, x, y):
    # Создает одну кнопку для любого меню

def create_death_screen(self):
    # Создание экрана смерти

def create_death_buttons(self):
    # Создает кнопки для экрана смерти

def create_win_screen(self):
    # Создание экрана победы

def create_win_buttons(self):
    # Создает кнопки для экрана победы

# Игровые механики и основной цикл:
def setup_timers(self):
    # Настройка игровых таймеров (геймплей, анимации)

def game_loop(self):
    # Основной игровой цикл (вызывается каждый кадр)

def update_cooldowns(self):
    # Уменьшает все таймеры перезарядки

def handle_player_movement(self):
    # Обрабатывает движение игрока влево-вправо

def handle_jump(self):
    # Обрабатывает прыжки и гравитацию

def check_collisions(self):
    # Проверяет столкновения игрока с полом и платформами

def check_floor_collision(self, player_rect):
    # Проверяет, стоит ли игрок на полу

def check_platform_collisions(self, player_rect, current_y):
    # Проверяет столкновения со всеми платформами

def is_colliding_with_platform(self, player_rect, platform_rect, current_y):
    # Проверяет столкновение с конкретной платформой

# Система стрельбы и пуль:
def update_bullets(self):
    # Обновляет все пули на экране

def check_bullet_boss_collision(self, bullet):
    # Проверяем, столкнулась ли пуля с боссом

def create_bullet(self):
    # Создает новую пулю когда игрок стреляет

# Система босса и AI:
def update_boss_gravity(self):
    # Обновление гравитации для босса

def check_boss_collisions(self):
    # Проверка коллизий босса с полом и платформами

def check_player_boss_collision(self):
    # Проверяет, столкнулся ли игрок с боссом

def update_boss_movement(self):
    # Умное движение босса с AI

def get_platform_at_position(self, x, y):
    # Определяет, на какой платформе находится объект

def calculate_boss_target(self, player_x, player_y, boss_x, boss_y, player_platform, boss_platform):
    # Вычисляет целевую позицию для босса

def immediate_descent_to_player(self, player_x, player_y, boss_platform):
    # Немедленный спуск к игроку когда босс выше

def jump_towards_player(self, player_x):
    # Прыжок в направлении игрока

def find_platform_to_reach_player(self, player_x, player_y, boss_platform):
    # Находит платформу для подъема к игроку

def execute_boss_movement(self, boss_x, boss_y, player_x, player_y, boss_platform):
    # Выполняет движение босса к цели

def is_safe_position(self, x, y, platform):
    # Проверяет, безопасна ли позиция (не упадем)

def analyze_environment(self):
    # Анализирует окружение и возвращает информацию о платформах

def can_reach_platform(self, from_platform, to_platform):
    # Проверяет, может ли босс допрыгнуть до платформы

def find_best_platform_to_reach_player(self):
    # Находит лучшую платформу для достижения игрока

def find_path_to_player(self):
    # Находит путь от босса к игроку через платформы

def find_boss_platform(self):
    # Находит платформу, на которой стоит босс

def find_player_platform(self):
    # Находит платформу, на которой стоит игрок

def can_reach_platform_direct(self, from_platform, to_platform):
    # Проверяет, может ли босс допрыгнуть до платформы напрямую

def get_platform_info(self, platform):
    # Получает информацию о платформе

def chase_player_directly(self, distance_x, abs_distance_x):
    # Прямое преследование игрока на той же платформе

def chase_player_across_platforms(self, player_platform, boss_platform, distance_x, distance_y):
    # Преследование игрока через платформы

def is_position_safe(self, x, y, platform):
    # Проверяет, безопасна ли позиция (не упадем с платформы)

def find_multi_level_path(self):
    # Находит многоуровневый путь к игроку через платформы

def advanced_chase(self, player_x, boss_x, player_y, boss_y, current_speed, direction):
    # Улучшенное преследование с поиском ближайшей платформы

def find_closest_platform_in_direction(self, direction):
    # Находит ближайшую платформу в указанном направлении

def jump_to_platform(self, target_platform):
    # Прыгает к указанной платформе

def handle_stuck_situation(self):
    # Обрабатывает ситуацию, когда босс застрял

def is_position_on_platform(self, rect, platform):
    # Проверяет, находится ли позиция на платформе

def is_path_clear(self, start_x, start_y, end_x, end_y):
    # Проверяет, свободен ли путь между двумя точками

def can_navigate_between(self, platform_a, platform_b):
    # Проверяет, можно ли перепрыгнуть с одной платформы на другую

def find_platform_by_position(self, x, y):
    # Находит платформу по позиции объекта

def chase_target(self, boss_x, direction, current_speed, boss_platform):
    # Преследование цели по горизонтали

def navigate_to_platform(self, boss_x, boss_y, direction, current_speed, boss_platform):
    # Навигация к целевой платформе

def jump_towards_target(self, direction):
    # Прыжок в направлении цели

# Система здоровья и состояний:
def player_take_damage(self, damage):
    # Наносит урон игроку

def player_die(self):
    # Обработка смерти игрока

def boss_defeated(self):
    # Обработка победы над боссом

def hide_boss(self):
    # Скрытие босса и его UI

# Анимации и визуальные эффекты:
def update_animation(self):
    # Обновление анимации игрока

def update_boss_animation(self):
    # Обновление анимации босса

# UI обновления и позиционирования:
def update_ui_positions(self):
    # Обновление позиций UI элементов

def update_player_ui_positions(self):
    # Обновление позиций UI игрока

def update_player_health_display(self):
    # Обновление отображения здоровья игрока

def update_boss_ui_positions(self):
    # Обновление позиций UI босса

def update_boss_health_display(self):
    # Обновление отображения здоровья босса

# Управление игровыми состояниями:
def toggle_pause(self):
    # Включает или выключает паузу

def show_pause_menu(self):
    # Показывает меню паузы

def hide_pause_menu(self):
    # Прячет меню паузы

def show_death_screen(self):
    # Показывает экран смерти

def hide_death_screen(self):
    # Скрыть экран смерти

def show_win_screen(self):
    # Показывает экран победы

def hide_win_screen(self):
    # Прячет экран победы

# Обработка ввода пользователя:
def keyPressEvent(self, event):
    # Вызывается когда нажимают клавишу

def keyReleaseEvent(self, event):
    # Вызывается когда отпускают клавишу

def mousePressEvent(self, event):
    # Вызывается когда кликают мышкой

# Управление игровыми сессиями:
def restart_game(self):
    # Полностью перезапускает игру

def next_level(self):
    # Переход на следующий уровень

def return_to_main_menu(self):
    # Возврат в главное меню из паузы или победы

def return_to_main_menu_from_death(self):
    # Возврат в главное меню с экрана смерти

def create_new_main_menu(self):
    # Создает новое окно главного меню

# Системные методы:
def closeEvent(self, event):
    # Вызывается когда закрывают окно игры

def handle_critical_error(self, context, error):
    # Показывает сообщение об ошибке и выходит из игры

def initialize_platform_map(self):
    # Инициализация карты платформ для навигации AI