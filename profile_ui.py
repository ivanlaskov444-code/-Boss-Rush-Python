from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_ProfileWindow(object):
    def setupUi(self, ProfileWindow):
        ProfileWindow.setObjectName("ProfileWindow")
        ProfileWindow.resize(500, 500)  # Увеличили высоту для фото
        ProfileWindow.setMinimumSize(QtCore.QSize(500, 500))
        ProfileWindow.setMaximumSize(QtCore.QSize(500, 500))

        self.centralwidget = QtWidgets.QWidget(ProfileWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Заголовок профиля
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(0, 20, 500, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("title_label")

        # Фото профиля
        self.photo_label = QtWidgets.QLabel(self.centralwidget)
        self.photo_label.setGeometry(QtCore.QRect(200, 70, 100, 100))
        self.photo_label.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.photo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setText("Фото")
        self.photo_label.setObjectName("photo_label")

        # Кнопка выбора фото
        self.select_photo_btn = QtWidgets.QPushButton(self.centralwidget)
        self.select_photo_btn.setGeometry(QtCore.QRect(175, 180, 150, 30))
        self.select_photo_btn.setObjectName("select_photo_btn")

        # Фрейм для информации
        self.info_frame = QtWidgets.QFrame(self.centralwidget)
        self.info_frame.setGeometry(QtCore.QRect(50, 220, 400, 200))
        self.info_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.info_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.info_frame.setObjectName("info_frame")

        # Никнейм
        self.nickname_label = QtWidgets.QLabel(self.info_frame)
        self.nickname_label.setGeometry(QtCore.QRect(20, 30, 150, 25))
        self.nickname_label.setObjectName("nickname_label")

        self.nickname_value = QtWidgets.QLabel(self.info_frame)
        self.nickname_value.setGeometry(QtCore.QRect(180, 30, 200, 25))
        self.nickname_value.setObjectName("nickname_value")

        # Пароль
        self.password_label = QtWidgets.QLabel(self.info_frame)
        self.password_label.setGeometry(QtCore.QRect(20, 70, 150, 25))
        self.password_label.setObjectName("password_label")

        self.password_value = QtWidgets.QLabel(self.info_frame)
        self.password_value.setGeometry(QtCore.QRect(180, 70, 200, 25))
        self.password_value.setObjectName("password_value")

        # Монеты
        self.credits_label = QtWidgets.QLabel(self.info_frame)
        self.credits_label.setGeometry(QtCore.QRect(20, 110, 150, 25))
        self.credits_label.setObjectName("credits_label")

        self.credits_value = QtWidgets.QLabel(self.info_frame)
        self.credits_value.setGeometry(QtCore.QRect(180, 110, 200, 25))
        self.credits_value.setObjectName("credits_value")

        # Уровень
        self.level_label = QtWidgets.QLabel(self.info_frame)
        self.level_label.setGeometry(QtCore.QRect(20, 150, 150, 25))
        self.level_label.setObjectName("level_label")

        self.level_value = QtWidgets.QLabel(self.info_frame)
        self.level_value.setGeometry(QtCore.QRect(180, 150, 200, 25))
        self.level_value.setObjectName("level_value")

        # Кнопка закрытия
        self.close_btn = QtWidgets.QPushButton(self.centralwidget)
        self.close_btn.setGeometry(QtCore.QRect(200, 430, 100, 30))
        self.close_btn.setObjectName("close_btn")

        ProfileWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ProfileWindow)
        QtCore.QMetaObject.connectSlotsByName(ProfileWindow)

    def retranslateUi(self, ProfileWindow):
        _translate = QtCore.QCoreApplication.translate
        ProfileWindow.setWindowTitle(_translate("ProfileWindow", "Профиль игрока"))
        self.title_label.setText(_translate("ProfileWindow", "ПРОФИЛЬ ИГРОКА"))
        self.select_photo_btn.setText(_translate("ProfileWindow", "Выбрать фото"))
        self.nickname_label.setText(_translate("ProfileWindow", "Никнейм:"))
        self.password_label.setText(_translate("ProfileWindow", "Пароль:"))
        self.credits_label.setText(_translate("ProfileWindow", "Количество монет:"))
        self.level_label.setText(_translate("ProfileWindow", "Уровень:"))
        self.close_btn.setText(_translate("ProfileWindow", "Закрыть"))