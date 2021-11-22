import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.con = sqlite3.connect("coffee.db")
        self.modified = []
        self.titles = None
        self.load_table()
        self.tableWidget.itemChanged.connect(self.item_changed)

    def load_table(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = ['id', 'name', 'sort', 'roast_degree', 'type', 'flavour_description', 'price', 'packing_volume']
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = []

    def item_changed(self, item):
        print(self.titles)
        mod = f'{self.titles[item.column()]} = "{item.text()}"'
        changes = f'id = "{self.tableWidget.item(item.row(), 0).text()}"'
        print(mod)
        print(changes)
        self.modified.append(changes)
        self.modified.append(mod)
        self.save_results()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee\nSET "
            que += self.modified[1] + '\n'
            que += f'WHERE {self.modified[0]}'
            print(que)
            try:
                cur.execute(que)
                self.con.commit()
                self.modified = []
            except Exception as e:
                print(e)
                exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    # sys.excepthook = except_hook
    sys.exit(app.exec())
