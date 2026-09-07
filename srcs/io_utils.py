from __future__ import annotations
import json
from io import BufferedIOBase
from typing import Generator, Callable, TypeVar, ParamSpec
import os
from srcs.schema import G, ClassConfig
from srcs.exception import DataException
from functools import wraps
from contextlib import ExitStack
P = ParamSpec("P")
R = TypeVar("R")

def file_manager(file_configs: dict[str, tuple[str, str, bool]]):
    def decorator(func: Callable[..., R]) -> Callable[P, R | tuple[str, bool]]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | tuple[str, bool]:
            try:
                with ExitStack() as stack:
                    files = {}
                    for alias, (path, mode, make_file) in file_configs.items():
                        if (make_file):
                            directory = os.path.dirname(path)
                            if directory and not os.path.exists(directory):
                                os.makedirs(directory)
                            if not os.path.exists(path):
                                open(path, "ab").close()
                        files[alias] = stack.enter_context(open(path, mode))
                    return func(files, *args, **kwargs)
            except FileNotFoundError:
                return "필요한 데이터 파일이 존재하지 않습니다.", False
            except PermissionError:
                return "오류: 파일이 다른 프로그램에서 사용 중이거나 권한이 없습니다.", False
            except BlockingIOError:
                return "오류: 파일 읽기/쓰기 작업이 지연되고 있습니다. 잠시 후 다시 시도하세요.", False
            except OSError as e:
                if e.errno == 28: # No space left on device
                    return "오류: 디스크 공간이 부족하여 저장할 수 없습니다.", False
                return f"기타 OS 오류: {e.strerror}", False

        return wrapper
    return decorator

def addpadding(my_class: object | None, line_size: int) -> bytes:
    if my_class is None:
        return b"\x20" * (line_size - 1) + b"\n"
    bts = json.dumps(my_class.__dict__, ensure_ascii=False).encode("utf-8")
    if len(bts) > line_size - 1:
        raise ValueError(f"데이터가 너무 큽니다! ({len(bts)} bytes / 제한: {line_size-1})")
    return bts.ljust(line_size - 1, b"\x20") + b"\n"

def is_tombstone(b: bytes) -> bool:
    return b == b" " * (len(b) - 1) + b"\n"

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
            if not line:
                return
            if (is_tombstone(line)):
                continue
            data = bytestoclass(line, d)
            if data is not None:
                yield data
    else:
        file.seek(0, os.SEEK_END)
        offset = file.tell() - d.line_size
        while offset >= 0:
            file.seek(offset)
            line = file.read(d.line_size)
            offset -= d.line_size
            if (is_tombstone(line)):
                continue
            data = bytestoclass(line, d)
            if data is not None:
                yield data


def isExist(file: BufferedIOBase, d: ClassConfig[G], idx: int) -> bool:
    file.seek(idx * d.line_size)
    line = file.read(d.line_size)
    if not line:
        return False
    return not is_tombstone(line)


def seekfilesize(file: BufferedIOBase)->int:
    current = file.tell()
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(current)
    return size

def indexAvailable(file: BufferedIOBase, d: ClassConfig[G], idx: int) -> bool:
    size = seekfilesize(file)
    total_idx = size // d.line_size
    return idx <= total_idx


# if last exist return last item as G or None
def getlastitem(file: BufferedIOBase, d: ClassConfig[G]) -> G | None:
    return next(filegenerator(file, d, rev=True))