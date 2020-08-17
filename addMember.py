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
        self.label = QLabel("Add Contact", self)
        self.img = QLabel(self)
        # ############ child widget for bottom Layout ############
        self.nameLabel = QLabel("Name : ", self)
        self.nameLine = QLineEdit(self)
        self.nameLine.setPlaceholderText(" Enter your name")

        self.familyLabel = QLabel("Family : ", self)
        self.familyLine = QLineEdit(self)
        self.familyLine.setPlaceholderText(" Enter your family")

        self.phoneLabel = QLabel("Phone : ", self)
        self.phoneLine = QLineEdit(self)
        self.phoneLine.setPlaceholderText(" Ex: 0911 123 4567")

        self.emailLabel = QLabel("Email : ", self)
        self.emailLine = QLineEdit(self)
        self.emailLine.setPlaceholderText(" Enter your email")

        self.pictureLabel = QLabel("Picture : ", self)
        self.pictureButton = QPushButton("Upload", self)

        self.addressLabel = QLabel("Address : ", self)
        self.addressTextEdit = QTextEdit(self)
        self.saveAddress = QPushButton("Add", self)

        self.url = None
        self.imgName = None

    def ui(self, name=None):
        self.window.setDisabled(True)
        # ############## add widget bottomLayout ###########
        self.bottomLayout.setVerticalSpacing(15)
        self.bottomLayout.addRow(self.nameLabel, self.nameLine)
        self.bottomLayout.addRow(self.familyLabel, self.familyLine)
        self.bottomLayout.addRow(self.phoneLabel, self.phoneLine)
        self.bottomLayout.addRow(self.emailLabel, self.emailLine)
        self.bottomLayout.addRow(self.pictureLabel, self.pictureButton)
        self.bottomLayout.addRow(self.addressLabel, self.addressTextEdit)
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
            self.img.setPixmap(QPixmap("img/person.svg").scaled(300, 300, Qt.KeepAspectRatio))
        elif name == "update":
            self.saveAddress.setText("Edit")
            self.label.setText("Edit contact")
            self.pictureButton.clicked.connect(self.upload)
            self.saveAddress.clicked.connect(self.up_data)

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
                pix = QPixmap("img/person.svg")
                self.img.setPixmap(pix.scaled(300, 300, Qt.KeepAspectRatio))

    def add_data(self):
        name = self.nameLine.text()
        family = self.familyLine.text()
        phone = self.phoneLine.text()
        email = self.emailLine.text()
        address = self.addressTextEdit.toPlainText()
        file_name = "person.svg"

        if self.url is not None:
            if not self.url[0] == "":
                file_name = os.path.basename(self.url[0])
                file_name = file_name[-3:]
            else:
                file_name = "person.svg"

        if not (name and family and phone) == "":
            self.db = sqlite3.connect("product_data")
            data = self.db.cursor()
            inset = "insert into member(name, family, phone, email, address) values (?,?,?,?,?)"
            data.execute(inset, (name, family, phone, email, address))
            select = "select max(id) from member"
            id_contact = data.execute(select).fetchone()
            update = "update member set img=? where id=?"

            if self.imgName is not None:
                if not file_name == "person.svg":
                    # print(self.imgName)
                    # print(file_name)
                    self.imgName.save("img/{}.{}".format(str(id_contact[0]), file_name))
                    data.execute(update, ("{}.{}".format(id_contact[0], file_name), id_contact[0]))
                else:
                    data.execute(update, (file_name, id_contact[0]))
            else:
                data.execute(update, (file_name, id_contact[0]))

            self.db.commit()
            QMessageBox.information(self, "Info", "Contact has been added")

            self.db.close()
            self.close()
            self.window.win()
        else:
            QMessageBox.information(self, "Warning", "Fields can not empty")

    def up_data(self):
        self.db = sqlite3.connect("product_data")
        file_name = "person.svg"
        if self.url is not None:
            if not self.url[0] == "":
                file_name = os.path.basename(self.url[0])
                file_name = file_name[-3:]
            else:
                file_name = "person.svg"

        if self.imgName is not None:
            if not file_name == "person.svg":
                self.imgName.save("img/{}.{}".format(str(self._id), file_name))
                self.up_img = "{}.{}".format(str(self._id), file_name)
            else:
                self.up_img = file_name
        # else:
        #     self.up_img = file_name

        name = self.nameLine.text()
        family = self.familyLine.text()
        phone = self.phoneLine.text()
        email = self.emailLine.text()
        address = self.addressTextEdit.toPlainText()

        if not (name and family and phone) == "":
            message = QMessageBox.information(self, "Info", "You sure Edit item ?", QMessageBox.Yes | QMessageBox.No)
            if message == QMessageBox.Yes:
                update = "UPDATE member set name=?, family=?,  phone=?, email=?, img=?, address=? WHERE id=?"
                self.db.execute(update, (name, family, phone, email, self.up_img, address, self._id))
                self.db.commit()
                QMessageBox.information(self, "Info", "Contact has been Edited")
                self.flagUpload = False
                self.db.close()
                self.close()
                self.window.win()
        else:
            QMessageBox.information(self, "Warning", "Fields can not empty")

    def update_data(self, _id):
        self.db = sqlite3.connect("product_data")
        data = self.db.execute("SELECT * FROM member where id=?", (int(_id),)).fetchall()
        self._id, name, family, phone, email, self.up_img, address = data[0]

        self.nameLine.setText(name)
        self.familyLine.setText(family)
        self.phoneLine.setText(phone)
        self.emailLine.setText(email)
        pix = QPixmap("img/{}".format(self.up_img))
        self.img.setPixmap(pix.scaled(300, 300, Qt.KeepAspectRatio))
        self.addressTextEdit.setText(address)
