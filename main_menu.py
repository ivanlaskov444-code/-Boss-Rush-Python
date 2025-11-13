from PyQt6 import QtWidgets, QtCore


class Ui_MainMenuWindow(QtWidgets.QMainWindow):
    def __init__(self, player_data, db):
        super().__init__()
        self.player_data = player_data
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Galaxy Jumper")
        self.setFixedSize(1000, 700)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)

        # Простой стиль для теста
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0c29, stop:0.5 #302b63, stop:1 #24243e);
            }
            QLabel {
                color: white;
                font-family: 'Arial';
            }
            QPushButton {
                background: #667eea;
                color: white;
                border: 2px solid white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14pt;
                margin: 5px;
            }
        """)

        # Заголовок
        title = QtWidgets.QLabel("GALAXY JUMPER")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 48pt; color: #ffcc00; margin: 50px;")
        layout.addWidget(title)

        # Информация о игроке
        info = QtWidgets.QLabel(f"Игрок: {self.player_data[1]} | Уровень: {self.player_data[4]}")
        info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("font-size: 16pt; color: #00ffcc;")
        layout.addWidget(info)

        # Кнопки
        play_btn = QtWidgets.QPushButton("🚀 ИГРАТЬ")
        play_btn.clicked.connect(self.start_game)
        layout.addWidget(play_btn)

        shop_btn = QtWidgets.QPushButton("🛍️ МАГАЗИН")
        shop_btn.clicked.connect(self.open_shop)
        layout.addWidget(shop_btn)

        exit_btn = QtWidgets.QPushButton("🚪 ВЫХОД")
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)

        layout.addStretch()

    def start_game(self):
        print("Запуск игры...")

    def open_shop(self):
        print("Открываем магазин...")