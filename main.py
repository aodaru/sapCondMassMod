from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox 
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from sap import SapGui
from ui_sap import Ui_MainWindow
import sys
import shutil 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Automatin SAP System")

        # Always on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.btn_open.clicked.connect(self.open_file)
        self.btn_login.clicked.connect(self.login_sap)

        self.btn_ejecutar.clicked.connect(self.massive_change)

        self.btn_logout.clicked.connect(self.logout)
        self.btn_close.clicked.connect(self.close_application)

        self.plainTextEdit.setReadOnly(True)

        if hasattr(self, 'lbl_template'):
            self.lbl_template.linkActivated.connect(self.download_template)
    
    def open_file(self):
        self.file = QFileDialog.getOpenFileName(self, "Elija la hoja de cálculo")
        self.txt_file.setText(str(self.file[0]))

    def login_sap(self):
        self.sap = SapGui()
        self.sap.sapLogin(self.plainTextEdit.appendPlainText)

        self.plainTextEdit.appendPlainText(f"{'='*50}")
        self.plainTextEdit.appendPlainText("Login successful") 
        self.plainTextEdit.appendPlainText(f"{'='*50}")

    def massive_change(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Confirmación de ejecución de procedimiento masivo")
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Estas Seguro de ejecutar el procedimiento masivo?")
        msgBox.setInformativeText("Se registraran modificaciones a condiciones de precios.")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msgBox.exec_()

        if ret == QMessageBox.Yes:
            self.sap.massive_change(self.txt_file.text(), self.plainTextEdit.appendPlainText)

            self.plainTextEdit.appendPlainText(f"{'='*50}")
            self.plainTextEdit.appendPlainText("Ejecucion completada con exito!") 
            self.plainTextEdit.appendPlainText(f"{'='*50}")

    def logout(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Cerrar")
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Esta seguro que desea cerrar la sesión?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msgBox.exec_()

        if ret == QMessageBox.Yes:
            self.sap.safe_close_window(self.plainTextEdit.appendPlainText)
            self.plainTextEdit.appendPlainText(f"{'='*50}")
            self.plainTextEdit.appendPlainText("Sesión cerrada con éxito")
            self.plainTextEdit.appendPlainText(f"{'='*50}")

    def close_application(self):
        self.close()

    def download_template(self):
        template_source = BASE_DIR / "template_vk12.xlsx"
        if not template_source.exists():
            QMessageBox.critical(self, "Error", "No se encontró el archivo de plantilla.")
            return
        dest = QFileDialog.getSaveFileName(self, "Guardar plantilla como", "template_vk12.xlsx", "Excel Files (*.xlsx)")
        if dest:
            try:
                shutil.copy(template_source, dest[0])
                QMessageBox.information(self, "Éxito", "Plantilla descargada exitosamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo descargar la plantilla: {e}")


if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon("icon.ico")) 
    window = MainWindow()
    window.show()
    app.exec_()