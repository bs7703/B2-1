TRANSACTION_MSG_LIST = [
    "날짜(YYYY-MM-DD): ",
    "타입(income/expense): ",
    "카테고리 (20자내): ",
    "금액(단위100/양수, 최대 1000000): "
]
CATEGORY_MSG_LIST = [
    "카테고리 (20자내): "
]

ADD_HELP = """\
add
  새로운 거래 내역을 추가합니다.

사용법:
  add
  add --help
"""

LIST_HELP = """\
list
  저장된 거래 내역을 조회합니다.

사용법:
  list
  list --limit N
  list --help

옵션:
  --limit N
      최대 N개의 거래 내역을 표시합니다.
"""

SEARCH_HELP = """\
search
  조건에 맞는 거래 내역을 검색합니다.

사용법:
  search --from_date YYYY-MM
  search --to_date YYYY-MM
  search --amount AMOUNT
  search --type TYPE
  search --category CATEGORY

조건:
  하나 이상의 검색 옵션을 반드시 지정해야 합니다.

옵션:
  --from_date YYYY-MM
      검색 시작 월입니다.

  --to_date YYYY-MM
      검색 종료 월입니다.

  --amount AMOUNT
      거래 금액으로 검색합니다.

  --type TYPE
      거래 유형으로 검색합니다.

  --category CATEGORY
      거래 카테고리로 검색합니다.
"""

SUMMARY_HELP = """\
summary
  특정 월의 거래 내역을 요약합니다.

사용법:
  summary --month YYYY-MM
  summary --month YYYY-MM --top N
  summary --help

필수 옵션:
  --month YYYY-MM
      요약할 월입니다.

옵션:
  --top N
      상위 N개의 항목을 표시합니다.
"""

UPDATE_HELP = """\
update
  기존 거래 내역을 수정합니다.

사용법:
  update --id ID
  update --help

필수 옵션:
  --id ID
      수정할 거래의 ID입니다.
"""

DELETE_HELP = """\
delete
  기존 거래 내역을 삭제합니다.

사용법:
  delete --id ID
  delete --help

필수 옵션:
  --id ID
      삭제할 거래의 ID입니다.
"""

IMPORT_HELP = """\
import
  CSV 파일의 거래 데이터를 가져옵니다.

사용법:
  import --from YYYY-MM
  import --help

필수 옵션:
  --from YYYY-MM
      가져올 CSV 데이터의 기준 월입니다.
"""

EXPORT_HELP = """\
export
  거래 데이터를 CSV 파일로 내보냅니다.

사용법:
  export --out FILE.csv --month YYYY-MM
  export --help

필수 옵션:
  --out FILE.csv
      데이터를 저장할 CSV 파일 경로입니다.

  --month YYYY-MM
      내보낼 거래의 월입니다.

옵션:
  --from YYYY-MM
      검색 시작 월입니다.

  --to YYYY-MM
      검색 종료 월입니다.
"""

BUDGET_HELP = """\
budget
  예산 관련 명령을 관리합니다.

사용 가능한 명령:
  budget set
      특정 월의 예산을 설정합니다.

사용법:
  budget set --month YYYY-MM --amount AMOUNT
  budget --help
"""

BUDGET_SET_HELP = """\
budget set
  특정 월의 예산을 설정합니다.

사용법:
  budget set --month YYYY-MM --amount AMOUNT
  budget set --help

필수 옵션:
  --month YYYY-MM
      예산을 설정할 월입니다.

  --amount AMOUNT
      설정할 예산 금액입니다.
"""

CATEGORY_HELP = """\
category
  거래 카테고리를 관리합니다.

사용 가능한 명령:
  category add
      새로운 카테고리를 추가합니다.

  category list
      등록된 카테고리를 조회합니다.

  category remove
      기존 카테고리를 삭제합니다.

사용법:
  category add
  category list
  category remove
  category --help
"""

CATEGORY_ADD_HELP = """\
category add
  새로운 거래 카테고리를 추가합니다.

사용법:
  category add
  category add --help
"""

CATEGORY_LIST_HELP = """\
category list
  등록된 모든 거래 카테고리를 조회합니다.

사용법:
  category list
  category list --help
"""

CATEGORY_REMOVE_HELP = """\
category remove
  기존 거래 카테고리를 삭제합니다.

사용법:
  category remove
  category remove --help
"""

HELP_MESSAGES = {
    "add": ADD_HELP,
    "list": LIST_HELP,
    "search": SEARCH_HELP,
    "summary": SUMMARY_HELP,
    "update": UPDATE_HELP,
    "delete": DELETE_HELP,
    "import": IMPORT_HELP,
    "export": EXPORT_HELP,
    "budget": BUDGET_HELP,
    "budget set": BUDGET_SET_HELP,
    "category": CATEGORY_HELP,
    "category add": CATEGORY_ADD_HELP,
    "category list": CATEGORY_LIST_HELP,
    "category remove": CATEGORY_REMOVE_HELP,
}