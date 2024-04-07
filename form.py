# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\funny\OneDrive\Документы\DST_Tools\form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(830, 350)
        MainWindow.setMinimumSize(QtCore.QSize(830, 350))
        MainWindow.setMaximumSize(QtCore.QSize(830, 350))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\Users\\funny\\OneDrive\\Документы\\DST_Tools\\scripts/Icon\'s/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 310, 810, 30))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.progressBar.setObjectName("progressBar")
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(50, 10, 130, 30))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(470, 10, 130, 30))
        self.pushButton2.setObjectName("pushButton2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 50, 810, 250))
        self.plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plainTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plainTextEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.plainTextEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton3.setGeometry(QtCore.QRect(190, 10, 130, 30))
        self.pushButton3.setObjectName("pushButton3")
        self.pushButton4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton4.setGeometry(QtCore.QRect(330, 10, 130, 30))
        self.pushButton4.setObjectName("pushButton4")
        self.pushButton5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton5.setGeometry(QtCore.QRect(750, 10, 30, 30))
        self.pushButton5.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:\\Users\\funny\\OneDrive\\Документы\\DST_Tools\\scripts/Icon\'s/aroow.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton5.setIcon(icon1)
        self.pushButton5.setIconSize(QtCore.QSize(25, 25))
        self.pushButton5.setObjectName("pushButton5")
        self.pushButton6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton6.setGeometry(QtCore.QRect(790, 10, 30, 30))
        self.pushButton6.setMouseTracking(False)
        self.pushButton6.setAcceptDrops(False)
        self.pushButton6.setToolTipDuration(0)
        self.pushButton6.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("C:\\Users\\funny\\OneDrive\\Документы\\DST_Tools\\scripts/Icon\'s/github.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton6.setIcon(icon2)
        self.pushButton6.setIconSize(QtCore.QSize(20, 20))
        self.pushButton6.setObjectName("pushButton6")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(610, 10, 130, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton7.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.pushButton7.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("C:\\Users\\funny\\OneDrive\\Документы\\DST_Tools\\scripts/Icon\'s/folder.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton7.setIcon(icon3)
        self.pushButton7.setObjectName("pushButton7")
        self.pushButton.raise_()
        self.progressBar.raise_()
        self.pushButton1.raise_()
        self.pushButton2.raise_()
        self.plainTextEdit.raise_()
        self.pushButton3.raise_()
        self.pushButton4.raise_()
        self.pushButton5.raise_()
        self.pushButton6.raise_()
        self.pushButton7.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Инструменты переводчика DST"))
        self.pushButton1.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">Обновляет <span style=\" text-decoration: underline;\">DST.po</span> из файла для переводчиков <span style=\" text-decoration: underline;\">strings.pot</span> и<span style=\" font-weight:600;\"> создаёт копию</span> предыдущей версии <span style=\" text-decoration: underline;\">DST.po</span>.</p><p align=\"center\">Файл <span style=\" text-decoration: underline;\">strings.pot</span> подгружается из папки с <span style=\" font-weight:600;\">обновлённой</span> игрой при <span style=\" font-weight:600;\">запуске</span> инструмента.</p></body></html>"))
        self.pushButton1.setText(_translate("MainWindow", "Обновить из strings.pot"))
        self.pushButton2.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">Добавляет <span style=\" font-weight:600;\">все</span> строки из выбранного файла в<span style=\" text-decoration: underline;\"> DST.po.</span></p></body></html>"))
        self.pushButton2.setText(_translate("MainWindow", "Слить файл с DST.po"))
        self.pushButton3.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">Сохраняет строки с <span style=\" font-weight:600;\">отсутствующим переводом</span> в отдельный файл.</p><p align=\"center\">Имеются ввиду все строки, где <span style=\" text-decoration: underline;\">msgstr</span> не содержит в кавычках<span style=\" text-decoration: underline;\"> ничего.</span></p></body></html>"))
        self.pushButton3.setText(_translate("MainWindow", "Сохранить строки"))
        self.pushButton4.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">Ищет ошибки <span style=\" text-decoration: underline;\">структуры</span> выбранного файла, рекомендуется проверять, как файл <span style=\" font-weight:600;\">перед</span> слиянием с <span style=\" text-decoration: underline;\">DST.po</span>, так и сам<span style=\" text-decoration: underline;\"> DST.po </span><span style=\" font-weight:600;\">после</span> слияния.</p></body></html>"))
        self.pushButton4.setText(_translate("MainWindow", "Проверить структуру"))
        self.pushButton5.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">Скопировать <span style=\" text-decoration: underline;\">DST.po</span> из репозитория <span style=\" font-weight:600;\">GitHub.</span></p></body></html>"))
        self.pushButton6.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">Заменить<span style=\" text-decoration: underline;\"> DST.po</span> в локальном репозитории <span style=\" font-weight:600;\">GitHub Desktop.</span></p><p align=\"center\">Так же открывает <span style=\" font-weight:600;\">Github Desktop</span> при нажатии.</p></body></html>"))
        self.pushButton.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">Ищет совпадение строк по <span style=\" text-decoration: underline;\">msgid</span> и заменяет в конечном файле.</p><p align=\"center\">В качестве архива, рекомендуется использовать файл перевода из репозитория, а для заполнения, файл с новыми строками <span style=\" font-weight:600;\">без</span> перевода.</p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Заполнить по msgid"))
        self.pushButton7.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">Открыть рабочую папку.</p></body></html>"))
