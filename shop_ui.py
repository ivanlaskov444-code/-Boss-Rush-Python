from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ShopWindow(object):
    def setupUi(self, ShopWindow):
        ShopWindow.setObjectName("ShopWindow")
        ShopWindow.resize(800, 700)
        ShopWindow.setMinimumSize(QtCore.QSize(800, 700))
        ShopWindow.setMaximumSize(QtCore.QSize(800, 700))

        self.centralwidget = QtWidgets.QWidget(ShopWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Заголовок
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(0, 10, 800, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("title_label")

        # Баланс
        self.balance_label = QtWidgets.QLabel(self.centralwidget)
        self.balance_label.setGeometry(QtCore.QRect(0, 50, 800, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.balance_label.setFont(font)
        self.balance_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.balance_label.setObjectName("balance_label")

        # Вкладки
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setGeometry(QtCore.QRect(20, 90, 760, 500))
        self.tabs.setObjectName("tabs")

        # Вкладка улучшений игрока
        self.player_tab = QtWidgets.QWidget()
        self.player_tab.setObjectName("player_tab")
        self.tabs.addTab(self.player_tab, "Улучшения игрока")

        # Вкладка улучшений оружия
        self.weapon_tab = QtWidgets.QWidget()
        self.weapon_tab.setObjectName("weapon_tab")
        self.tabs.addTab(self.weapon_tab, "Улучшения оружия")

        # Вкладка бонусов
        self.bonus_tab = QtWidgets.QWidget()
        self.bonus_tab.setObjectName("bonus_tab")
        self.tabs.addTab(self.bonus_tab, "Бонусы")

        # Кнопка закрытия
        self.close_btn = QtWidgets.QPushButton(self.centralwidget)
        self.close_btn.setGeometry(QtCore.QRect(350, 610, 100, 30))
        self.close_btn.setObjectName("close_btn")

        ShopWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ShopWindow)
        QtCore.QMetaObject.connectSlotsByName(ShopWindow)

    def retranslateUi(self, ShopWindow):
        _translate = QtCore.QCoreApplication.translate
        ShopWindow.setWindowTitle(_translate("ShopWindow", "Магазин улучшений"))
        self.title_label.setText(_translate("ShopWindow", "МАГАЗИН УЛУЧШЕНИЙ"))
        self.balance_label.setText(_translate("ShopWindow", "Ваш баланс: 1000 монет"))
        self.tabs.setTabText(self.tabs.indexOf(self.player_tab), _translate("ShopWindow", "Улучшения игрока"))
        self.tabs.setTabText(self.tabs.indexOf(self.weapon_tab), _translate("ShopWindow", "Улучшения оружия"))
        self.tabs.setTabText(self.tabs.indexOf(self.bonus_tab), _translate("ShopWindow", "Бонусы"))
        self.close_btn.setText(_translate("ShopWindow", "Закрыть"))