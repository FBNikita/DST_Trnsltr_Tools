import sys
import os
from pathlib import Path

import PyQt5

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets
import sys
from shutil import copyfile
import zipfile
import io
import winreg
import datetime
import requests
import configparser
import subprocess

# Преобразуем ui шаблон в python код на лету
f = open(os.path.join(os.path.dirname(__file__), r'form.py'), "w", encoding="utf-8")
uic.compileUi(os.path.join(os.path.dirname(__file__), r'form.ui'), f)
f.close()

import form

def write_error_log(e):
    logf = open('error.log', 'w',encoding="utf-8")
    logf.write(str(e))
    logf.close()
    print(str(e))
    sys.exit(1)


def get_reg(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 322330", 0, winreg.KEY_READ|winreg.KEY_WOW64_64KEY)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except Exception as e:
        write_error_log(e)
        return None

def check_file(str):
    my_file = Path(str)
    try:
        my_abs_path = my_file.resolve()
    except Exception as e:
        write_error_log(e)


class same_msgid(QThread):
    progress = pyqtSignal(int)
    msg = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self,archive_po,bank_po):
        QThread.__init__(self)
        self.archive_po=archive_po
        self.bank_po=bank_po
        
    def __del__(self):
        self.wait()

    def run(self):
        filename1 = self.bank_po
        f1 = io.open(filename1, encoding='utf-8', mode='r')
        text1 = f1.readlines()
        f1.close()
        
        filename2 = self.archive_po
        f2 = io.open(filename2, encoding='utf-8', mode='r')
        text2 = f2.readlines()
        f2.close()
        
        counting = 0
        for ind1,line1 in  enumerate(text1):
            self.progress.emit(int(ind1 * 100/ len(text1)))
            if line1[:5] == 'msgid':
                for ind2, line2 in enumerate(text2):
                    if line1==line2:
                        text1[ind1+1]=text2[ind2+1]
                        counting+=1
                        break

        self.msg.emit(f"Найдено и подставлено строк в {filename1.split('/')[-1]}: " + str(counting))
        self.progress.emit(100)

        f=io.open(filename1, encoding='utf-8',mode='w')
        for lines in text1:
            f.write(lines)
        f.close()
        # self.finished.emit()

class merge_files(QThread):
    progress = pyqtSignal(int)
    msg = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self,DSTpo_path,merging_po):
        QThread.__init__(self)
        self.merging_po=merging_po
        self.DSTpo_path=DSTpo_path

    def __del__(self):
        self.wait()

    def run(self):
        f = io.open(self.DSTpo_path, encoding='utf-8', mode='r+')
        rustext = f.readlines()

        filename = self.merging_po
        pot = io.open(filename, encoding='utf-8', mode='r')
        translated = pot.readlines()
        pot.close()

        counting = 0
        for ind, line in enumerate(translated):
            self.progress.emit(int(ind * 100/ len(translated)))
            if line[:2] == '#.' and translated[ind + 3] != 'msgstr ""\n':
                for ind1, rusline in enumerate(rustext):
                    if rusline == line:
                        # rustext[ind1 + 2] = translated[ind + 2]
                        rustext[ind1 + 3] = translated[ind + 3]
                        counting += 1
                        break

        self.msg.emit("Добавлено новых строк: " + str(counting))
        self.progress.emit(100)
        f.seek(0)
        f.truncate()
        for lines in rustext:
            f.write(lines)
        f.close()
        self.finished.emit()

class add_new_strings(QThread):
    progress = pyqtSignal(int)
    msg = pyqtSignal(str)
    finished = pyqtSignal()
    def __init__(self,stringspo_path,DSTpo_path):
        QThread.__init__(self)
        self.stringspo_path=stringspo_path
        self.DSTpo_path=DSTpo_path

    def __del__(self):
        self.wait()

    def run(self):
        try:
            pot = io.open(self.stringspo_path, encoding='utf-8')
            pottext = pot.readlines()
            pot.close()
            f = io.open(self.DSTpo_path, encoding='utf-8', mode='r+')
            rustext = f.readlines()
            f.close()

            del pottext[:5]
            pottext[0:0]=rustext[:19]
            lastline=0
            for ind, line in enumerate(pottext):
                if line[:2] == '#.':
                    self.progress.emit(int(ind*100/len(pottext)))

                    for x in range(lastline,len(rustext)):
                        if line==rustext[x]:
                            pottext[ind+3]=rustext[x+3]
                            lastline=x+5
                            break



            self.progress.emit(100)
            pottext.extend(rustext[lastline:len(rustext)])
            # f.seek(0, 2)  # go to the end of file
            f = io.open(self.DSTpo_path, encoding='utf-8', mode='w')
            for lines in pottext:
                f.write(lines)
            f.close()
            self.finished.emit()
        except Exception as e:
            write_error_log(e)

