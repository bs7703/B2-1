from srcs.constants import BUDGET_PATH
from srcs.io_utils import file_manager, filegenerator, addpadding
from srcs.schema import DATACLASS, Budget
import os
from typing import Any

@file_manager({"b": (BUDGET_PATH, "rb+", True)})
def budgetset(files: dict[str, Any], month:str, amount:str):
    b = files['b']
    g = filegenerator(b, DATACLASS['budget'])
    res = "예산을 마지막 항목에 추가했습니다."
    for a in g:
        if (a.date == month):
            b.seek(-1 * DATACLASS['budget'].line_size, os.SEEK_CUR)
            res = f"{a.date}에 겹치는 항목이있어 예산을 {amount}로 재설정했습니다."
            break
    b.write(addpadding(Budget(int(amount), month), DATACLASS['budget'].line_size))
    return res,True

