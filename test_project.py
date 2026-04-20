import pytest
import pandas as pd
import tempfile
import os
from validators import validate_excel, validate_field, VALID_FLOWS, FLOW_FIELDS, VALID_UNIDAD_MEDIDA
from sap_vk12_massmod import SapVk12MassMod

# Tests para validators.py
class TestValidators:
    def test_validate_field_valid_material(self):
        error = validate_field("MATERIAL", "12345678", 1)
        assert error is None

    def test_validate_field_invalid_material(self):
        error = validate_field("MATERIAL", "ABC123", 1)
        assert "no debe contener letras" in error

    def test_validate_field_missing_importe(self):
        error = validate_field("IMPORTE", "", 1)
        assert "es obligatorio" in error

    def test_validate_field_invalid_importe(self):
        error = validate_field("IMPORTE", "ABC", 1)
        assert "debe ser numérico" in error

    def test_validate_field_invalid_org_venta(self):
        error = validate_field("ORG_VENTA", "2000", 1)
        assert "debe ser '1000'" in error

    def test_validate_field_invalid_can_distr(self):
        error = validate_field("CAN_DISTR", "60", 1)
        assert "debe ser 10, 20, 30, 40 o 50" in error

    def test_validate_field_invalid_sector(self):
        error = validate_field("SECTOR", "60", 1)
        assert "debe ser 10, 20, 30, 40 o 50" in error

    def test_validate_field_invalid_ramo(self):
        error = validate_field("RAMO", "INVALID", 1)
        assert "debe ser ZDET, ZCON o ZPROY" in error

    def test_validate_field_invalid_grupo_articulo_length(self):
        error = validate_field("GRUPO_ARTICULO", "123", 1)
        assert "debe tener 8 caracteres" in error

    def test_validate_field_invalid_grupo_articulo_chars(self):
        error = validate_field("GRUPO_ARTICULO", "12345678A", 1)  # 9 chars with letter
        assert "no debe contener letras" in error

    def test_validate_field_invalid_unidad_medida(self):
        error = validate_field("UNIDAD_DE_MEDIDA", "XYZ", 1)
        assert "No es una unidad de medida válida" in error

    def test_validate_excel_valid_data(self):
        data = {
            "TIPO_MODIFICACION": ["mat_orgvent_candistr"],
            "MATERIAL": ["12345678"],
            "UNIDAD_DE_MEDIDA": ["UN"],
            "IMPORTE": ["10.5"],
            "ORG_VENTA": ["1000"],
            "CAN_DISTR": ["10"]
        }
        df = pd.DataFrame(data)
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            df.to_excel(tmp.name, sheet_name="vk12", index=False)
            tmp.close()  # Close the file before reading
            validated_data, errors = validate_excel(tmp.name)
            os.unlink(tmp.name)
        assert len(errors) == 0
        assert len(validated_data) == 1

    def test_validate_excel_invalid_flow(self):
        data = {
            "TIPO_MODIFICACION": ["invalid_flow"],
            "MATERIAL": ["12345678"]
        }
        df = pd.DataFrame(data)
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            df.to_excel(tmp.name, sheet_name="vk12", index=False)
            tmp.close()
            validated_data, errors = validate_excel(tmp.name)
            os.unlink(tmp.name)
        assert len(errors) == 1
        assert "Flujo 'invalid_flow' no válido" in errors[0]

    def test_validate_excel_missing_field(self):
        data = {
            "TIPO_MODIFICACION": ["mat_orgvent_candistr"],
            "MATERIAL": ["12345678"],
            # Falta UNIDAD_DE_MEDIDA
            "IMPORTE": ["10.5"],
            "ORG_VENTA": ["1000"],
            "CAN_DISTR": ["10"]
        }
        df = pd.DataFrame(data)
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            df.to_excel(tmp.name, sheet_name="vk12", index=False)
            tmp.close()
            validated_data, errors = validate_excel(tmp.name)
            os.unlink(tmp.name)
        assert len(errors) == 1
        assert "UNIDAD_DE_MEDIDA" in errors[0]

# Tests para sap_vk12_massmod.py (esqueleto básico, requiere mock para sesión SAP)
class TestSapVk12MassMod:
    def test_available_flows(self):
        runner = SapVk12MassMod(None, print)  # Sesión mockeada
        flows = runner.available_flows()
        assert "vk12_massmod" in flows

    def test_run_flow_invalid(self):
        runner = SapVk12MassMod(None, print)
        with pytest.raises(ValueError):
            runner.run_flow("invalid", "dummy_path")

    # Para tests más avanzados, mockear la sesión SAP con unittest.mock
    # Ejemplo: from unittest.mock import MagicMock
    # session = MagicMock()
    # runner = SapVk12MassMod(session, print)
    # runner.run_vk12_massmod("path_to_test_excel")  # Usar el archivo test_vk12.xlsx