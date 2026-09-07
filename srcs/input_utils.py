from srcs.fileformat import Transaction,Category
from srcs.constants import TRANSACTION_MSG_LIST, CATEGORY_MSG_LIST
from srcs.constants import ASK_MAX

def ask_transaction(idx: int) -> Transaction | None:
    for n in range(ASK_MAX, 0, -1):
        print(f"남은시도횟수{n}")
        l:list[str] = []
        for msg in TRANSACTION_MSG_LIST:
            l.append(input(msg).strip())
        try:
            return Transaction(idx, *l)
        except ValueError as v:
            print(v)
            continue
    return None

def ask_category() -> Category | None:
    for n in range(ASK_MAX, 0, -1):
        print(f"남은시도횟수{n}")
        l:list[str] = []
        for msg in CATEGORY_MSG_LIST:
            l.append(input(msg).strip())
        try:
            return Category(*l)
        except ValueError as v:
            print(v)
            continue
