import csv

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QPushButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor
import sqlite3

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from predict_utils import predict_status

numeric = [1, 2, 7, 10, 13, 14]
category = [0, 3, 4, 5, 6, 7, 8, 9, 11, 12]
items = {0: ['b', 'a', '-'], 3:['u','y', '-'],
                 4: ['g', 'p', '-'],
                 5: ['c', 'q', 'w', 'i', 'aa', 'ff', 'k', 'cc', 'x', 'm', 'd', 'e', 'j', '-'],
                 6: ['v', 'h', 'bb', 'ff', 'j', 'z', 'dd' , '-'],
                 8: ['t', 'f'], 9: ['f', 't'], 11: ['f', 't'], 12: ['g', 's', 'p'],}
stats = {1: 28.46, 2: 2.75, 7: 1.0, 10: 0.0, 13: 160.0, 14: 5.0}
fname = 'data/test.csv'
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Кредит beta-версия")

        self.setMinimumSize(QSize(1000, 600))
        self.label = QLabel(self)
        self.label.setText('ID заявки: ')
        self.label.resize(130, 30)
        self.label.move(10, 10)

        self.red = QColor(220, 150, 150)
        self.green = QColor(220, 220, 150)

        self.newrec = QPushButton(self)
        self.newrec.setText('Новая заявка')
        self.newrec.resize(130, 30)
        self.newrec.move(310, 10)
        self.newrec.clicked.connect(self.add_rec)
        
        self.edit = QLineEdit(self)
        self.edit.move(100, 10)
        self.edit.resize(200, 30)
        self.edit.setText("")
        self.edit.textChanged.connect(self.search)

        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.resize(980, 540)
        self.table.move(10, 50)
        recs = []
        with open(fname, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            arr = list(reader)
            for el in arr:
                id_rec = int(el['ID'][2:])
                if id_rec not in recs:
                    recs.append(id_rec)
            
            self.table.setColumnCount(len(arr[0].keys()))
            self.table.setHorizontalHeaderLabels(arr[0].keys())
        self.id_rec = max(recs) # для номера новой записи   
        self.search()

    def search(self):
        self.table.setRowCount(0)
        with open(fname, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            arr = list(reader)
            numRows = 0
            text = self.edit.text()
            
            for el in arr:
                col = 0
                self.table.insertRow(numRows)
                if text.lower() in el['ID'].lower():
                    for key in el.keys():
                        self.table.setItem(numRows, col, QTableWidgetItem(str(el[key])))
                        col += 1
                    if el['V'] == '+':
                        color = self.green
                    else:
                        color = self.red
                    for i in range(len(el.keys())):
                        self.table.item(numRows, i).setBackground(color)
                    numRows += 1
            self.table.resizeColumnsToContents()

    def add_rec(self):
        self.id_rec = self.id_rec + 1
        new_id = 'IR' + str(self.id_rec).zfill(6)
        #self.edit.setText(new_id)
        self.win_add = WindowAdd()
        self.win_add.show()

    def get_new_rec_id(self):
        return 'IR' + str(self.id_rec).zfill(6)

        
class WindowAdd(QMainWindow):
    def __init__(self):
        super(WindowAdd, self).__init__()
        self.setWindowTitle('Новая заявка')
        self.setMinimumSize(QSize(500, 300))
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)      # Устанавливаем центральный виджет
        self.grid_layout = QGridLayout()                # Создаём QGridLayout
        self.central_widget.setLayout(self.grid_layout)
        
        self.lbs = QLabel(self)
        self.lbs.setText('ID заявки: ' + mw.get_new_rec_id())
        self.lbs.resize(60, 25)
        self.grid_layout.addWidget(self.lbs, 0, 0, 1, 2)
        self.status = QLabel(self)
        self.status.setText('Статус заявки: ?')
        self.status.resize(60, 25)
        self.grid_layout.addWidget(self.status, 0, 3, 1, 1)
        
                
        self.X_arr = []
        for i in range(5):
            for j in range(3):
                x = QLabel(self)
                n = 3*i + j
                t = 'X' + str(3*i + j) + ':  '
                x.setText(t)
                x.resize(30, 25)
                self.grid_layout.addWidget(x, 2*i + 1, 2*j)
                if n in numeric:
                    y = QLineEdit(self)
                    if n in stats:
                        y.setText(str(stats[n]))
                        y.textChanged.connect(self.edit_rec)
                else:
                    y = QComboBox(self)
                    # настройка ComboBox
                    if n in items:
                        for item in items[n]:
                            y.addItem(item)
                    
                y.resize(30, 25)
                self.grid_layout.addWidget(y, 2*i + 1, 2*j + 1)
                self.X_arr.append(y)
        self.btn_save = QPushButton(self)
        self.btn_save.resize(100, 25)
        self.btn_save.setText('Сохранить заявку')
        self.btn_save.setEnabled(False)
        self.grid_layout.addWidget(self.btn_save, 12, 0, 1, 6)
        self.btn_save.clicked.connect(self.save_rec)
        
        self.btn_check = QPushButton(self)
        self.btn_check.resize(60, 25)
        self.btn_check.setText('Проверить')
        self.grid_layout.addWidget(self.btn_check, 0, 4, 1, 2)
        self.btn_check.clicked.connect(self.check_rec)

    def check_rec(self):
        self.new_rec = []
        for i in range(15):
            if i in numeric:
                val = self.X_arr[i].text()
                if val == '':
                    val = stats[i]
                self.new_rec.append(float(val))
            elif i in category:
                val = self.X_arr[i].currentText()
                if val == '-':
                    val = 'nan'
                self.new_rec.append(val)
        self.status_rec = predict_status(self.new_rec)[0]
        if self.status_rec == 0:
            self.status.setText('Статус заявки: NO')
        else:
            self.status.setText('Статус заявки: OK')
        self.btn_save.setEnabled(True)
        self.btn_check.setEnabled(False)
        
    def edit_rec(self):
        self.btn_save.setEnabled(False)
        self.btn_check.setEnabled(True)
        self.status.setText('Статус заявки: ?')

    def save_rec(self):
        new_id = 'IR' + str(mw.id_rec).zfill(6)
        status = '+'
        if self.status_rec == 0:
            status = '-'
        
        with open(fname, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            arr = list(reader)
        fieldnames = arr[0].keys()
        new_rec = [str(len(arr))] + [new_id] + [str(x) for x in self.new_rec] + [status]
        new_rec = dict(zip(fieldnames, new_rec))
        #print(new_rec)
        
        with open(fname, "w", newline='') as out_file:
            writer = csv.DictWriter(out_file, delimiter=',',fieldnames=fieldnames )
            writer.writeheader()
            for row in arr:
                writer.writerow(row)
            #print(row)
            writer.writerow(new_rec)
        mw.win_add.close()
        mw.edit.setText(new_id)
        mw.search()
                
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())

