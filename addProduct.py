from PyQt5.QtWidgets import *
import sqlite3
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PIL import Image
import os


class Member(QWidget):

    def __init__(self, window):
        super(Member, self).__init__()
        self.window = window
        self.setWindowTitle("Add Member")
        self.setGeometry(700, 150, 350, 450)
        # ############# Flags ###########
        self._id = None
        self.up_img = None
        self.flagUpload = False
        # ############## Data base ##############
        self.db = sqlite3.connect("product_data")
        # ############### Layouts #####################
        self.mainLayout = QVBoxLayout()
        self.saveLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topLayout = QVBoxLayout()
        # ############ child widget for top Layout ############
        self.label = QLabel("Add Product", self)
        self.img = QLabel(self)
        # ############ child widget for bottom Layout ############
        self.nameLabel = QLabel("Name Product : ", self)
        self.nameLine = QLineEdit(self)
        self.nameLine.setPlaceholderText(" Enter your name Product")

        self.factoryLabel = QLabel("Factory : ", self)
        self.factoryLine = QLineEdit(self)
        self.factoryLine.setPlaceholderText(" Enter Factory Product")

        self.priceLabel = QLabel("Price : ", self)
        self.priceLine = QLineEdit(self)
        self.priceLine.setPlaceholderText(" Enter Price Product")

        self.quantityLabel = QLabel("Quantity : ", self)
        self.quantityLine = QComboBox(self)

        self.pictureLabel = QLabel("Picture : ", self)
        self.pictureButton = QPushButton("Upload", self)

        self.saveAddress = QPushButton("Add", self)

        self.url = None
        self.imgName = None

    def ui(self, name=None):
        self.window.setDisabled(True)
        # ############## add widget bottomLayout ###########
        self.bottomLayout.setVerticalSpacing(15)
        self.bottomLayout.addRow(self.nameLabel, self.nameLine)
        self.bottomLayout.addRow(self.factoryLabel, self.factoryLine)
        self.bottomLayout.addRow(self.priceLabel, self.priceLine)
        self.bottomLayout.addRow(self.quantityLabel, self.quantityLine)
        self.bottomLayout.addRow(self.pictureLabel, self.pictureButton)
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
        self.topLayout.addWidget(self.label)
        self.topLayout.addWidget(self.img)
        if name == "add":
            self.pictureButton.clicked.connect(self.upload)
            self.saveAddress.clicked.connect(self.add_data)
            self.img.setPixmap(QPixmap("img/computer.svg").scaled(300, 300, Qt.KeepAspectRatio))
        elif name == "update":
            self.saveAddress.setText("Edit")
            self.label.setText("Edit Product")
            self.pictureButton.clicked.connect(self.upload)
            self.saveAddress.clicked.connect(self.up_data)
    # ################### Combo Box >>
        for i in range(100):
            self.quantityLine.addItem(str(i))

        self.setLayout(self.mainLayout)

    def closeEvent(self, event):
        self.window.win()
        self.db.close()

    def upload(self):
        self.url = QFileDialog.getOpenFileName(self, "Open file", "", "Images File (*.jpg *.png)")

        if self.url is not None:
            if not self.url[0] == "":
                self.imgName = Image.open(self.url[0])
                pix = QPixmap(self.url[0])
                self.img.setPixmap(pix.scaled(300, 300, Qt.KeepAspectRatio))
            else:
                pix = QPixmap("img/computer.svg")
                self.img.setPixmap(pix.scaled(300, 300, Qt.KeepAspectRatio))

    def add_data(self):
        name = self.nameLine.text()
        factory = self.factoryLine.text()
        price = self.priceLine.text()
        quantity = self.quantityLine.currentText()
        file_name = "computer.svg"

        if self.url is not None:
            if not self.url[0] == "":
                file_name = os.path.basename(self.url[0])
                file_name = file_name[-3:]
            else:
                file_name = "person.svg"

        if not (name and factory and price) == "":

            try:
                int(price)

                self.db = sqlite3.connect("product_data")
                data = self.db.cursor()
                inset = "insert into product(name, factory, price, quantity) values (?,?,?,?)"
                data.execute(inset, (name, factory, price, quantity))
                select = "select max(id) from product"
                id_contact = data.execute(select).fetchone()
                update = "update product set img=? where id=?"

                if self.imgName is not None:
                    if not file_name == "computer.svg":
                        # print(self.imgName)
                        # print(file_name)
                        self.imgName.save("img/p{}.{}".format(str(id_contact[0]), file_name))
                        data.execute(update, ("p{}.{}".format(id_contact[0], file_name), id_contact[0]))
                    else:
                        data.execute(update, (file_name, id_contact[0]))
                else:
                    data.execute(update, (file_name, id_contact[0]))

                self.db.commit()
                QMessageBox.information(self, "Info", "Product has been added")

                self.db.close()
                self.close()
                self.window.win()

            except ValueError:
                QMessageBox.information(self, "Warning", "If should be the value Price of the integer")

        else:
            QMessageBox.information(self, "Warning", "Fields can not empty")

    def up_data(self):
        self.db = sqlite3.connect("product_data")
        file_name = "computer.svg"
        if self.url is not None:
            if not self.url[0] == "":
                file_name = os.path.basename(self.url[0])
                file_name = file_name[-3:]
            else:
                file_name = "computer.svg"

        if self.imgName is not None:
            if not file_name == "computer.svg":
                # print("'{}'-'{}'".format(self._id, file_name))
                self.imgName.save("img/p{}.{}".format(str(self._id), file_name))
                self.up_img = "p{}.{}".format(str(self._id), file_name)
            else:
                self.up_img = file_name
        # else:
        #     self.up_img = file_name

        name = self.nameLine.text()
        factory = self.factoryLine.text()
        price = self.priceLine.text()
        quantity = self.quantityLine.currentText()

        if not (name and factory and price) == "":

            try:
                int(price)

                message = QMessageBox.information(self, "Info", "You sure Edit item ?",
                                                  QMessageBox.Yes | QMessageBox.No)
                if message == QMessageBox.Yes:
                    update = "UPDATE product set name=?, factory=?,  price=?, quantity=?, img=? WHERE id=?"
                    self.db.execute(update, (name, factory, price, quantity, self.up_img, self._id))
                    self.db.commit()
                    QMessageBox.information(self, "Info", "Product has been Edited")
                    self.flagUpload = False
                    self.db.close()
                    self.close()
                    self.window.win()

            except ValueError:
                QMessageBox.information(self, "Warning", "If should be the value Price of the integer")

        else:
            QMessageBox.information(self, "Warning", "Fields can not empty")

    def update_data(self, _id):
        self.db = sqlite3.connect("product_data")
        data = self.db.execute("SELECT * FROM product where id=?", (int(_id),)).fetchall()
        self._id, name, factory, price, quantity, self.up_img = data[0]

        self.nameLine.setText(name)
        self.factoryLine.setText(factory)
        self.priceLine.setText(price)
        for i in range(100):
            self.quantityLine.addItem(str(i))
        self.quantityLine.setCurrentText(quantity)
        pix = QPixmap("img/{}".format(self.up_img))
        self.img.setPixmap(pix.scaled(300, 300, Qt.KeepAspectRatio))
