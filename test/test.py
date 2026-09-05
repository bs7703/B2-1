import json
import random
from datetime import datetime, timedelta

# 설정된 라인 사이즈
TRX_SIZE = 256
CAT_SIZE = 128
BGT_SIZE = 64

def save_fixed_width_jsonl(filename, data, line_size):
    """데이터를 JSON으로 변환 후 스페이스 패딩을 채워 고정 크기로 저장"""
    with open(filename, 'wb') as f:  # 바이트 단위 쓰기를 위해 'wb' 모드
        for item in data:
            json_str = json.dumps(item, ensure_ascii=False)
            json_bytes = json_str.encode('utf-8')
            
            # 패딩 계산: (전체 사이즈 - 현재 바이트 - 1(줄바꿈문자))
            padding_size = line_size - len(json_bytes) - 1
            
            if padding_size < 0:
                raise ValueError(f"데이터가 설정된 {line_size}바이트를 초과합니다: {json_str}")
            
            # 데이터 + 스페이스 패딩 + 줄바꿈
            line = json_bytes + (b' ' * padding_size) + b'\n'
            f.write(line)

# --- 1. 카테고리 생성 (128바이트) ---
category_names = ["식비", "교통비", "주거비", "통신비", "의료비", "쇼핑", "취미", "교육", "월급", "부수입"]
categories = [{"category": name} for name in category_names]

# --- 2. 예산 생성 (64바이트, 월별 유니크, 카테고리 없음) ---
budgets = []
for month in range(1, 13):
    budgets.append({
        "month": f"2023-{month:02d}",
        "amount": random.randint(100, 999) * 10000 # 10,000,000 미만
    })

# --- 3. 트랜잭션 생성 (256바이트, ID/날짜 오름차순, 메모/태그 없음) ---
start_date = datetime(2023, 1, 1)
raw_dates = [start_date + timedelta(days=random.randint(0, 364), minutes=random.randint(0, 1439)) for _ in range(1000)]
raw_dates.sort()

transactions = []
for i, date in enumerate(raw_dates):
    cat = random.choice(category_names)
    is_income = cat in ["월급", "부수입"]
    transactions.append({
        "id": i + 1,
        "date": date.strftime("%Y-%m-%d"),
        "category": cat,
        "amount": random.randint(1, 100) * 5000,
        "type": "income" if is_income else "expense"
    })

# 파일 저장 실행
save_fixed_width_jsonl('category.jsonl', categories, CAT_SIZE)
save_fixed_width_jsonl('budget.jsonl', budgets, BGT_SIZE)
save_fixed_width_jsonl('transaction.jsonl', transactions, TRX_SIZE)

print(f"파일 생성 완료!")
print(f"- transaction.jsonl: {len(transactions)} lines, each {TRX_SIZE} bytes")
print(f"- category.jsonl: {len(categories)} lines, each {CAT_SIZE} bytes")
print(f"- budget.jsonl: {len(budgets)} lines, each {BGT_SIZE} bytes")