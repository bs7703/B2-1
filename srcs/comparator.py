from datetime import datetime
from srcs.validator import validate_month, validate_date

def _parse_to_datetime(date_str: str) -> datetime:
    if validate_date(date_str):
        return datetime.strptime(date_str, "%Y-%m-%d")
    if validate_month(date_str):
        return datetime.strptime(date_str, "%Y-%m")
    raise TypeError(f"지원하지 않는 날짜 형식입니다: {date_str}")

# date1이 date2이후인지판단.
def comp_date(date1: str, date2: str) -> bool:
    try:
        return  _parse_to_datetime(date1) >= _parse_to_datetime(date2)
    except ValueError as e:
        raise ValueError(f"날짜 비교 중 오류 발생: {e}")