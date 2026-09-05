from srcs.io_utils import isExist, addpadding, filegenerator, indexAvailable, getlastitem
from srcs.fileformat import transaction,category, budget
from srcs.constants import TRANSACTION_MSG_LIST, CATEGORY_MSG_LIST, TRANSACTION_LINE_SIZE, TRANSACTION_PATH, CATEGORY_PATH, BUDGET_PATH
from srcs.schema import DATACLASS
from srcs.comparator import comp_date
from functools import wraps
from typing import Callable, TypeVar, ParamSpec, Any, Generator
from contextlib import ExitStack
from srcs.constants import ASK_MAX
from srcs.exception import DataException
from srcs.query import get_search_results
import csv
from collections import Counter
import os
P = ParamSpec("P")
R = TypeVar("R")

def ask_transaction(idx: int) -> transaction | None:
    for n in range(ASK_MAX, 0, -1):
        print(f"남은시도횟수{n}")
        l:list[str] = []
        for msg in TRANSACTION_MSG_LIST:
            l.append(input(msg).strip())
        try:
            return transaction(idx, *l)
        except ValueError:
            continue
    return None

def ask_category() -> category | None:
    for n in range(ASK_MAX, 0, -1):
        print(f"남은시도횟수{n}")
        l:list[str] = []
        for msg in CATEGORY_MSG_LIST:
            l.append(input(msg).strip())
        try:
            return category(*l)
        except ValueError:
            continue

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
            except Exception as e:
                return f"시스템 오류 발생: {e}", False
        return wrapper
    return decorator

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

@file_manager({"t": (TRANSACTION_PATH, "rb", False)})
def search(files: dict[str, Any], from_date:str | None = None, to_date:str | None = None, amount:str | None = None, type:str | None = None)->tuple[str, bool]:
    t = files['t']
    g = filegenerator(t, DATACLASS['transaction'], rev=True)
    search = get_search_results(from_date=from_date,to_date=to_date,amount= int(amount) if amount is not None else None,type_str=type)
    for a in g:
        if (search.match(a)):
            print(a.__dict__)
    return "출력을 종료합니다", True
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
    b.write(addpadding(budget(int(amount), month), DATACLASS['budget'].line_size))
    return res,True




# --- 집계 헬퍼 함수 ---
def aggregate_transactions(gen: Generator[transaction, None, None], month: str):
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

# --- 주요 기능 구현 ---
# --- CSV 스키마 정의 ---
CSV_COLUMNS = ["date", "type", "category", "amount", "memo", "tag"]

@file_manager({"t": (TRANSACTION_PATH, "rb+", True)})
def import_csv(files: dict[str, Any], **kwargs) -> tuple[str, bool]:
    csv_path = kwargs.get("from")
    t_file = files['t']
    
    last_item = getlastitem(t_file, DATACLASS['transaction'])
    next_id = last_item.id + 1 if last_item else 0
    
    count = 0
    try:
        # UTF-8로 읽기
        with open(csv_path, mode="r", encoding="utf-8-sig") as f: # utf-8-sig는 BOM 대응
            reader = csv.DictReader(f)
            for row in reader:
                # 필수값(Required) 확인
                if not all(row.get(col) for col in ["date", "type", "category", "amount"]):
                    continue
                
                new_tx = transaction(
                    id=next_id,
                    date=row['date'],
                    type=row['type'],
                    category=row['category'],
                    amount=int(row['amount']),
                    memo=row.get('memo', ""),
                    tags=row.get('tags', "")
                )
                
                t_file.write(addpadding(new_tx, DATACLASS['transaction'].line_size))
                next_id += 1
                count += 1
                
        return f"성공: {count}건의 데이터를 가져왔습니다.", True
    except Exception as e:
        return f"가져오기 실패: {e}", False

@file_manager({"t": (TRANSACTION_PATH, "rb", False)})
def export_csv(files: dict[str, Any], **kwargs) -> tuple[str, bool]:
    out_path = kwargs.get("out")
    month = kwargs.get("month")
    from_date = kwargs.get("from")
    to_date = kwargs.get("to")
    
    t_file = files['t']
    g = filegenerator(t_file, DATACLASS['transaction'])
    
    # 검색 엔진 활용
    search_engine = get_search_results(from_date=from_date or month, to_date=to_date or month)
    
    try:
        # UTF-8로 쓰기
        with open(out_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            writer.writeheader() # 헤더 포함
            
            count = 0
            for tx in g:
                if search_engine.match(tx):
                    # CSV 스키마에 있는 필드만 추출하여 저장 (id 제외)
                    row = {col: getattr(tx, col) for col in CSV_COLUMNS}
                    writer.writerow(row)
                    count += 1
                    
        return f"성공: {count}건의 데이터를 {out_path}에 저장했습니다.", True
    except Exception as e:
        return f"내보내기 실패: {e}", False

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
        if b.date == month:
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