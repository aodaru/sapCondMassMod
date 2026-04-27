from os import replace
import subprocess
import time
import os
import sys
from dotenv import load_dotenv
from sap_vk12_massmod import SapVk12MassMod
import win32com.client  # type: ignore
import pandas as pd
from pathlib import Path
from paths import get_base_path

BASE_DIR = Path(get_base_path())
load_dotenv(BASE_DIR / ".env")

system_sap = os.getenv("SYSTEM")
mandt = os.getenv("MANDT")
username = os.getenv("USER")
password = os.getenv("PASSWD")
language = os.getenv("LANGUAGE")

class SapGui():
    def open_sap(self):
        self.path = r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe"
        subprocess.Popen(self.path)
    
    def connection_sap(self):
        # debes investigar como detectar si ya esta corriendo el SAPGUI
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        application = SapGuiAuto.GetScriptingEngine
        self.connection = application.Children(0)
        self.session = self.connection.Children(0)
        self.session.findById("wnd[0]").maximize()

    def sapLogin(self, log_func=print):
        self.open_sap()
        time.sleep(3)
        self.SapGuiAuto = win32com.client.GetObject("SAPGUI")
        self.application = self.SapGuiAuto.GetScriptingEngine

        try:
            self.connection = self.application.OpenConnection(system_sap, True)
        except:
            print(sys.exc_info()[0])
            log_func(f"{'='*50}")
            log_func(f"Error tratando de conectar con SAP: {sys.exc_info()[0]}")
            log_func(f"La red no esta accesible o el sistema SAP no esta disponible.")
            log_func(f"{'='*50}")

        time.sleep(3)
        self.session = self.connection.Children(0)

        if not type(self.SapGuiAuto) == win32com.client.CDispatch:
            return

        try: 

            # THE CLIENT
            self.session.findById("wnd[0]/usr/txtRSYST-MANDT").text = mandt
            # USERNAME
            self.session.findById("wnd[0]/usr/txtRSYST-BNAME").text = username
            # PASSWORD
            self.session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = password
            # LANGUAGE
            self.session.findById("wnd[0]/usr/txtRSYST-LANGU").text = language
            # ENTER
            self.session.findById("wnd[0]").sendVKey(0)
        
        except:
            print(sys.exc_info()[0])
            log_func(f"Error tratando de conectar con SAP: {sys.exc_info()[0]}")

    def safe_close_window(self, log_func=print):

        try:
            self.connection_sap()
            self.connection.CloseSession('ses[0]')
        except:
            print(sys.exc_info()[0])
            log_func(f"{'='*50}")
            log_func(f"Error tratando de conectar con SAP para cerrar sesión: {sys.exc_info()[0]}")
            log_func(f"{'='*50}")

        subprocess.run(["taskkill", "/f", "/im", "saplogon.exe"])
    
    def massive_change(self, file_path, log_func=print):
        if not hasattr(self, "session") or self.session is None:
            raise RuntimeError("SAP session no iniciada. Ejecute sapLogin primero.")

        runner = SapVk12MassMod(self.session, log_func)
        return runner.run_vk12_massmod(file_path)
