from dataclasses import dataclass
from srcs.constants import TYPE_RANGE, MAX_TRANSACTION, CATEGORY_FIELD_SIZE
from datetime import datetime
from srcs.validator import validate_category
@dataclass
class transaction:
    id: int
    date: str
    type: str
    category: str
    amount: int
    def __post_init__(self):
        try:
            self.amount = int(self.amount)
        except TypeError:
            raise TypeError("숫자가 아닙니다.")
        if self.amount < 0:
            raise ValueError("amount minus Error")
        if (self.amount > MAX_TRANSACTION):
            raise ValueError(f"가능한 거래한도{MAX_TRANSACTION}초과입니다.")
        if self.type not in TYPE_RANGE:
            raise ValueError("Type_Error")
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date_Error")

#버젯은 인자전달정규화로 인자전달시 확인
@dataclass
class budget:
    amount: int
    date: str
@dataclass
class category:
    category: str
    def __post_init__(self):
        if not(validate_category(self.category)):
            raise ValueError(f"category가 {CATEGORY_FIELD_SIZE}크기를 넘으면ㅇ나됩니다.")