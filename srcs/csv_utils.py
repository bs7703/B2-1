from srcs.io_utils import addpadding, filegenerator,getlastitem
from srcs.constants import TRANSACTION_PATH
from srcs.schema import DATACLASS
from srcs.io_utils import file_manager
from srcs.query import get_search_results
import csv


# --- 주요 기능 구현 ---
# --- CSV 스키마 정의 ---
CSV_COLUMNS = ["date", "type", "category", "amount"]


@file_manager({"t": (TRANSACTION_PATH, "rb+", True)})
def import_csv(files: dict[str, Any], **kwargs) -> tuple[str, bool]:
    
    csv_path = kwargs.get("from")
    file_manager({"csv": (csv_path, "r", False)})
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
