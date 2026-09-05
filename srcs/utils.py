from .io_utils import isExist
from fileformat import transaction
from constants import MSG_LIST, TRANSACTION_LINE_SIZE, TRANSACTION_PATH, CATEGORY_PATH
from io_utils import ClassToBytePadding, FileGenerator, indexAvailable, seekfilesize

def ask(idx: int) -> transaction:
    while True:
        l:list[str] = []
        for msg in MSG_LIST:
            l.append(input(msg).strip())
        try:
            return transaction(idx, *l)
        except ValueError:
            continue

def addtransaction()->bool:
    with open(CATEGORY_PATH, "rb") as c, open(TRANSACTION_PATH,"rb+") as transaction_file:
        category = FileGenerator.CATEGORY_GENERATOR(c, rev=False)
        tx_id = seekfilesize(transaction_file) // TRANSACTION_LINE_SIZE + 1
        res = ask(tx_id)
        for a in category:
            if a.category == res.category:
                transaction_file.write(ClassToBytePadding.TRANSACTION_PADDING(res))
                print(f"tx_id:{tx_id}의 거래추가성공.")
                return True
        print("카테고리를 먼저 추가하세요")
        return False

# update -True Delete-False
def updatetransaction(tx_id:int, update:bool=True)->bool:
    with open(TRANSACTION_PATH,"rb+") as file:
        if not (indexAvailable(file, TRANSACTION_LINE_SIZE, tx_id)):
            return False
        if not isExist(file, TRANSACTION_LINE_SIZE, tx_id):
            return False
        file.seek(tx_id * TRANSACTION_LINE_SIZE)
        file.write(ClassToBytePadding.TRANSACTION_PADDING(ask(tx_id) if update else None))
        return True

#transaction의 generator활용
def transactionlist(n:int)->bool:
   with open(TRANSACTION_PATH, "rb") as file:
        g = FileGenerator.TRANSACTION_GENERATOR(file, rev=True)
        for a in range(n):
            try:
                trx = next(g)
                print(trx.__dict__)
            except StopIteration:
                print(f"{n}개 요청하였으나, 항목이 {a}개만 존재함.")
                return False
        return True