from __future__ import annotations
import json
from io import BufferedIOBase
from typing import Generator
import os
from srcs.schema import G, ClassConfig
from srcs.exception import DataException

def addpadding(my_class: object | None, line_size: int) -> bytes:
    if my_class is None:
        return b"\x20" * (line_size - 1) + b"\n"
    bts = json.dumps(my_class.__dict__, ensure_ascii=False).encode("utf-8")
    if len(bts) > line_size - 1:
        raise ValueError(f"데이터가 너무 큽니다! ({len(bts)} bytes / 제한: {line_size-1})")
    return bts.ljust(line_size - 1, b"\x20") + b"\n"

def is_tombstone(b:bytes)->bool:
    return b.strip(b"\x20") == b"\n"

def bytestoclass(line: bytes, d: ClassConfig[G]) -> G | None:
    try:
        data = json.loads(line.decode("utf-8"))
        return d.dict_type(**data)
    except (json.JSONDecodeError, ValueError, TypeError, UnicodeDecodeError) as e:
        print(f"데이터 해석 실패: {e}")
        raise DataException


def filegenerator(file: BufferedIOBase, d: ClassConfig[G], rev: bool = False) -> Generator[G, None, None]:
    if not rev:
        while True:
            line = file.read(d.line_size)
            if (is_tombstone(line)):
                continue
            if not line:
                return
            data = bytestoclass(line, d)
            if data is not None:
                yield data
    else:
        file.seek(0, os.SEEK_END)
        offset = file.tell() - d.line_size
        while offset >= 0:
            file.seek(offset)
            line = file.read(d.line_size)
            if (is_tombstone(line)):
                offset -=  d.line_size
                continue
            data = bytestoclass(line, d)
            if data is not None:
                yield data
            offset -= d.line_size


def isExist(file: BufferedIOBase, d: ClassConfig[G], idx: int) -> bool:
    file.seek(idx * d.line_size)
    line = file.read(d.line_size)
    if is_tombstone(line):
        return False
    file.seek(0)
    return True


def seekfilesize(file: BufferedIOBase):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size


def indexAvailable(file: BufferedIOBase, d: ClassConfig[G], idx: int) -> bool:
    size = seekfilesize(file)
    total_idx = size / d.line_size
    return idx <= total_idx


# if last exist return last item as G or None
def getlastitem(file: BufferedIOBase, d: ClassConfig[G]) -> G | None:
    try:
        return next(filegenerator(file, d, rev=True))
    except StopIteration:
        return None