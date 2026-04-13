from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from sap import SapGui
from ui_main import Ui_MainWindow
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Automatin SAP System")

        # SYSTEM PAGES
        self.btn_home.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_home))
        self.btn_sap.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_sap))
        self.btn_about.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_about))
        self.btn_contact.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_contacts))

        self.btn_open.clicked.connect(self.open_file)
        self.btn_login.clicked.connect(self.login_sap)

        self.btn_register.clicked.connect(self.register)
    
    def open_file(self):
        self.file = QFileDialog.getOpenFileName(self, "Elija la hoja de cálculo")
        self.txt_file.setText(str(self.file[0]))

    def login_sap(self):
        self.sap = SapGui()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Login successful")
        msg.setWindowTitle("SAP Login")
        msg.exec_()

    def register(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Register Client")
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("¿Desea registrar el cliente?")
        msgBox.setInformativeText("Se registrarán los datos del cliente en el sistema SAP")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msgBox.exec_()

        if ret == QMessageBox.Yes:
            self.sap.register_client(self.txt_file.text())
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Client registered successfully")
            msg.setWindowTitle("SAP Client Registration")
            msg.exec_()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()