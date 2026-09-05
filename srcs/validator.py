from datetime import datetime


def validate_any(value: str) -> bool:
    return True
def validate_month(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m")
        return True
    except ValueError:
        return False
def validate_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False
def validate_suffix(value: str, suffix:str)->bool:
    return value.endswith(suffix)
def validate_num(value: str)-> bool:
    try:
        return int(value) > 0
    except ValueError:
        raise ValueError