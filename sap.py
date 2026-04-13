from os import replace
import subprocess
import time
import os
import sys
from dotenv import load_dotenv
import win32com.client  # type: ignore
import pandas as pd

load_dotenv()

system_sap = os.getenv("SYSTEM")
mandt = os.getenv("MANDT")
username = os.getenv("USER")
password = os.getenv("PASSWD")
language = os.getenv("LANGUAGE")

class SapGui():
    def __init__(self):

        self.path = r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe"
        subprocess.Popen(self.path)
        time.sleep(3)

        self.SapGuiAuto = win32com.client.GetObject("SAPGUI")
        if not type(self.SapGuiAuto) == win32com.client.CDispatch:
            print("SAP GUI not found")
            return

        application = self.SapGuiAuto.GetScriptingEngine
        self.connection = application.OpenConnection(system_sap, True)
        time.sleep(3)

        self.session = self.connection.Children(0)

        self.sapLogin()

    def sapLogin(self):

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

    def safe_close_window(self, window_id):
        try:
            self.session.findById(window_id).close()
        except Exception:
            pass
    
    def register_client(self, file_path): 
        data = pd.read_excel(file_path, sheet_name="Hoja1").astype(str)
        data.columns = data.columns.str.replace(" ", '_')

        self.session.findById("wnd[0]").maximize()
        
        for index, row in data.iterrows():
            self.session.findById("wnd[0]/tbar[0]/okcd").text = "xd01"
            self.session.findById("wnd[0]").sendVKey(0)
            time.sleep(2)
            self.session.findById("wnd[1]/usr/cmbRF02D-KTOKD").key = "ZNAC"
            self.session.findById("wnd[1]/usr/cmbRF02D-KTOKD").setFocus()
            self.session.findById("wnd[1]").sendVKey(0)
            time.sleep(2)
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/cmbSZA1_D0100-TITLE_MEDI").key = "CONSUMIDOR_FINAL_SIN_NOMBRE"
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/txtADDR1_DATA-NAME1").text = row.NAME 
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/txtADDR1_DATA-SORT1").text = row.SEARCH_TERM
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/txtADDR1_DATA-STREET").text = row.STREET
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/txtADDR1_DATA-HOUSE_NUM1").text = row.NUM_HOUSE
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/txtADDR1_DATA-POST_CODE1").text = row.POSTCODE
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/ctxtADDR1_DATA-COUNTRY").text = row.COUNTRY
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/ctxtADDR1_DATA-REGION").text = row.REGION
            
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/txtADDR1_DATA-STREET").setFocus()
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0201/subAREA1:SAPMF02D:7111/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/txtADDR1_DATA-STREET").caretPosition = 7
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02").select()
            time.sleep(1)
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02/ssubSUBSC:SAPLATAB:0200/subAREA2:SAPMF02D:7123/ctxtKNA1-BRSCH").text = row.INDUSTRY
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02/ssubSUBSC:SAPLATAB:0200/subAREA3:SAPMF02D:7122/txtKNA1-STCD1").text = row.POSF1
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02/ssubSUBSC:SAPLATAB:0200/subAREA3:SAPMF02D:7122/txtKNA1-STCD2").text = row.POSF2
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02/ssubSUBSC:SAPLATAB:0200/subAREA3:SAPMF02D:7122/txtKNA1-STCD2").setFocus()
            self.session.findById("wnd[0]/usr/subSUBTAB:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB02/ssubSUBSC:SAPLATAB:0200/subAREA3:SAPMF02D:7122/txtKNA1-STCD2").caretPosition = 2
            self.session.findById("wnd[0]/tbar[0]/btn[11]").press()
            self.session.findById("wnd[0]/tbar[0]/btn[12]").press()