class ExampleApp(PyQt5.QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setFixedSize(self.size())
        dst_path=get_reg("InstallLocation")

        self.archive_po=None
        self.bank_po=None
        self.stringspo_path=None
        self.DSTpo_path=None
        self.old_DSTpo_path=None
        # dst_path="D:\SteamLibrary\steamapps\common\Don't Starve Together"
        if dst_path:
            self.DSTpo_path = os.path.join(os.path.dirname(__file__), r'DST.po')
            
            self.old_DSTpo_path = os.path.join(os.path.dirname(__file__), r'old_DST.po')
            
            check_file(self.DSTpo_path)
            check_file(dst_path+r"\data\databundles\scripts.zip")
            
            zscripts=zipfile.ZipFile(dst_path+r"\data\databundles\scripts.zip",'r')
            zscripts.extract(r"scripts/languages/strings.pot",path=os.path.dirname(__file__))
            zscripts.close()
            
            self.stringspo_path = (os.path.dirname(__file__)+ r'\scripts\languages\strings.pot')
            
            check_file(self.stringspo_path)
            self.count_empty()
            # self.plainTextEdit.appendPlainText("Путь до папки с игрой: " + dst_path)
            # self.plainTextEdit.appendPlainText("Путь до strings.pot: "+self.stringspo_path)
            # self.plainTextEdit.appendPlainText("Путь до DST.po: " + self.DSTpo_path)
            self.pushButton.clicked.connect(self.same_msgid)
            self.pushButton1.clicked.connect(self.add_new_strings)
            self.pushButton3.clicked.connect(self.save_empty_strings)
            self.pushButton2.clicked.connect(self.merge_files)
            self.pushButton4.clicked.connect(self.check_struct)
            self.pushButton5.clicked.connect(self.download_dst_from_github)
            self.pushButton6.clicked.connect(self.github_button)
            self.pushButton7.clicked.connect(self.open_project)
        else:
            write_error_log(Exception("Не найден ключ реестра"))
            
    def open_project(self):
        os.system(f"explorer {os.path.dirname(__file__)}")
        
    def github_button(self):
        try:
            config = configparser.ConfigParser()
            config.read("scripts/config.ini", encoding="utf-8")
            
            path_to_gh_repo = config.get("DEFAULT", "PATH_TO_GITHUB_REPO")

            if not os.path.exists(path_to_gh_repo):
                raise Exception()
            copyfile(self.DSTpo_path, path_to_gh_repo+'DST.po')
            
            if config.getboolean("DEFAULT", "OPEN_GITHUB"):
                os.system("github " + path_to_gh_repo)
                
            self.add_log_line("DST.po помещён в локальный репозиторий RLP")
            self.add_log_line("Открытие Github Desktop")
        except:
            # QMessageBox.warning(self, "Ошибка!", "Отсутствует файл scripts\config.ini")
            self.add_log_line("Ошибка! Отсутствует файл scripts\config.ini")
            
        
    def download_dst_from_github(self):
        with open(self.DSTpo_path, "w",encoding="utf-8") as f:
            f.write(requests.get("https://raw.githubusercontent.com/CunningFox146/RLP/master/DST.po").text)
        os.startfile(__file__)
        sys.exit()

        
    def same_msgid(self):
        filename1 = self.openFileNameDialog(file_open_dialog_text="Выберите файл для поиска строк:", default_filename="old_DST.po")
        if not filename1:
            return None
        filename2 = self.openFileNameDialog(file_open_dialog_text="Выберите файл для размещения строк:", default_filename="ClearStrocks.po")
        if not filename2:
            return None
        self.same_msgid_thread = same_msgid(filename1,filename2)
        self.same_msgid_thread.progress.connect(self.update_progress)
        self.same_msgid_thread.msg.connect(self.add_log_line)
        self.same_msgid_thread.finished.connect(self.count_empty)
        self.same_msgid_thread.start()

    def check_struct(self):
        filename = self.openFileNameDialog()
        if not filename:
            return None
        f = io.open(filename, encoding='utf-8', mode='r')
        rustext = f.readlines()
        f.close()
        for ind, rusline in enumerate(rustext):

            if rusline[:2] == '#.':
                idline = rusline[3:].rstrip()
                if idline not in rustext[ind + 1]:
                    self.add_log_line("\nid mismatch:")
                    self.add_log_line(str(ind) + " " + rustext[ind].strip())
                    self.add_log_line(str(ind + 1) + " " + rustext[ind + 1].strip())

                msgctxt = "msgctxt "
                if rustext[ind + 1][:len(msgctxt)] != msgctxt:
                    self.add_log_line("\nmsgctxt not found:")
                    self.add_log_line(str(ind) + " " + rustext[ind].strip())
                    self.add_log_line(str(ind + 1) + " " + rustext[ind + 1].strip())

                msgid = "msgid "
                if rustext[ind + 2][:len(msgid)] != msgid:
                    self.add_log_line("\nmsgid not found:")
                    self.add_log_line(str(ind) + " " + rustext[ind].strip())
                    self.add_log_line(str(ind + 1) + " " + rustext[ind + 1].strip())
                    self.add_log_line(str(ind + 2) + " " + rustext[ind + 2].strip())

                msgstr = "msgstr "
                # if '%' in rustext[ind + 3] and not ('%s' in rustext[ind + 3] or '%d' in rustext[ind + 3] or '% ' in rustext[ind + 3] or r'%\n' in rustext[ind + 3]):
                #     self.add_log_line("\nlonely '%' sign:")
                #     self.add_log_line(str(ind) + " " + rustext[ind + 3].strip())

                if rustext[ind + 3][:len(msgstr)] != msgstr:
                    self.add_log_line("\nmsgstr not found:")
                    self.add_log_line(str(ind) + " " + rustext[ind].strip())
                    self.add_log_line(str(ind + 1) + " " + rustext[ind + 1].strip())
                    self.add_log_line(str(ind + 2) + " " + rustext[ind + 2].strip())
                    self.add_log_line(str(ind + 3) + " " + rustext[ind + 3].strip())

                if len(rustext) > ind + 4 and rustext[ind + 4] != '\n':
                    self.add_log_line("\nmissing newline:")
                    self.add_log_line(str(ind) + " " + rustext[ind].strip())
                    self.add_log_line(str(ind + 1) + " " + rustext[ind + 1].strip())
                    self.add_log_line(str(ind + 2) + " " + rustext[ind + 2].strip())
                    self.add_log_line(str(ind + 3) + " " + rustext[ind + 3].strip())
                    self.add_log_line(str(ind + 4) + " " + rustext[ind + 4].strip())
        self.add_log_line("Проверено")

    def count_empty(self):
        f = io.open(self.DSTpo_path, encoding='utf-8', mode='r+')
        pottext = f.readlines()
        f.close()
        counter = -1
        for ind, line in enumerate(pottext):
            if line == 'msgstr ""\n':
                counter += 1
        self.add_log_line("Строки, требующие перевода: " + str(counter))

    def merge_files(self):
        filename = self.openFileNameDialog()
        if not filename:
            return None
        self.merge_files_thread = merge_files(self.DSTpo_path,filename)
        self.merge_files_thread.progress.connect(self.update_progress)
        self.merge_files_thread.msg.connect(self.add_log_line)
        self.merge_files_thread.finished.connect(self.count_empty)
        self.merge_files_thread.start()

    def add_new_strings(self):
        copyfile(self.DSTpo_path, self.old_DSTpo_path)
        self.new_strings_thread = add_new_strings(self.stringspo_path,self.DSTpo_path)
        self.new_strings_thread.progress.connect(self.update_progress)
        self.new_strings_thread.msg.connect(self.add_log_line)
        self.new_strings_thread.finished.connect(self.count_empty)
        self.new_strings_thread.start()
        self.plainTextEdit.appendPlainText("Обновление DST.po")


    def update_progress(self, val):
        self.progressBar.setValue(val)

    def add_log_line(self,str):
        self.plainTextEdit.appendPlainText(str)

    def save_empty_strings(self):
        f = io.open(self.DSTpo_path, encoding='utf-8', mode='r')
        rustext = f.readlines()
        f.close()


        toadd = []
        search4 = "#. STRINGS."
        for ind, line in enumerate(rustext):
            if line[:len(search4)] == search4:
                if rustext[ind + 3] == 'msgstr ""\n':
                    toadd.extend(rustext[ind:ind + 5])
        filename=os.path.join(os.path.dirname(__file__), f"ClearStrocks_{datetime.datetime.now().strftime('%d.%m.%Y')}.po")
        if filename:
            pot = io.open(filename, encoding='utf-8', mode='w')
            pot.seek(0)
            pot.truncate()
            for lines in toadd:
                pot.write(lines)
            pot.close()
            self.add_log_line("Файл сохранён")

    def openFileNameDialog(self, file_open_dialog_text="Выберите файл", default_filename=""):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, file_open_dialog_text, default_filename,"All Files (*)", options=options)
        if fileName:
            return  fileName
        return  None

    def saveFileDialog(self):
        dialog=QFileDialog()
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = dialog.getSaveFileName(self,"Сохранить в отдельный файл","","Pot Files (*.pot)", options=options)
        if fileName:
            if fileName[-4:]!=".pot":
                fileName+='.pot'
            return  fileName
        return  None



def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()