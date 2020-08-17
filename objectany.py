from PyQt5.QtWidgets import *
import sqlite3
import style
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
import os


class ObjectAny(QWidget):

    def __init__(self, data, name, window):
        super(ObjectAny, self).__init__()
        self.setWindowTitle("Product")
        self.setGeometry(200, 100, 400, 400)
        self.data = data
        self.__name__ = name
        self.window = window
        self.id = None
        # ############################## Layout >>
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.childBottom = QHBoxLayout()
        self.bottomGroupBox = QGroupBox("Info")
        self.topGroupBox = QGroupBox("Search Box")
        self.topGroupBox.setStyleSheet(style.searchBoxStyle())
        self.middleGroupBox = QGroupBox("List Box")
        self.middleGroupBox.setStyleSheet(style.listBoxStyle())

        # ############################## DataBase >>
        self.db = sqlite3.connect("product_data")
        # ############################## Widget >>
        self.productWidget = QTableWidget()
        self.productWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.radio_1 = QRadioButton("All")
        self.radio_2 = QRadioButton("Available")
        self.radio_3 = QRadioButton("UnAvailable")
        self.searchLabel = QLabel("Search :")
        self.lineEditSearch = QLineEdit()
        self.buttonSearch = QPushButton("Search")
        self.buttonList = QPushButton("List")
        # ################# Button >>
        self.updateButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")

        self.ui()

    def ui(self):
        # ############################### Left Layout >>
        self.leftLayout.addWidget(self.productWidget)
        # ###################################### right Layout >>
        # ################# Top Layout>>
        self.topLayout.addWidget(self.searchLabel, 10)
        self.topLayout.addWidget(self.lineEditSearch, 64)
        self.lineEditSearch.setPlaceholderText("Search for {}".format(self.data))
        self.topLayout.addWidget(self.buttonSearch, 26)
        self.topGroupBox.setLayout(self.topLayout)
        self.rightLayout.addWidget(self.topGroupBox)
        # ##################### Bottom Layout >>
        self.bottomGroupBox.setLayout(self.bottomLayout)
        self.rightLayout.addWidget(self.bottomGroupBox)
        self.childBottom.addStretch()
        self.childBottom.setSpacing(10)
        self.childBottom.addWidget(self.deleteButton)
        self.childBottom.addWidget(self.updateButton)
        self.bottomGroupBox.hide()
        # ############################## Add Layout >>
        self.rightLayout.addStretch()
        self.mainLayout.addLayout(self.leftLayout, 65)
        self.mainLayout.addLayout(self.rightLayout, 35)

        self.setLayout(self.mainLayout)
        # ############################ Triggered Action >>
        self.productWidget.doubleClicked.connect(self.change)
        self.deleteButton.clicked.connect(self.delete_value)
        self.updateButton.clicked.connect(self.change)
        self.buttonSearch.clicked.connect(self.search_item)

        if self.__name__ == "sel":
            self.productWidget.doubleClicked.connect(self.delete_sell)
        elif self.__name__ == "mem":
            self.productWidget.clicked.connect(self.bottom_layout_member)
        elif self.__name__ == "pro":
            self.productWidget.clicked.connect(self.bottom_layout_member)

    def widget(self):
        """
        Show items in table widget and update/delete
        :return:
        """
        self.bottomGroupBox.hide()
        for i in reversed(range(self.productWidget.rowCount())):
            self.productWidget.removeRow(i)

        data = "Select Count(*) from {}".format(self.data)
        rows = self.db.execute(data).fetchone()
        data = "SELECT name FROM pragma_table_info('{}')".format(self.data)
        columns = self.db.execute(data).fetchall()
        count = len(columns)
        self.productWidget.setRowCount(rows[0])
        self.productWidget.setColumnCount(count)
        for i in range(count):
            name = str(columns[i][0])
            self.productWidget.setHorizontalHeaderItem(i, QTableWidgetItem(name.capitalize()))
        # ####################### For Design Member >>
        if self.__name__ == "mem":
            self.productWidget.setColumnHidden(0, True)
            self.productWidget.setColumnHidden(5, True)
            self.productWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.productWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
            self.productWidget.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)

        elif self.__name__ == "pro":
            self.productWidget.setColumnHidden(0, True)
            self.productWidget.setColumnHidden(5, True)
            self.productWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.productWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        elif self.__name__ == "sel":
            self.productWidget.setColumnHidden(0, True)
            self.productWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.productWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
            self.productWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
            self.productWidget.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
            self.show_sell()

        data = "Select id from {}".format(self.data)
        _id = self.db.execute(data).fetchall()
        for i in range(rows[0]):

            txt = "Select * from {} where id=?".format(self.data)
            table = self.db.execute(txt, (_id[i][0],)).fetchone()
            for j in range(count):
                self.productWidget.setItem(i, j, QTableWidgetItem(str(table[j])))

    def data_base(self, txt):
        self.db.execute(txt)

    def change(self):
        if self.productWidget.selectionModel().hasSelection():
            self.id = self.productWidget.item(self.productWidget.currentRow(), 0).text()

        self.window.update_items(int(self.id), self.__name__)

    def bottom_layout_member(self):
        self.bottomGroupBox.show()
        for i in reversed(range(self.bottomLayout.count())):
            if i == 2:
                self.bottomLayout.itemAt(i).layout().setParent(None)
            else:
                self.bottomLayout.itemAt(i).widget().setParent(None)
        self.id = self.productWidget.item(self.productWidget.currentRow(), 0).text()
        if self.__name__ == "mem":
            data = self.db.execute("SELECT name, family, img FROM member where id=?", (int(self.id),)).fetchall()
            name, family, img = data[0]
            name_label = QLabel("{} {}".format(name, family))
        elif self.__name__ == "pro":
            data = self.db.execute("SELECT name, factory, img FROM product where id=?", (int(self.id),)).fetchall()
            name, factory, img = data[0]
            name_label = QLabel("{} {}".format(name, factory))
        elif self.__name__ == "sel":
            pass

        image = QLabel()
        image.setPixmap(QPixmap("img/{}".format(img)).scaled(300, 300, Qt.KeepAspectRatio))
        image.setAlignment(Qt.AlignCenter)
        name_label.setAlignment(Qt.AlignCenter)
        self.bottomLayout.setVerticalSpacing(15)
        self.bottomLayout.addRow(image)
        self.bottomLayout.addRow(name_label)
        self.bottomLayout.addRow(self.childBottom)

    def delete_value(self):
        if self.productWidget.selectionModel().hasSelection():
            self.id = self.productWidget.item(self.productWidget.currentRow(), 0).text()

        m_box = QMessageBox.information(self, "Warning", "You sure delete item?", QMessageBox.Yes | QMessageBox.No)

        if m_box == QMessageBox.Yes:
            txt = "SELECT img FROM {} WHERE id=?".format(self.data)
            img = self.db.execute(txt, (self.id,)).fetchone()
            if self.__name__ == "mem":
                if not img[0] == "person.svg":
                    os.remove("img/{}".format(img[0]))
            elif self.__name__ == "pro":
                if not img[0] == "computer.svg":
                    os.remove("img/{}".format(img[0]))

            txt = """DELETE FROM {} where id=?""".format(self.data)
            self.db.execute(txt, (self.id,))
            self.db.commit()

            self.window.win()
            QMessageBox.information(self, "Info", "Item is deleted")
            self.bottomGroupBox.hide()

    def delete_sell(self):
        if self.productWidget.selectionModel().hasSelection():
            self.id = self.productWidget.item(self.productWidget.currentRow(), 0).text()
            m_box = QMessageBox.information(self, "Warning", "You sure delete item?", QMessageBox.Yes | QMessageBox.No)

            if m_box == QMessageBox.Yes:
                txt = """DELETE FROM sell where id=?""".format(self.data)
                self.db.execute(txt, (self.id,))
                self.db.commit()

                self.widget()
                QMessageBox.information(self, "Info", "Item is deleted")

    def show_sell(self):
        self.bottomGroupBox.show()
        for i in reversed(range(self.bottomLayout.count())):
            self.bottomLayout.itemAt(i).widget().setParent(None)

        customer_count = self.db.execute("Select count(*) from member").fetchone()
        product_count = self.db.execute("Select count(*) from product").fetchone()
        img = "sell.svg"
        name_label = QLabel("Number of Customers : {}".format(customer_count[0]))
        product_label = QLabel("Number of Products : {}".format(product_count[0]))

        image = QLabel()
        image.setPixmap(QPixmap("img/{}".format(img)).scaled(300, 300, Qt.KeepAspectRatio))
        image.setAlignment(Qt.AlignCenter)
        name_label.setAlignment(Qt.AlignCenter)
        product_label.setAlignment(Qt.AlignCenter)
        self.bottomLayout.setVerticalSpacing(15)
        self.bottomLayout.addRow(image)
        self.bottomLayout.addRow(name_label)
        self.bottomLayout.addRow(product_label)

    def search_item(self):

        value = self.lineEditSearch.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search query can not empty")
            self.widget()
        else:
            self.lineEditSearch.setText("")
            if self.__name__ == "mem":
                txt = "select * from {} where name like ? or family like ?".format(self.data)
                data = self.db.execute(txt, ("%" + value + "%", "%" + value + "%")).fetchall()
            elif self.__name__ == "pro":
                txt = "select * from {} where name like ? or factory like ?".format(self.data)
                data = self.db.execute(txt, ("%" + value + "%", "%" + value + "%")).fetchall()
            elif self.__name__ == "sel":
                txt = "select * from {} where name like ? or family like ? or product like ?".format(self.data)
                data = self.db.execute(txt, ("%" + value + "%", "%" + value + "%", "%" + value + "%")).fetchall()
            if not data:
                QMessageBox.information(self, "Warning", "This item does not exist")
            else:
                if not self.__name__ == "sel":
                    self.bottomGroupBox.hide()
                for i in reversed(range(self.productWidget.rowCount())):
                    self.productWidget.removeRow(i)
                rows = len(data)
                self.productWidget.setRowCount(rows)
                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.productWidget.setItem(i, j, QTableWidgetItem(str(column)))
