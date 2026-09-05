from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from typing import Callable
from .constants import T, K, TYPE_RANGE
from srcs.constants import CATEGORY_FIELD_SIZE


def check_category_length(func:Callable[[K], None]):
    @wraps(func)
    def wrapper(self:K):
        result = func(self)
        if len(self.category.encode('utf-8')) > CATEGORY_FIELD_SIZE:
            raise ValueError("Category_Length_Error")
        return result
    return wrapper

def check_validity(func:Callable[[T], None]):
    @wraps(func)
    def wrapper(self:T):
        result = func(self)
        try:
            self.amount = int(self.amount)
        except (ValueError, TypeError):
            raise ValueError("int_value_error")
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date_Error")
        if self.amount < 0:
            raise ValueError("amount minus Error")
        return result
    return wrapper

@dataclass
class transaction:
    id: int
    date: str
    type: str
    category: str
    amount: int
    @check_category_length
    @check_validity
    def __post_init__(self):
        if self.type not in TYPE_RANGE:
            raise ValueError("Type_Error")
@dataclass
class budget:
    amount: int
    date: str
    @check_validity
    def __post_init__(self):
        ...

@dataclass
class category:
    category: str
    @check_category_length
    def __post_init__(self):
        ...