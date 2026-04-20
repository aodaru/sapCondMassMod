import pandas as pd
from typing import Optional, Tuple, List
import os
import json
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Leer y parsear desde .env
VALID_FLOWS = tuple(os.getenv("VALID_FLOWS", "").split(","))

VALID_ORG_VENTA = set(os.getenv("VALID_ORG_VENTA", "").split(","))
VALID_CAN_DISTR = set(os.getenv("VALID_CAN_DISTR", "").split(","))
VALID_SECTOR = set(os.getenv("VALID_SECTOR", "").split(","))
VALID_RAMO = set(os.getenv("VALID_RAMO", "").split(","))
VALID_UNIDAD_MEDIDA = set(os.getenv("VALID_UNIDAD_MEDIDA", "").split(","))

# FLOW_FIELDS como diccionario desde JSON
FLOW_FIELDS = json.loads(os.getenv("FLOW_FIELDS", "{}"))

def is_numeric(value: str) -> bool:
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def is_integer(value: str) -> bool:
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False

def solo_numeros(texto: str) -> bool:
    texto = texto.strip()
    return texto.isdigit()


def validate_field(field: str, value: str, row_num: int) -> Optional[str]:
    value = str(value).strip()

    if not value or value.lower() == "nan":
        return f"Fila {row_num}: '{field}' es obligatorio"

    if field == "IMPORTE" and not is_numeric(value):
        return f"Fila {row_num}: '{field}' debe ser numérico"

    if field == "MATERIAL" and not solo_numeros(value):
        return f"Fila {row_num}: '{field} - {value}' no debe contener letras ni caracteres especiales"

    if field == "ORG_VENTA" and value not in VALID_ORG_VENTA:
        return f"Fila {row_num}: '{field}' debe ser '1000'"

    if field == "CAN_DISTR" and value not in VALID_CAN_DISTR:
        return f"Fila {row_num}: '{field}' debe ser 10, 20, 30, 40 o 50"

    if field == "SECTOR" and value not in VALID_SECTOR:
        return f"Fila {row_num}: '{field} - {value}'  debe ser 10, 20, 30, 40 o 50"

    if field == "RAMO" and value not in VALID_RAMO:
        return f"Fila {row_num}: '{field}' debe ser ZDET, ZCON o ZPROY"

    if field == "GRUPO_ARTICULO":
        if len(value) != 9:
            return f"Fila {row_num}: '{field} - {value}' debe tener 8 caracteres"
        if not solo_numeros(value):
            return f"Fila {row_num}: '{field}' no debe contener letras ni caracteres especiales"

    if field == "UNIDAD_DE_MEDIDA" and value not in VALID_UNIDAD_MEDIDA:
        return f"Fila {row_num}: '{field}' debe ser UN, MT o PT"

    return None


def validate_excel(file_path: str, log_func=print) -> Tuple[pd.DataFrame, List[str]]:
    errors = []

    data = pd.read_excel(file_path, sheet_name="Hoja1", dtype=str)
    data.columns = data.columns.str.strip().str.upper().str.replace(" ", "_")

    for index, row in data.iterrows():
        flow_name = str(row.get("TIPO_MODIFICACION", "")).strip().lower()

        if flow_name not in VALID_FLOWS:
            errors.append(f"Fila {index}: Flujo '{flow_name}' no válido")
            continue

        for field in FLOW_FIELDS.get(flow_name, []):
            error = validate_field(field, row.get(field, ""), index)
            if error:
                errors.append(error)
                data.drop(index, inplace=True)  # Eliminar fila con error para evitar procesamiento posterior   

    return data, errors


def print_validation_errors(errors: List[str], log_func=print):
    if errors:
        log_func(f"\n{'='*50}")
        log_func(f"Se encontraron {len(errors)} error(es):")
        log_func("="*50)
        for error in errors:
            log_func(f"  - {error}")
        log_func("="*50)
