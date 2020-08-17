from PyQt5.QtWidgets import *
import sqlite3
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *


class Sell(QWidget):

    def __init__(self, window):
        super(Sell, self).__init__()
        self.window = window
        self.setWindowTitle("Sell Product")
        self.setGeometry(700, 150, 350, 450)
        self.mem = None
        self.pro = None
        # ############## Data base ##############
        self.db = sqlite3.connect("product_data")
        # ############### Layouts #####################
        self.mainLayout = QVBoxLayout()
        self.saveLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topLayout = QVBoxLayout()
        # ############ child widget for top Layout ############
        self.label = QLabel("Select Product", self)
        self.img = QLabel(self)
        # ############ child widget for bottom Layout ############
        self.nameProductLabel = QLabel("Select Product : ", self)
        self.nameProductCombo = QComboBox(self)

        self.nameMemberLabel = QLabel("Select Customer : ", self)
        self.customerCombo = QComboBox(self)

        self.quantityLabel = QLabel("Quantity : ", self)
        self.quantityLine = QComboBox(self)

        self.saveAddress = QPushButton("Sell", self)

    def ui(self):
        self.window.setDisabled(True)
        # ############## add widget bottomLayout ###########
        self.bottomLayout.setVerticalSpacing(15)
        self.bottomLayout.addRow(self.nameMemberLabel, self.customerCombo)
        self.bottomLayout.addRow(self.nameProductLabel, self.nameProductCombo)
        self.bottomLayout.addRow(self.quantityLabel, self.quantityLine)
        # ################ Set Layout for save button
        self.saveLayout.addWidget(self.saveAddress)

        self.bottomLayout.addRow(self.saveLayout)
        # ############ add Layout to mainLayout ##############
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        # ############### add widget topLayout ###########
        self.label.setAlignment(Qt.AlignCenter)
        self.img.setStyleSheet("border:2px solid grey;")
        self.img.setAlignment(Qt.AlignCenter)
        self.img.setPixmap(QPixmap("img/sell.svg").scaled(300, 300, Qt.KeepAspectRatio))
        self.topLayout.addWidget(self.label)
        self.topLayout.addWidget(self.img)
        self.saveAddress.clicked.connect(self.add_data)

        self.setLayout(self.mainLayout)
        # ######################### Show items in Layout >>
        self.mem = self.db.execute("""SELECT id, name, family FROM member""").fetchall()
        self.pro = self.db.execute("""SELECT id, name FROM product""").fetchall()
        for i in range(len(self.mem)):
            self.customerCombo.addItem("{} {} {}".format(self.mem[i][0], self.mem[i][1], self.mem[i][2]))

        for i in range(len(self.pro)):
            self.nameProductCombo.addItem("{} {}".format(self.pro[i][0], self.pro[i][1]))
        # ######################## index changed >>
        self.nameProductCombo.currentTextChanged.connect(self.show_quantity)
        self.show_quantity()

    def show_quantity(self):
        ls = self.nameProductCombo.currentText().split(" ")
        num = self.db.execute("SELECT quantity FROM product WHERE id=?", (ls[0],)).fetchone()
        self.quantityLine.clear()
        if not (len(self.mem) and len(self.pro)) == 0:
            self.show()
            if not num[0] == "0":
                for i in range(1, int(num[0]) + 1):
                    self.quantityLine.addItem(str(i))
            else:
                self.quantityLine.addItem("0")
        else:
            QMessageBox.information(self, "Warning", "the Product Or Customer is empty")
            self.close()
            self.window.win()

    def closeEvent(self, event):
        self.window.win()
        self.db.close()

    def add_data(self):
        product = self.nameProductCombo.currentText().split(" ")
        txt = self.customerCombo.currentText().split(" ")
        name_family = self.db.execute("select name, family from member where id=?", (int(txt[0]), )).fetchone()
        quantity = self.quantityLine.currentText()
        if not quantity == "0":

            self.db = sqlite3.connect("product_data")
            data = self.db.cursor()

            txt = "SELECT price,quantity FROM product WHERE id=?"
            value = data.execute(txt, (product[0],)).fetchone()
            amount = int(value[0]) * int(quantity)
            new_quantity = int(value[1]) - int(quantity)

            inset = "insert into sell(name, family, product, price, quantity, amount) values (?,?,?,?,?,?)"
            data.execute(inset, (name_family[0], name_family[1], product[1], value[0], quantity, amount))

            # ########################## Update Quantity product >>
            update = "UPDATE product set quantity=? WHERE id=?"
            self.db.execute(update, (new_quantity, product[0]))

            self.db.commit()
            txt_2 = """The product was sold
             {} x {} = {}""".format(value[0], quantity, amount)
            QMessageBox.information(self, "Info", txt_2)

            self.db.close()
            self.close()
            self.window.win()

        else:
            QMessageBox.information(self, "Warning", "the Product Unavailable")
