import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import objectany
import qdarkstyle
from PyQt5.QtGui import QFont
import addMember
import addProduct
import addSell
from PyQt5.QtCore import Qt


class Main(QWidget):

    def __init__(self):
        super(Main, self).__init__()
        # ####################### Main Window #########################
        self.setGeometry(300, 100, 1020, 670)
        self.setWindowTitle("Product Manager  V0.1")
        self.main = QVBoxLayout()
        self.setWindowIcon(QIcon("icon/computer.svg"))
        # ######################## Switch Widows oder >>
        self.member = None
        self.product = None
        self.sell = None
        self.tab1 = None
        self.tab2 = None
        self.tab3 = None
        # ######################### Tool Bar ########################
        self.toolBar = QToolBar("ToolBar", self)
        self.addProduct = QAction(QIcon("icon/product.svg"), "Add Product", self)
        self.addMember = QAction(QIcon("icon/followers.svg"), "Add Member", self)
        self.sellProduct = QAction(QIcon("icon/sell.svg"), "Sell Product", self)

        # ######################## Tab widget ######################
        self.tabs = QTabWidget(self)

        self.ui()

    def ui(self):
        self.tool_bar()
        self.tab_widget()
        self.setLayout(self.main)

    def tool_bar(self):
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # ################## Add Product ############################
        self.toolBar.addAction(self.addProduct)
        self.toolBar.addSeparator()
        # ################## Add Member #############################
        self.toolBar.addAction(self.addMember)
        self.toolBar.addSeparator()
        # ################# Sell Product ###########################
        self.toolBar.addAction(self.sellProduct)
        # ################### Triggered Action >>
        self.addMember.triggered.connect(self.add_member)
        self.addProduct.triggered.connect(self.add_product)
        self.sellProduct.triggered.connect(self.add_sell)

        self.main.addWidget(self.toolBar)

    def tab_widget(self):
        # ######################## Tab 1>>
        self.tab1 = objectany.ObjectAny("product", "pro", self)
        self.tab1.data_base("Create Table if not exists product"
                            "(id integer primary key, name text, factory text, "
                            "price text, quantity text, img text)")
        self.tab1.widget()
        # ####################### Tab 2 >>
        self.tab2 = objectany.ObjectAny("member", "mem", self)
        self.tab2.data_base("Create table IF NOT EXISTS member"
                            "(id integer primary key, name text, family text,"
                            " phone text, email text, img text, address text)")
        self.tab2.widget()
        # ####################### Tab 3 >>
        self.tab3 = objectany.ObjectAny("sell", "sel", self)
        self.tab3.data_base("Create Table if not exists sell"
                            "(id integer primary key, name text, family text,"
                            " product text, price text, quantity text,  amount text)")
        self.tab3.widget()

        self.tabs.addTab(self.tab1, "Products")
        self.tabs.addTab(self.tab2, "Members")
        self.tabs.addTab(self.tab3, "Sells")

        self.main.addWidget(self.tabs)

    def add_member(self):
        self.member = None
        self.member = addMember.Member(self)
        self.member.ui("add")
        self.member.show()

    def add_product(self):
        self.product = None
        self.product = addProduct.Member(self)
        self.product.ui("add")
        self.product.show()

    def add_sell(self):
        self.sell = None
        self.sell = addSell.Sell(self)
        self.sell.ui()
        # self.sell.show()

    def update_items(self, _id, name):
        if name == "mem":
            self.member = None
            self.member = addMember.Member(self)
            self.member.update_data(_id)
            self.member.ui("update")
            self.member.show()
        elif name == "pro":
            self.product = None
            self.product = addProduct.Member(self)
            self.product.update_data(_id)
            self.product.ui("update")
            self.product.show()

    def win(self):
        self.setDisabled(False)
        self.tab1.widget()
        self.tab2.widget()
        self.tab3.widget()


def main():
    app = QApplication(sys.argv)
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)
    # app.setStyle('Breeze')
    # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setFont(QFont("Noto Sans", 10))

    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
