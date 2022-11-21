import sys
import sqlite3
from PyQt5.QtWidgets import QTableWidgetItem, QApplication
from UI.main import Ui_MainWindow
from UI.addEditCoffeeForm import Ui_Dialog


class LatteMacchiato(Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.con = sqlite3.connect('./data/latte macchiato db.db')
        res = self.con.cursor().execute('SELECT * FROM coffee').fetchall()
        self.table.setColumnCount(len(res[0]))
        self.table.setRowCount(len(res))
        self.table.setHorizontalHeaderLabels(['ИД', 'Название сорта', 'Степень обжарки', 'Молотый/В зернах',
                                              'Описание вкуса', 'Цена', 'Объем упаковки'])
        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                if j == 2:
                    roast = self.con.cursor().execute(f'SELECT name FROM roasts WHERE id = {elem}').fetchone()[0]
                    self.table.setItem(i, j, QTableWidgetItem(roast))
                elif j == 3:
                    if elem == 1:
                        self.table.setItem(i, j, QTableWidgetItem('Молотый'))
                    elif elem == 2:
                        self.table.setItem(i, j, QTableWidgetItem('В зернах'))
                else:
                    self.table.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()

        self.add_btn.clicked.connect(self.add)
        self.edit_btn.clicked.connect(self.edit)

    def add(self):
        dialog = AddEditCoffeeForm()
        dialog.exec()
        if dialog.clicked:
            cur = self.con.cursor()
            cur.execute(
                'INSERT INTO coffee (variety, roasting_id, ground_or_grains, taste_description, price, '
                f'packing_volume) VALUES ("{dialog.variety}", (SELECT id FROM roasts WHERE name = "{dialog.roasting}"),'
                f' {dialog.ground_or_grains}, "{dialog.taste_description}", {dialog.price}, {dialog.packing_volume})')
            self.con.commit()
            res = cur.execute('SELECT * FROM coffee').fetchall()
            self.table.setRowCount(len(res))
            for i, row in enumerate(res):
                for j, elem in enumerate(row):
                    if j == 2:
                        roast = self.con.cursor().execute(f'SELECT name FROM roasts WHERE id = {elem}').fetchone()[0]
                        self.table.setItem(i, j, QTableWidgetItem(roast))
                    elif j == 3:
                        if elem == 1:
                            self.table.setItem(i, j, QTableWidgetItem('Молотый'))
                        elif elem == 2:
                            self.table.setItem(i, j, QTableWidgetItem('В зернах'))
                    else:
                        self.table.setItem(i, j, QTableWidgetItem(str(elem)))
            self.table.resizeColumnsToContents()
            cur.close()
            self.update()

    def edit(self):
        dialog = AddEditCoffeeForm()
        dialog.exec()
        if dialog.clicked:
            cur = self.con.cursor()
            cur.execute(
                f'UPDATE coffee SET variety = "{dialog.variety}", roasting_id = (SELECT id FROM roasts WHERE name = '
                f'"{dialog.roasting}"), ground_or_grains = {dialog.ground_or_grains}, taste_description = '
                f'"{dialog.taste_description}", price = {dialog.price}, packing_volume = {dialog.packing_volume} '
                f'WHERE id = {self.table.currentRow() + 1}')
            self.con.commit()
            res = cur.execute('SELECT * FROM coffee').fetchall()
            for i, row in enumerate(res):
                for j, elem in enumerate(row):
                    if j == 2:
                        roast = self.con.cursor().execute(f'SELECT name FROM roasts WHERE id = {elem}').fetchone()[0]
                        self.table.setItem(i, j, QTableWidgetItem(roast))
                    elif j == 3:
                        if elem == 1:
                            self.table.setItem(i, j, QTableWidgetItem('Молотый'))
                        elif elem == 2:
                            self.table.setItem(i, j, QTableWidgetItem('В зернах'))
                    else:
                        self.table.setItem(i, j, QTableWidgetItem(str(elem)))
            self.table.resizeColumnsToContents()
            cur.close()
            self.update()


class AddEditCoffeeForm(Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.clicked = False
        self.confirm_btn.clicked.connect(self.click)

    def click(self):
        self.clicked = True
        self.variety = self.variety_line_edit.text()
        self.roasting = self.roasting_combo_box.currentText()
        self.ground_or_grains = 1 if self.ground_or_grains_combo_box.currentText() == 'Молотый' else 2
        self.taste_description = self.taste_description_line_edit.text()
        self.price = self.price_spinbox.value()
        self.packing_volume = self.packing_volume_spinbox.value()
        self.close()


app = QApplication(sys.argv)
ex = LatteMacchiato()
ex.show()
sys.exit(app.exec())
