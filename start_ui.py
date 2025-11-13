from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_StartWindow(object):
    def setupUi(self, StartWindow):
        StartWindow.setObjectName("StartWindow")
        StartWindow.setEnabled(True)
        StartWindow.resize(371, 287)
        StartWindow.setBaseSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(parent=StartWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Создаем вертикальный layout для центрирования элементов
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Добавляем растягивающее пространство сверху
        self.verticalSpacer_top = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                                        QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer_top)

        self.Name_game = QtWidgets.QLabel(parent=self.centralwidget)
        self.Name_game.setBaseSize(QtCore.QSize(10, 10))
        font = QtGui.QFont()
        font.setFamily("Rockwell Extra Bold")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.Name_game.setFont(font)
        self.Name_game.setObjectName("Name_game")
        # Выравнивание текста по центру
        self.Name_game.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.Name_game)

        # Добавляем пространство между названием и кнопками
        self.verticalSpacer_middle = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer_middle)

        self.Login = QtWidgets.QPushButton(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Login.setFont(font)
        self.Login.setObjectName("Login")
        self.verticalLayout.addWidget(self.Login)

        self.Register = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Register.setObjectName("Register")
        self.verticalLayout.addWidget(self.Register)

        # Добавляем растягивающее пространство снизу
        self.verticalSpacer_bottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer_bottom)

        StartWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=StartWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 371, 21))
        self.menubar.setObjectName("menubar")
        StartWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=StartWindow)
        self.statusbar.setObjectName("statusbar")
        StartWindow.setStatusBar(self.statusbar)

        self.retranslateUi(StartWindow)
        QtCore.QMetaObject.connectSlotsByName(StartWindow)

    def retranslateUi(self, StartWindow):
        _translate = QtCore.QCoreApplication.translate
        StartWindow.setWindowTitle(_translate("StartWindow", "MainWindow"))
        self.Name_game.setText(_translate("StartWindow", "BossRush"))
        self.Login.setText(_translate("StartWindow", "Войти"))
        self.Register.setText(_translate("StartWindow", "Зарегистрироваться"))