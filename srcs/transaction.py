from collections import Counter

from srcs.io_utils import isExist, addpadding, filegenerator, indexAvailable, getlastitem
from srcs.constants import TRANSACTION_LINE_SIZE, TRANSACTION_PATH, CATEGORY_PATH, BUDGET_PATH
from srcs.input_utils import ask_transaction
from srcs.schema import DATACLASS
from srcs.comparator import comp_date
from srcs.query import get_search_results
from srcs.io_utils import file_manager
from typing import  Any
import os

#1. 추가시 최신의데이터만 마지막인덱스에서 추출해 비교후, 인덱스를 +1씩하며 유니크한 아이디부여
#2. 카테고리가없으면, 카테고리를 추가하는것을 막음.
@file_manager({"f": (CATEGORY_PATH, "rb", False), "t": (TRANSACTION_PATH, "rb+", True)})
def addtransaction(files: dict[str, Any]) -> tuple[str, bool]:
    c_file, t_file = files['f'], files['t']
    category = filegenerator(c_file, DATACLASS['category'])
    last_item = getlastitem(t_file, DATACLASS['transaction'])
    tx_id = last_item.id + 1 if last_item else 0
    res = ask_transaction(tx_id)
    if res is None:
        return "시도횟수이내 적합한 데이터 입력을 실패했습니다", False
    if last_item and not comp_date(res.date, last_item.date):
        return "가계부는 최신순으로 추가해야합니다.", False
    for a in category:
        if a.category == res.category:
            t_file.seek(0, os.SEEK_END)
            t_file.write(addpadding(res, DATACLASS['transaction'].line_size))
            return f"tx_id:{tx_id}의 거래추가성공.", True
    return "카테고리를 먼저 추가하세요", False

@file_manager({"f": (TRANSACTION_PATH, "rb+", False)})
def updatetransaction(files: dict[str, Any], id:str, update: bool = True) -> tuple[str, bool]:
    f = files['f']
    tx_id = int(id)
    if not indexAvailable(f, DATACLASS['transaction'], tx_id):
        return "인덱스 범위 초과", False
    if not isExist(f, DATACLASS['transaction'], tx_id):
        return "해당 데이터가 존재하지 않습니다.", False
    f.seek(tx_id * TRANSACTION_LINE_SIZE)
    data = ask_transaction(tx_id) if update else None # 삭제 시 None(톰스톤)
    f.write(addpadding(data, DATACLASS['transaction'].line_size))
    return f"tx_id {tx_id} 처리 완료", True

#transaction의 generator활용
@file_manager({"f": (TRANSACTION_PATH, "rb", False)})
def transactionlist(files: dict[str, Any], n: int) -> tuple[str, bool]:
    f = files['f']
    g = filegenerator(f, DATACLASS['transaction'], rev=True)
    for a in range(n):
        try:
            trx = next(g)
            print(trx.__dict__)
        except StopIteration:
            return f"{n}개 요청했으나 {a}개만 존재함.", False
    return "조회 성공", True

@file_manager({"t": (TRANSACTION_PATH, "rb", False)})
def search(files: dict[str, Any], from_date:str | None = None, to_date:str | None = None, amount:str | None = None, type:str | None = None)->tuple[str, bool]:
    t = files['t']
    g = filegenerator(t, DATACLASS['transaction'], rev=True)
    search = get_search_results(from_date=from_date,to_date=to_date,amount= int(amount) if amount is not None else None,type_str=type)
    for a in g:
        if (search.match(a)):
            print(a.__dict__)
    return "출력을 종료합니다", True



# --- 집계 헬퍼 함수 ---
def aggregate_transactions(gen: Generator[Transaction, None, None], month: str):
    stats = {
        "income": 0,
        "expense": 0,
        "categories": Counter()
    }
    
    for tx in gen:
        # month가 "2023-10" 형태라면 tx.date("2023-10-15")의 앞부분과 비교
        if tx.date.startswith(month):
            if tx.type == "income":
                stats["income"] += tx.amount
            elif tx.type == "expense":
                stats["expense"] += tx.amount
                stats["categories"][tx.category] += tx.amount
                
    return stats

@file_manager({"t": (TRANSACTION_PATH, "rb", False), "b": (BUDGET_PATH, "rb", False)})
def summary(files: dict[str, Any], **kwargs) -> tuple[str, bool]:
    month = kwargs.get("month")
    top_n = int(kwargs.get("top", 5))
    
    t_file = files['t']
    b_file = files['b']
    
    # 1. 거래 데이터 집계
    g = filegenerator(t_file, DATACLASS['transaction'])
    stats = aggregate_transactions(g, month)
    
    # 2. 예산 가져오기
    budget_amount = 0
    bg = filegenerator(b_file, DATACLASS['budget'])
    for b in bg:
        if b.month == month:
            budget_amount = b.amount
            break
            
    # 3. 결과 출력
    print(f"\n=== {month} 요약 리포트 ===")
    print(f"총 수입: {stats['income']:,}원")
    print(f"총 지출: {stats['expense']:,}원")
    print(f"잔액: {stats['income'] - stats['expense']:,}원")
    
    if budget_amount > 0:
        diff = budget_amount - stats['expense']
        status = "여유" if diff >= 0 else "초과"
        print(f"예산 대비: {budget_amount:,}원 중 {stats['expense']:,}원 사용 ({status}: {abs(diff):,}원)")
    
    print(f"\n--- 지출 TOP {top_n} 카테고리 ---")
    for i, (cat, amt) in enumerate(stats['categories'].most_common(top_n), 1):
        print(f"{i}. {cat}: {amt:,}원")
    return "요약 완료", True