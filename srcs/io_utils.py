import json
from functools import partial
from io import BufferedIOBase, BufferedReader
from typing import  Generator, Type
import os
from srcs.fileformat import budget, category, transaction
from .constants import BUDGET_LINE_SIZE, CATEGORY_LINE_SIZE, G, TRANSACTION_LINE_SIZE


def addpadding(my_class:G | None, line_size:int) -> bytes:
    bytes = b""
    if (my_class is not None):
        bytes = json.dumps(my_class.__dict__, ensure_ascii=False).encode('utf-8')
    bytes = bytes.rjust(line_size - 1, b'\x00') + b'\n'
    return bytes

def BytesToClass(line:bytes,line_size:int, dict_class:Type[G])->G | None:
    try:
        if line == b'\x00' * (line_size - 1) + b'\n':
            return None
        data = json.loads(line)
        return dict_class(**data)
    except json.JSONDecodeError as e:
        raise e
    except ValueError as e:
        raise e

def filegenerator(file: BufferedReader,line_size: int,dict_class: Type[G],rev: bool) -> Generator[G, None, None]:
    if not rev:
        while True:
            line = file.read(line_size)
            if not line:
                return
            data = BytesToClass(line, line_size, dict_class)
            if data is not None:
                yield data
    else:
        file.seek(0, os.SEEK_END)
        offset = file.tell() - line_size
        while offset >= 0:
            file.seek(offset)
            line = file.read(line_size)
            data = BytesToClass(line, line_size, dict_class)
            if data is not None:
                yield data
            offset -= line_size
def isExist(file:BufferedIOBase, line_size:int, idx:int)->bool:
    file.seek(idx * line_size)
    line = file.read(line_size)
    if line is b'\x00' * (line_size - 1) + b'\n':
        return False
    return True

def seekfilesize(file: BufferedIOBase):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0) 
    return size
def indexAvailable(file:BufferedIOBase, line_size:int, idx:int)->bool:
    size=  seekfilesize(file)
    total_idx = size / line_size
    return idx <= total_idx

class FileGenerator:
    TRANSACTION_GENERATOR= partial(filegenerator, line_size=TRANSACTION_LINE_SIZE, dict_class=transaction)
    BUDGET_GENERATOR = partial(filegenerator, line_size=BUDGET_LINE_SIZE, dict_class=budget)
    CATEGORY_GENERATOR = partial(filegenerator, line_size=CATEGORY_LINE_SIZE, dict_class=category)
class ClassToBytePadding:
    TRANSACTION_PADDING=partial(addpadding, line_size=TRANSACTION_LINE_SIZE)
    BUDGET_PADDING=partial(addpadding, line_size=BUDGET_LINE_SIZE)
    CATEGORY_PADDING=partial(addpadding, line_size=CATEGORY_LINE_SIZE)
