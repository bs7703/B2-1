from typing import TypeVar,Callable,TypedDict
from srcs.utils import addtransaction, transactionlist, updatetransaction
from srcs.validator import validate_month, validate_num, validate_suffix,validate_any
from .fileformat import budget, transaction, category
from functools import partial

T = TypeVar("T", transaction, budget)
K = TypeVar("K", transaction, category)
G = TypeVar("G", transaction, budget, category)
Validator = Callable[[str], bool]

class CommandSpec(TypedDict):
    pos: Validator | None
    options: dict[str, Validator | None]

TRANSACTION_PATH = "data/transcation.jsonl"
BUDGET_PATH = "data/budget.jsonl"
CATEGORY_PATH = "data/category.jsonl"

TYPE_RANGE = ["IN", "OUT"]
TRANSACTION_LINE_SIZE = 512
CATEGORY_LINE_SIZE = 64
BUDGET_LINE_SIZE = 64
CATEGORY_FIELD_SIZE = 40

MSG_LIST = [
    "날짜(YYYY-MM-DD): ",
    "타입(IN/OUT): ",
    "카테고리 (20자내): ",
    "금액(단위100/양수, 최대 1000000): "
]
VALID_COMMANDS: dict[str, CommandSpec] = {

    "add": {"pos": None, "options": {}},
    "list": {"pos": None, "options": {"limit": validate_num}},
    "search": {"pos": validate_any, "options": {
        "from": validate_month, "to": validate_month,
        "category": None, "type": None, "q": None, "tag": None
    }},

    "summary": {"pos": None, "options": {"month": validate_month, "top": validate_num}},

    "update": {"pos": None, "options": {"id": validate_num}},

    "delete": {"pos": None, "options": {"id": validate_num}},

    "import": {"pos": None, "options": {"from": validate_month}},

    "export": {"pos": None, "options": {
        "out": partial(validate_suffix, ".csv"),
        "month": validate_month, "from": validate_month, "to": validate_month
    }}
}


VALID_SUBCOMMANDS: dict[str, dict[str, CommandSpec]] = {
    "budget": {
        "set": {"pos": None, "options": {
            "month": validate_month, "amount": validate_num
        }}
    },
    "category": {
        "add": {"pos": validate_any, "options": {}},
        "list": {"pos": None, "options": {}},
        "remove": {"pos": validate_any, "options": {}}
    }
}

VALID_CMD:dict[str, Callable[..., bool]] = {
    "add": addtransaction,
    "update": partial(updatetransaction, update = True),
    "delete": partial(updatetransaction, update = False),
    "list": transactionlist
}