import pandas as pd
from typing import Optional, Tuple, List

VALID_FLOWS = (
    "mat_orgvent_candistr",
    "orgvent_candistr_sec_ramo_mat",
    "orgven_candist_sec_gpoart",
    "orgvent_candistr_gpoart",
)

FLOW_FIELDS = {
    "mat_orgvent_candistr": ["MATERIAL", "UNIDAD_DE_MEDIDA", "IMPORTE", "ORG_VENTA", "CAN_DISTR"],
    "orgvent_candistr_gpoart": ["ORG_VENTA", "CAN_DISTR", "GRUPO_ARTICULO", "IMPORTE"],
    "orgvent_candistr_sec_ramo_mat": ["ORG_VENTA", "CAN_DISTR", "SECTOR", "RAMO", "MATERIAL"],
    "orgven_candist_sec_gpoart": ["ORG_VENTA", "CAN_DISTR", "SECTOR", "RAMO", "GRUPO_ARTICULO"],
}

VALID_ORG_VENTA = {"1000"}
VALID_CAN_DISTR = {"10", "20", "30", "40", "50"}
VALID_SECTOR = {"10", "20", "30", "40", "50"}
VALID_RAMO = {"ZDET", "ZCON", "ZPROY"}
VALID_UNIDAD_MEDIDA = {"UN", "MT", "PT"}


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
