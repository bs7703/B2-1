from srcs.exception import DataException
from srcs.dispatcher import VALID_CMD

def execute(cmd:str, options:dict[str, str]):
    try:
        msg, s = VALID_CMD[cmd](**options)
        print(msg, f"{s}")
    except DataException:
        print("데이터 무결성에 오류가있습니다")