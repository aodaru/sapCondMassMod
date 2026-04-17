from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox 
from sap import SapGui
from ui_sap import Ui_MainWindow
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Automatin SAP System")

        self.btn_open.clicked.connect(self.open_file)
        self.btn_login.clicked.connect(self.login_sap)

        self.btn_ejecutar.clicked.connect(self.massive_change)

        self.btn_logout.clicked.connect(self.logout)
        self.btn_close.clicked.connect(self.close_application)

        self.plainTextEdit.setReadOnly(True)
    
    def open_file(self):
        self.file = QFileDialog.getOpenFileName(self, "Elija la hoja de cálculo")
        self.txt_file.setText(str(self.file[0]))

    def login_sap(self):
        self.sap = SapGui()
        self.sap.sapLogin()

        self.plainTextEdit.appendPlainText("Login successful") 

    def massive_change(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Confirmación de ejecución de procedimiento masivo")
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Estas Seguro de ejecutar el procedimiento masivo?")
        msgBox.setInformativeText("Se registraran modificaciones a condiciones de precios.")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msgBox.exec_()

        if ret == QMessageBox.Yes:
            self.sap.massive_change(self.txt_file.text(), self.plainTextEdit.appendPlainText)

            self.plainTextEdit.appendPlainText("Ejecucion completada con exito!") 

    def logout(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Cerrar")
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Esta seguro que desea cerrar la sesión?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msgBox.exec_()

        if ret == QMessageBox.Yes:
            self.sap.safe_close_window()

    def close_application(self):
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()