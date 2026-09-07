from srcs.io_utils import  addpadding, filegenerator
from srcs.constants import TRANSACTION_PATH, CATEGORY_PATH
from srcs.input_utils import ask_category
from srcs.schema import DATACLASS
from srcs.io_utils import file_manager
from srcs.exception import DataException
from typing import  Any
import os

@file_manager({"f": (CATEGORY_PATH, "rb+", True)})
def categoryadd(files: dict[str, Any])->tuple[str, bool]:
    f = files['f']
    res = ask_category()
    if res is None:
        return "시도횟수이내 적합한 데이터 입력을 실패했습니다", False
    g = filegenerator(f, DATACLASS['category'])
    for a in g:
        if res.category == a.category:
            return "중복된 카테고리가 있습니다", False
    f.write(addpadding(res, DATACLASS['category'].line_size))
    return "카테고리 추가 성공", True


@file_manager({"f": (CATEGORY_PATH, "rb", False)})
def categorylist(files: dict[str, Any])->tuple[str, bool]:
    f = files['f']
    f.seek(0) 
    g = filegenerator(f, DATACLASS['category'])
    try:
        for a in g:
            print(f"category:{a.category}")
    except DataException:
        raise DataException
    return "카테고리 목록이 출력됨.", True

@file_manager({"c": (CATEGORY_PATH, "rb+", False), "t": (TRANSACTION_PATH, "rb", False)})
def categoryremove(files: dict[str, Any])->tuple[str, bool]:
    c = files['c']
    t = files['t']
    res = ask_category()
    if res is None:
        return "시도횟수이내 적합한 데이터 입력을 실패했습니다", False
    g_c = filegenerator(c, DATACLASS['category'])
    for a in g_c:
        if a.category == res.category:
            g_t = filegenerator(t, DATACLASS['transaction'])
            for a in g_t:
                if a.category == res.category:
                    return "transaction에서 이미 사용중인 카테고리입니다.", False
            c.seek(-1 * DATACLASS['category'].line_size, os.SEEK_CUR)
            c.write(addpadding(None, DATACLASS['category'].line_size))
            return "카테고리 삭제를 성공했습니다", True
    return "해당하는 카테고리가 없습니다", False