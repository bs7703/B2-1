from datetime import datetime
from srcs.constants import CATEGORY_FIELD_SIZE

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
        val = int(value)
        if (val < 0):
            raise ValueError
    except (TypeError, ValueError):
        return False
    return True
def validate_under(value:str, num:int)->bool:
    try:
        val = int(value)
        if (val > num):
            raise ValueError
    except (TypeError, ValueError):
        return False
    return True
def validate_category(value:str)->bool:
    return len(str.encode("utf-8")) > CATEGORY_FIELD_SIZE
