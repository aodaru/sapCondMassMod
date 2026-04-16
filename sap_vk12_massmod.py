import time
import pandas as pd


class SapVk12MassMod:
    """Lógica de modificación masiva para el flujo VK12."""

    def __init__(self, session):
        self.session = session

    def available_flows(self):
        return ["vk12_massmod"]

    def run_flow(self, flow_name, file_path):
        if flow_name == "vk12_massmod":
            return self.run_vk12_massmod(file_path)
        raise ValueError(f"Flujo desconocido: {flow_name}")

    def run_vk12_massmod(self, file_path):
        # data = pd.read_excel(file_path, sheet_name="Hoja1").astype(str)
        data = pd.read_excel(file_path, sheet_name="Hoja1", dtype=str)
        data.columns = data.columns.str.strip().str.upper().str.replace(" ", "_")

        required_columns = [
            "MATERIAL", 
            "UNIDAD_DE_MEDIDA", 
            "IMPORTE", 
            "GRUPO_ARTICULO",
            "ORG_VENTA",
            "CAN_DISTR",
            "SECTOR",
            "RAMO",
            "TIPO_MODIFICACION"
            ]
        missing_columns = [c for c in required_columns if c not in data.columns]
        if missing_columns:
            raise ValueError(f"Faltan columnas en el Excel: {', '.join(missing_columns)}")

        self.session.findById("wnd[0]").maximize()

        for index, row in data.iterrows():
            flow_name = row.TIPO_MODIFICACION.strip().lower()
            method_name = flow_name.replace("-", "_")
            method = getattr(self, method_name, None)

            if method and callable(method):
                method(self.session, row, index)
            else:
                print(f"Advertencia: Flujo '{flow_name}' no encontrado. Fila {index}, Material: {row.MATERIAL}")

    # Flujos modificacion masiva

    # ## material, organización de ventas, canal de distribución
    def _mat_orgvent_candistr(self, session, row, index):
        print(f"Material: {row.MATERIAL}")
        session.findById("wnd[0]/tbar[0]/okcd").text = "vk12"
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[0]/usr/ctxtRV13A-KSCHL").text = "Z004"
        session.findById("wnd[0]/usr/ctxtRV13A-KSCHL").caretPosition = 4
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[1,0]").select()
        session.findById("wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[1,0]").setFocus()
        session.findById("wnd[1]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[0]/usr/ctxtF001").text = row.ORG_VENTA
        session.findById("wnd[0]/usr/ctxtF002").text = row.CAN_DISTR
        session.findById("wnd[0]/usr/ctxtF003-LOW").text = row.MATERIAL
        session.findById("wnd[0]/usr/ctxtF003-LOW").setFocus()
        session.findById("wnd[0]/usr/ctxtF003-LOW").caretPosition = 8
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[0]/tbar[1]/btn[8]").press()
        time.sleep(1)

        material_field = session.findById(
            "wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/ctxtKOMG-MATNR[0,0]"
        )
        existing_material = material_field.text
        if existing_material:
            print(f"Fila {index}: material ya contiene datos: {existing_material}")
        else:
            material_field.text = row.MATERIAL

        unidad_medida_field = session.findById(
            "wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/ctxtKOMG-VRKME[1,0]"
        )
        existing_unidad_medida = unidad_medida_field.text
        if existing_unidad_medida:
            print(f"Fila {index}: unidad de medida ya contiene datos: {existing_unidad_medida}")
        else:
            unidad_medida_field.text = row.UNIDAD_DE_MEDIDA

        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[3,0]").text = row.IMPORTE
        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[3,0]").setFocus()
        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[3,0]").caretPosition = 16
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[3]").press()
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[3]").press()

    # ## Organización de ventas, canal de distribución, grupo de artículo
    def _orgvent_candistr_gpoart(self, session, row, index):
        session.findById("wnd[0]/tbar[0]/okcd").text = "vk12"
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[0]/usr/ctxtRV13A-KSCHL").text = "Z004"
        session.findById("wnd[0]/usr/ctxtRV13A-KSCHL").caretPosition = 4
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[6,0]").select()
        session.findById("wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[6,0]").setFocus()
        session.findById("wnd[1]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[0]/usr/ctxtF001").text = row.ORG_VENTA
        session.findById("wnd[0]/usr/ctxtF002").text = row.CAN_DISTR
        session.findById("wnd[0]/usr/ctxtF003-LOW").text = row.GRUPO_ARTICULO
        session.findById("wnd[0]/usr/ctxtF003-LOW").setFocus()
        session.findById("wnd[0]/usr/ctxtF003-LOW").caretPosition = 9
        session.findById("wnd[0]/tbar[1]/btn[8]").press()
        time.sleep(1)
        gpo_mat_field = session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/ctxtKOMG-MATKL[0,0]")
        existing_gpo_mat = gpo_mat_field.text
        if existing_gpo_mat:
            print(f"Fila {index}: grupo de material ya contiene datos: {existing_gpo_mat}")
        else:
            gpo_mat_field.text = row.GRUPO_ARTICULO
    
        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[2,0]").text = row.IMPORTE
        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[2,0]").setFocus
        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[2,0]").caretPosition = 16
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[3]").press()
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[3]").press()

    # ## Organización de ventas, canal de distribución, sector ramo material
    def _orgvent_candistr_sec_ramo_mat(self, session, row, index):
        session.findById("wnd[0]/tbar[0]/okcd").text = "vk12"
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[0]/usr/ctxtRV13A-KSCHL").text = "Z004"
        session.findById("wnd[0]/usr/ctxtRV13A-KSCHL").caretPosition = 4
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[3,0]").select()
        session.findById("wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[3,0]").setFocus()
        session.findById("wnd[1]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[0]/usr/ctxtF001").text = row.ORG_VENTA
        session.findById("wnd[0]/usr/ctxtF002").text = row.CAN_DISTR
        session.findById("wnd[0]/usr/ctxtF003").text = row.SECTOR
        session.findById("wnd[0]/usr/ctxtF004").text = row.RAMO
        session.findById("wnd[0]/usr/ctxtF005-LOW").text = row.MATERIAL
        session.findById("wnd[0]/usr/ctxtF005-LOW").setFocus()
        session.findById("wnd[0]/usr/ctxtF005-LOW").caretPosition = 8
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]/tbar[1]/btn[8]").press()
        time.sleep(1)

        ramo_field = session.findById("wnd[0]/usr/ctxtKOMG-BRSCH")
        existing_ramo = ramo_field.text
        if existing_ramo:
            print(f"Fila {index}: ramo ya contiene datos: {existing_ramo}")
        else:
            ramo_field.text = row.RAMO

        material_field = session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/ctxtKOMG-MATNR[0,0]")
        existing_material = material_field.text
        if existing_material:
            print(f"Fila {index}: material ya contiene datos: {existing_material}")
        else:
            material_field.text = row.MATERIAL

        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/ctxtKOMG-MATNR[0,0]").setFocus
        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/ctxtKOMG-MATNR[0,0]").caretPosition = 8
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[4,0]").text = row.IMPORTE
        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[4,0]").setFocus()
        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[4,0]").caretPosition = 11
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[3]").press()
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[3]").press()
    
    # ## Organización de ventas, canal de distribución, sector grupo de artículo
    def _orgven_candist_sec_gpoart(self, session, row, index):
        session.findById("wnd[0]/tbar[0]/okcd").text = "vk12"
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[0]/usr/ctxtRV13A-KSCHL").text = "Z004"
        session.findById("wnd[0]/usr/ctxtRV13A-KSCHL").caretPosition = 4
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[4,0]").select()
        session.findById("wnd[1]/usr/sub:SAPLV14A:0100/radRV130-SELKZ[4,0]").setFocus()
        session.findById("wnd[1]/tbar[0]/btn[0]").press()
        time.sleep(1)
        session.findById("wnd[0]/usr/ctxtF001").text = row.ORG_VENTA
        session.findById("wnd[0]/usr/ctxtF002").text = row.CAN_DISTR
        session.findById("wnd[0]/usr/ctxtF003").text = row.SECTOR
        session.findById("wnd[0]/usr/ctxtF004").text = row.RAMO
        session.findById("wnd[0]/usr/ctxtF005-LOW").text = row.GRUPO_ARTICULO
        session.findById("wnd[0]/usr/ctxtF005-LOW").setFocus()
        session.findById("wnd[0]/usr/ctxtF005-LOW").caretPosition = 9
        session.findById("wnd[0]/tbar[1]/btn[8]").press()

        gpo_mat_field = session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/ctxtKOMG-MATKL[0,0]")
        existing_gpo_mat = gpo_mat_field.text
        if existing_gpo_mat:
            print(f"Fila {index}: grupo de material ya contiene datos: {existing_gpo_mat}")
        else:
            gpo_mat_field.text = row.GRUPO_ARTICULO

        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[4,0]").text = row.IMPORTE
        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[4,0]").setFocus()
        session.findById("wnd[0]/usr/tblSAPMV13ATCTRL_FAST_ENTRY/txtKONP-KBETR[4,0]").caretPosition = 16
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[3]").press()
        time.sleep(1)
        session.findById("wnd[0]/tbar[0]/btn[3]").press()
    # Fin - Flujos modificacion masiva


    # Llamada de flujos masivos
    def mat_orgvent_candistr(self, session, row, index):
        self._mat_orgvent_candistr(session, row, index)

    def orgvent_candistr_gpoart(self, session, row, index):
        self._orgvent_candistr_gpoart(session, row, index)

    def orgvent_candistr_sec_ramo_mat(self, session, row, index):
        self._orgvent_candistr_sec_ramo_mat(session, row, index)

    def orgven_candist_sec_gpoart(self, session, row, index):
        self._orgven_candist_sec_gpoart(session, row, index)

